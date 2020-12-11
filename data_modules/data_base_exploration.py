# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 16:35:50 2020

    Explore downloaded open source data
    https://www.notion.so/Publications-Scientifiques-APIs-f0ee5df762f049e29584cacd4f456efb
    http://s2-public-api-prod.us-west-2.elasticbeanstalk.com/corpus/

    wget https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/2020-11-06/manifest.txt
    wget -B https://s3-us-west-2.amazonaws.com/ai2-s2-research-public/open-corpus/2020-11-06/ -i manifest.txt

@author: CHRISTIAN
"""


# D:\ecomdataforgoodfr\Ceebios\base_open_source


import os
import glob
import json
import getopt

import gzip
import io

import ntpath

import time
import pprint

pp = pprint.PrettyPrinter(2)
import json
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)
pd.set_option("max_colwidth", 1000)


if False:  # local desktop working
    os.chdir("D:/ecomdataforgoodfr/Ceebios/batch8_ceebios/base_open_source")
    print(os.getcwd())

from scispacy_lib import explore__text_byScispacy


def read_parameters(argv):
    """ definition ou lecture des parametres d'entree """
    # example of execution
    # python data_base_exploration.py --path ./data_dir

    # default value
    path = "D:/ecomdataforgoodfr/Ceebios/base_open_source"

    opts = None
    try:
        if argv is not None and len(argv) > 0:
            opts, _ = getopt.getopt(argv, "p", ["path="])
    except getopt.GetoptError as e:
        print("Invalid arguments")
        print(e)
        exit(2)

    if opts is not None:
        for opt, arg in opts:
            if opt in ("-p", "--path"):
                path = arg
    return path


def add_rows(r):
    global dh

    k = r["key"]
    name_lst = r["name_lst"]
    for word in name_lst:
        dh = dh.append({"key": k, "canonicalName": word}, ignore_index=True)


def df_generate(df, rank, columns_lst, output_file):
    df_family = df[df["rank"] == rank]
    df_family = df_family[columns_lst]
    df_family.reset_index(drop=True, inplace=True)
    df_family.to_csv(output_file, sep=";")
    print("df ", rank, " generate:", output_file)
    print(df_family.shape, list(df_family.columns))
    print(df_family.head())
    return df_family


def read_gbif_extract_csvCategorical(file_name="../data/gbif_extract.csv"):
    """ load gbif csv data base """
    """ output csv files with short names and key """

    output_file_family = "../data/gbif_extract_family.csv"
    output_file_genus = "../data/gbif_extract_genus.csv"
    output_file_species = "../data/gbif_extract_species.csv"
    output_file_categories = "../data/gbif_extract_categories.csv"

    important_cols = [
        "speciesKey",
        "canonicalName",
        "family",
        "familyKey",
        "genus",
        "genusKey",
        "rank",
    ]
    df = pd.read_csv(file_name)
    print(df.shape, list(df.columns))
    print("-important columns:")
    df = df[important_cols]
    print(df.shape, list(df.columns))

    for c in list(df.columns):
        if c.find("Key") == -1:
            df[c] = df[c].apply(str).str.lower()

    print("rank list:", df["rank"].unique())

    df_family = df_generate(
        df, "family", ["familyKey", "family", "rank"], output_file_family
    )
    df_genus = df_generate(
        df, "genus", ["genusKey", "genus", "rank"], output_file_genus
    )

    df_species = df[(df["rank"] == "species") | (df["rank"] == "subspecies")]
    df_species.reset_index(drop=True, inplace=True)

    print("df_species", df_species.shape)
    print(df_species.head())
    df_species.to_csv(output_file_species, sep=";")
    print("df ", "species and subspecies", " generate:", output_file_species)

    print("Categorical <=> concat family + genus + species names list")
    df_cat_columns = ["key", "name", "rank"]
    # concat family + genus + species
    df_cat = df_family
    df_cat.columns = df_cat_columns
    df_genus.columns = df_cat_columns
    df_species = df_species[["speciesKey", "canonicalName", "rank"]]
    df_species.columns = df_cat_columns
    dg = pd.concat([df_cat, df_genus, df_species])

    dg.reset_index(drop=True, inplace=True)
    dg.to_csv(output_file_categories, sep=";")
    print("df_cat", dg.shape)
    print(
        "df ",
        "categories = [family+genus+species]",
        " generate:",
        output_file_categories,
    )
    return dg

dg_gbif_Categorical = None
def search_in_gbif_extract_Categorical(keyword):
    ''' search keyword in dataset '''
    ''' input keyword, output gbif_id, keyword, rank '''
    global dg_gbif_Categorical
    df = dg_gbif_Categorical[dg_gbif_Categorical['name']==keyword]
    if len(df)>0:
        return list(df.values[0])
    return([0, keyword, ''])

dg_gbif_Categoricalx = None
def search_in_gbif_extract_Categoricald_x(keyword):
    ''' search with indexed column '''
    ''' this one is faster '''
    ''' input keyword, output gbif_id, keyword, rank '''
    global dg_gbif_Categoricalx
    
    try:
        df = dg_gbif_Categoricalx.loc[keyword]
        return list(df)
    except:
        pass
    return([0, keyword, ''])
    

