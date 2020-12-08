import gzip
import io
import json
import os
import time

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


class Loader:
    def __init__(self):
        self.gbif_source_path = (
            "/Users/chloesekkat/Documents/batch8_ceebios/data/simplified_taxon_gbif.csv"
        )
        self.papers_data_dir = (
            "/Users/chloesekkat/Documents/batch8_ceebios/data_open_source"
        )

        self.to_keep = [
            "id",
            "title",
            "paperAbstract",
            "authors",
            "year",
            "fieldsOfStudy",
            "journalName",
            "doiUrl",
        ]
        self.keyword_processor = get_gbif_keyprocessor(self.gbif_source_path)
        self.nlp = en_core_sci_lg.load()


def clean_gz_to_csv(data_dir: str, file: str, loader: Loader) -> None:
    """
    Clean all gz files and save them in csv format.
    """
    json_list = []
    gz = gzip.open(os.path.join(data_dir, file), "rb")
    f = io.BufferedReader(gz)
    for line in f.readlines():
        json_list.append(json.loads(line))
    gz.close()
    data = pd.DataFrame(json_list)
    data = remove_empty_abstract(data)
    data = keep_columns(data, loader.to_keep)
    data["year"] = data["year"].fillna(0)
    data["year"] = data["year"].astype(int)
    data = keep_english_titles(data)
    data = remove_stopwords_from_title_abstract(data, list_stopwords)
    data = keep_articles_with_species(data, loader.keyword_processor)
    data = add_entities(data, loader.nlp)
    data.to_json(
        f"/Volumes/Extreme SSD/ceebios/{file[:-3]}.json",
        orient="records",
        default_handler=str,
    )
    print(f"{file[:-3]} DONE")


def main():
    loader = Loader()
    for file in os.listdir(loader.papers_data_dir):
        if file.endswith(".gz"):
            clean_gz_to_csv(loader.papers_data_dir, file, loader)


if __name__ == "__main__":
    main()
