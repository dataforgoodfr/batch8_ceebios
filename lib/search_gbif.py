# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 14:08:30 2020

Module de recherche sur la base gbif https://www.gbif.org/fr/

http://tecfa.unige.ch/perso/lombardf/calvin/teaching/mammiferes-fr-latin.html

@author: CHRISTIAN
"""


import os
import time
import pprint
import json
import re
import pandas as pd
from nltk.probability import FreqDist

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from pygbif import species
from scipy import sparse


if False: # local desktop working
    os.chdir('D:/ecomdataforgoodfr/Ceebios/batch8_ceebios/lib')
    print(os.getcwd())



def test_species():    
    data = species.name_suggest(q='Puma concolor')
    for x in data:
        print(len(x))
    
    data2 = species.name_suggest()
    for x in data2:
        print(len(x))
    
    nb_species = 0
    for i in range(0, 10):
        tab_rep = species.name_suggest(q='vespa', offset=i)
        print(len(tab_rep))
        for doc in tab_rep:
            if 'species' in doc:
                nb_species += 1
                print(doc['species'])
            
            
    print(nb_species)            

def collect_all_species(fname = "../data/tfidf/data_gbif.json"):
    ''' collect all species '''
    
    last_read = 1
    offset = 0
    ts = time.time()
    dct = {}
    nb_species = 0
    data = []
    while last_read>0:
        tab_rep = species.name_suggest(offset=offset)
        offset += 1 
        # if time.time()-ts>60:
        #    break
        last_read = len(tab_rep)
        for x in tab_rep:
            nb_species += 1
            data.append(x)
            for k in x.keys():
                if k not in dct:
                    dct[k] = 1
                else:
                    dct[k] += 1 
                    
    pp = pprint.PrettyPrinter(2)                
    print('nb species', nb_species)
    print('Dict:', len(dct))
    pp.pprint(dct)
    
    with open(fname,"w", encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile,ensure_ascii=False)
    print(time.time()-ts)    
        
        
def read_collect_bgif(fname = "../data/tfidf/data_gbif.json"):
    datain = []
    with open(fname,"r", encoding='utf-8') as jsonfile:
        datain = json.load(jsonfile)
    return datain


def create_Tf_matrix(corpus, \
                     filename_npz='../data/tfidf/data_tf.npz', \
                     filename_features="../data/tfidf/data_feature_names.pkl"):
    ''' creation d'une matrice TF '''
    
    vectorizer = CountVectorizer(max_features=len(corpus))
    X = vectorizer.fit_transform(corpus)
    print('-Vectorized matrix, ', X.toarray().shape)
    print(' first line:')
    print(X.toarray()[0])
    print('- Nombre de features :'+str(len(vectorizer.get_feature_names())))
    print(vectorizer.get_feature_names()[0:10], ' ...')
    
    data = pd.DataFrame(vectorizer.get_feature_names())
    data.to_pickle(filename_features) 
    print('tf feature names - saved')
    sparse.save_npz(filename_npz, X)
    print('tf matrix:', filename_npz,' - saved')

def create_TfIdf(corpus, \
                     filename_npz='../data/tfidf/data_tfidf.npz', \
                     filename_features="../data/tfidf/data_tfidf_feature_names.pkl"):
    '''    
    Création de la matrice pondérée TF-IDF (Term Frequency times Inverse Document Frequency)
    La matrice TF-IDF est une mesure qui permet de faire de la ségrégation entre documents.
    Si un mot a une très haute fréquence dans une question, mais une fréquence basse dans les autres questions du corpus,
    c’est qu’il s’agit d’un mot important pour caractériser le document en question.
    '''
    vectorizer = TfidfVectorizer(max_features=len(corpus))
    X = vectorizer.fit_transform(corpus)
    print('-Tfidf matrix, ', X.toarray().shape)
    print(' first line:')
    print(X.toarray()[0])
    
    print('- Nombre de features :'+str(len(vectorizer.get_feature_names())))
    print(vectorizer.get_feature_names()[0:10], ' ...')
    
    data = pd.DataFrame(vectorizer.get_feature_names())
    data.to_pickle(filename_features) 
    print('tfidf feature names - saved')
    sparse.save_npz(filename_npz, X)
    print('tfidf matrix:', filename_npz,' - saved')


def read_clean_dataset(fname, disp_first=True):
    ''' load dataset '''
    
    datain = read_collect_bgif(fname)
    if disp_first==True:
        print('- We suppress key fields, and convert to minus')
    
    tab = []
    for doc in datain:
        terms = []
        for k, v in doc.items():
            if k.endswith('Key')==False:
                if type(v)!=str:
                    continue
                v = v.lower()
                v = re.sub(r"[^a-z]+", ' ', v)
                terms.append(v)
        tab.append({'terms': terms})
        
    if disp_first==True:
        pp = pprint.PrettyPrinter(2)
        print('First doc, before')
        pp.pprint(datain[0])
        print('then')
        print(tab[0])
    
    dataset = pd.DataFrame(tab)    
    dataset['d'] = dataset.index
    
    return dataset

def load_clean_and_generate_tf_idf(fname="../data/tfidf/data_gbif.json"):
    ''' clean dataset and create tf and tfidf '''
    
    print(" load dataset, and clean")
    dataset = read_clean_dataset(fname)
    print('- Verification:')
    display(dataset.head())
    
    
    dataset['freq'] = dataset['terms'].apply(lambda x: FreqDist(x))
    
    #fdist1 : frequence dans le tableau de mots
    print("Calcul de la frequence des mots")
    fdist = dataset['freq'].sum()
    print('Words list created, size:', len(fdist))
    
    
    print('- mots les plus fréquents:')
    d_list = pd.DataFrame(fdist.most_common(100))
    print(d_list)
    # c = sorted(d_list[0])
    dataset['line'] = dataset['terms'].apply(lambda x: ' '.join(x))
    corpus = dataset['line'].to_list()
    print('corpus len:', len(corpus))
    
    print('- create tf matrix')
    create_Tf_matrix(corpus)
    print('- create tfidf matrix')
    create_TfIdf(corpus)
    
    
            