def read_gbif_extract_csvCategorical_test():
    global dg_gbif_Categorical
    
    file_categories = "../data/gbif_extract_categories.csv"
    
    dg = pd.read_csv(file_categories, names=['key', 'name', 'rank'], sep=';')
    print(dg.shape, dg.columns)
    print(dg.head())
    dg_gbif_Categorical = dg
    keyword = 'oedicerotidae'
    print(search_in_gbif_extract_Categorical(keyword))
    ts = time.time()
    for i in range(0,2000):
        keyword = 'austronecydalopsis iridipennis'
        ret = search_in_gbif_extract_Categorical(keyword)
    print('time:', time.time()-ts) # 11.45

    print('Same loop but with index:(work if key does exist)')
    dg_gbif_Categoricalx = dg_gbif_Categorical
    dg_gbif_Categoricalx.index = dg_gbif_Categoricalx['name']
    ts = time.time()
    for i in range(0,2000):
        keyword = 'austronecydalopsis iridipennis'
        ret = search_in_gbif_extract_Categoricald_x(keyword)
    print('time:', time.time()-ts) # 3.57
        
    
        
        
def read_gbif_extract_csv(
    file_name="../data/gbif_extract.csv",
    output_file="../data/gbif_extract_canonicalName_short.csv",
):
    """ load gbif csv data base """
    """ output csv files with short names and key """
    """ used to detect canonical names """
    """ see "search_canonicalName()" function in scispacy_lib.py module """

    important_cols = ["key", "canonicalName"]
    df = pd.read_csv(file_name)
    print(df.shape, list(df.columns))

    print("-important columns:")
    df = df[important_cols]
    print(df.shape, list(df.columns))

    # print(df.head(10))
    for c in list(df.columns):
        if c.find("Key") == -1:
            df[c] = df[c].apply(str).str.lower()
    print(df.shape, list(df.columns))
    print("canonicalName:")
    print(df.head(10))
    df["name_lst"] = df["canonicalName"].apply(lambda x: x.split(" "))
    df["size"] = df["name_lst"].apply(lambda x: len(x))
    print(df["size"].describe())
    ##### output
    print("Output file with short reduce canonical name:", output_file)
    print("- to find canonical name in abstract sci. papers")
    tot_rows = df.shape[0]
    ts = time.time()
    total_read = 0
    total_write = 0
    dct = {}
    with open(output_file, "w") as f:
        f.write("canonicalName_word;tab_key\n")
        for i, r in df.iterrows():
            total_read += 1
            if time.time() - ts > 10:
                ts = time.time()
                print(
                    total_read,
                    "/",
                    tot_rows,
                    round(total_read / tot_rows * 100, 2),
                    "%",
                )
            if r["key"] is None:
                continue
            if r["size"] == 1:
                name = r["canonicalName"]
                # dct[name] = [r['key']]
                # print(name, dct[name], 'name first in')
                f.write(name + ";" + str(r["key"]) + "\n")
                total_write += 1
                continue
            for name in r["name_lst"]:
                f.write(name + ";" + str(r["key"]) + "\n")
                total_write += 1
            continue
        print("Data report:", "total_read", total_read, "total_write", total_write)
    print("End file generated:", output_file)

    if False:
        # following code just produced an out of memory
        text = df["canonicalName"].values
        # create the transform
        vectorizer_canonicalName = CountVectorizer()
        # tokenize and build vocab
        vectorizer_canonicalName.fit(text)

        # summarize
        print("len vectorizer.vocabulary_):", len(vectorizer.vocabulary_))
        print("canonicalName:")
        i = 0
        for k, v in vectorizer_canonicalName.vocabulary_.items():
            print(k, v)
            i += 1
            if i > 10:
                break

        # encode document*
        text = "psygmatocerus guianensis"
        vector = vectorizer.transform([text])
        vector.toarray()

        text_out = vectorizer.inverse_transform(vector)
        print(text_out)

        dataX = []
        dataY = []
        for i, r in df_canonicalName.iterrows():
            dataY.append(int(r["key"]))
            v = vectorizer_canonicalName.transform([r["canonicalName"]])
            dataX.append(list(v.toarray()[0]))
        n_patterns = len(dataX)
        print("Total Patterns: ", n_patterns)


def get_gz_tab_files(path):
    """ create a list of compressed gz files downloades """
    path2 = path + "/*.gz"
    path3 = path + "/**/*.gz"

    tab_files = glob.glob(path2)
    tab_files3 = glob.glob(path3)
    return tab_files + tab_files3


def from_json(file):
    """Get Shape from json file."""
    with open(file, "r") as fp:
        doc = json.load(fp)
    return doc


def load_one_gz_file(gz_file):
    """ extract json data from compressed file """
    tab_doc = []
    gz = gzip.open(gz_file, "rb")
    f = io.BufferedReader(gz)
    for line in f.readlines():
        tab_doc.append(json.loads(line))
    gz.close()
    return tab_doc


def main(argv=[]):
    """ main entry point """
    # argv=[]
    path = read_parameters(argv)
    tab_files = get_gz_tab_files(path)
    print("Nb of commpressed gz files:", len(tab_files))
    gz_file = tab_files[0]
    tab_doc = load_one_gz_file(gz_file)
    print("file:", ntpath.basename(gz_file), "length:", len(tab_doc))
    df = pd.DataFrame(tab_doc)
    print(df.shape)
    print(list(df.columns))
    print(df.head(1))

    dfa = df[df["paperAbstract"] != ""]
    dfa.reset_index(drop=True, inplace=True)
    display(dfa["paperAbstract"].loc[0])
    x = dfa["paperAbstract"].loc[0]
    explore__text_byScispacy(x)


if __name__ == "__main__":
    main(sys.argv[1:])
