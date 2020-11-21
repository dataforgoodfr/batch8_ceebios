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
import json
import re
import pandas as pd


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('max_colwidth', 1000)


if False: # local desktop working
    os.chdir('D:/ecomdataforgoodfr/Ceebios/batch8_ceebios/lib')
    print(os.getcwd())

def read_parameters(argv):
    ''' definition ou lecture des parametres d'entree '''
    # example of execution
    # python data_base_exploration.py --path ./data_dir

    # default value
    path = "D:/ecomdataforgoodfr/Ceebios/base_open_source"
    
    opts = None
    try:
        if argv is not None and len(argv)>0:
            opts, _ = getopt.getopt(argv,
                                    "p",
                                    ["path="])
    except getopt.GetoptError as e:
        print("Invalid arguments")
        print(e)
        exit(2)

    if opts is not None:
        for opt, arg in opts:
            if opt in ('-p', '--path'):
                path = arg
    return path


def get_gz_tab_files(path):
    ''' create a list of compressed gz files downloades '''
    path2 = path + '/*.gz'
    path3 = path + '/**/*.gz'

    
    tab_files = glob.glob(path2)   
    tab_files3 = glob.glob(path3)   
    return tab_files + tab_files3


def from_json(file):
    """Get Shape from json file."""
    with open(file, 'r') as fp:
        doc = json.load(fp)
    return doc


def load_one_gz_file(gz_file):
    ''' extract json data from compressed file '''
    tab_doc = []
    gz = gzip.open(gz_file, 'rb')
    f = io.BufferedReader(gz)
    for line in f.readlines():
         tab_doc.append(json.loads(line))         
    gz.close()
    return tab_doc



def main(argv=[]):
    ''' main entry point '''
    # argv=[]
    path = read_parameters(argv)
    tab_files = get_gz_tab_files(path)
    print('Nb of commpressed gz files:', len(tab_files))
    gz_file = tab_files[0]
    tab_doc = load_one_gz_file(gz_file)
    print('file:', ntpath.basename(gz_file), 'length:', len(tab_doc))
    df = pd.DataFrame(tab_doc)
    print(df.shape)
    print(list(df.columns))
    print(df.head(1))

if __name__ == "__main__":
    main(sys.argv[1:])