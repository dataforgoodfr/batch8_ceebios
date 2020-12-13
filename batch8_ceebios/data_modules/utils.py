from typing import List, Set

import pandas as pd
from flashtext import KeywordProcessor
from langdetect import detect
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from thinc.neural import Model

stop_words = set(stopwords.words("english"))

own_list = set(
    [
        "age",
        "sea",
        "data",
        "idea",
        "may",
        "america",
        "robert",
        "taiwan",
        "canada",
        "gordon",
        "major",
    ]
)

list_stopwords = stop_words | own_list


def get_gbif_keyprocessor(source_path: str) -> KeywordProcessor:
    """
    Get GBIF keyprocessor with all species/family/genus names needed.
    """
    gbif = pd.read_csv(source_path)
    gbif = gbif.dropna()
    all_species = gbif["canonicalName"].unique().tolist()
    all_family = gbif["family"].unique().tolist()
    all_genus = gbif["genus"].unique().tolist()
    all_names = set(all_species + all_family + all_genus)
    keyword_processor = KeywordProcessor()
    for name in all_names:
        keyword_processor.add_keyword(name)

    keyword_processor.remove_keywords_from_list(list(list_stopwords))
    return keyword_processor


def keep_columns(df: pd.DataFrame, cols_to_keep: List[str]) -> pd.DataFrame:
    """
    Return dataframe with wanted columns.
    """
    return df[cols_to_keep]


def remove_empty_abstract(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows where paper abstract is an empty string.
    """
    where = df["paperAbstract"].values != ""
    return df[where]


def remove_empty_titles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows where title is an empty string.
    """
    where = df["title"].values != ""
    return df[where]


def keep_english_titles(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keep only papers with title in english.
    """
    where = df["title"].map(detect).astype(str) == "en"
    return df[where].reset_index(drop=True)


def remove_stopwords_from_title_abstract(
    data: pd.DataFrame, list_stopwords: Set
) -> pd.DataFrame:
    """
    Remove all stopwords from title and abstract in order to prevent many false positive.
    """
    data = data.reset_index(drop=True)
    data["full"] = data["title"] + " " + data["abstract"]
    data["full"] = data["full"].str.lower()
    data["full"] = data["full"].map(lambda x: word_tokenize(x))
    data["full"] = data["full"].map(
        lambda sentence: " ".join(
            [word for word in sentence if not word in list_stopwords]
        )
    )
    return data


def keep_articles_with_species(
    data: pd.DataFrame, keyword_processor: KeywordProcessor
) -> pd.DataFrame:
    """
    Keep only articles for which we find a match and add a keyword column.
    Keywords are searched in paper title and paper abstract.
    The matched keywords need to be previously set in `keyword_processor`.
    """
    data["keyword"] = data["full"].map(lambda x: keyword_processor.extract_keywords(x))
    where = data["keyword"].astype(str) == "[]"
    data = data[~where]
    data = data.drop(["full"], axis=1)
    data = data.reset_index(drop=True)
    return data


def add_entities(data: pd.DataFrame, nlp: Model) -> pd.DataFrame:
    """
    Add to data a column `entities` which are found thanks to scispacy
    https://github.com/allenai/scispacy
    """
    data["tags"] = data["abstract"].map(lambda x: nlp(x).ents)
    return data


def add_all_ids_to_species(data: pd.DataFrame, cat_data: pd.DataFrame) -> pd.DataFrame:
    """
    Add all necessaries ids to match documents with gbif_id, canonical_name, rank.
    """
    df_join = pd.merge(
        data.explode("keyword"),
        cat_data,
        left_on="keyword",
        right_on="canonicalName",
        how="inner",
    )
    df_join["dict_species"] = df_join.apply(
        lambda row: {
            "gbif_id": row["taxonID"],
            "canonical_name": row["canonicalName"],
            "rank": row["taxonRank"],
        },
        axis=1,
    )
    df_tmp = (
        df_join.groupby(["doc_id", "title", "abstract"])
        .agg({"dict_species": lambda x: list(x)})
        .reset_index()
    )
    df_join = df_join.drop(
        ["keyword", "taxonID", "canonicalName", "taxonRank", "dict_species"], axis=1
    )
    df_join = df_join.drop_duplicates(subset=["doc_id", "title", "abstract"])
    df_final = pd.merge(
        df_join, df_tmp, on=["doc_id", "title", "abstract"], how="inner"
    )
    return df_final
