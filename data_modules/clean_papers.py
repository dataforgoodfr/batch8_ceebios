import gzip
import io
import json
import os

import en_core_sci_lg
import pandas as pd

from data_modules.utils import (
    get_gbif_keyprocessor,
    remove_empty_abstract,
    keep_columns,
    keep_english_titles,
    remove_stopwords_from_title_abstract,
    keep_articles_with_species,
    add_entities,
    list_stopwords,
)

gbif_source_path = (
    "/Users/chloesekkat/Documents/batch8_ceebios/data/simplified_taxon_gbif.csv"
)
papers_data_dir = "/Users/chloesekkat/Documents/batch8_ceebios/data_open_source"

to_keep = ["title", "paperAbstract", "year", "fieldsOfStudy"]
keyword_processor = get_gbif_keyprocessor(gbif_source_path)
nlp = en_core_sci_lg.load()


def get_gz_files_clean(data_dir: str) -> None:
    """
    Clean all gz files and save them in csv format.
    """
    for file in os.listdir(data_dir):
        if file.endswith(".gz"):
            json_list = []
            gz = gzip.open(os.path.join(data_dir, file), "rb")
            f = io.BufferedReader(gz)
            for line in f.readlines():
                json_list.append(json.loads(line))
            gz.close()
            data = pd.DataFrame(json_list)
            data = remove_empty_abstract(data)
            data = keep_columns(data, to_keep)
            data["year"] = data["year"].fillna(0)
            data["year"] = data["year"].astype(int)
            data = keep_english_titles(data)
            data = remove_stopwords_from_title_abstract(data, list_stopwords)
            data = keep_articles_with_species(data, keyword_processor)
            data = add_entities(data, nlp)
            data.to_csv(f"../data/scientific_papers/{file[:-3]}.csv", index=False)
            print(f"{file[:-3]} DONE")


if __name__ == "__main__":
    get_gz_files_clean(papers_data_dir)
