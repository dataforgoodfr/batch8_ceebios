# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 13:00:30 2020

Module de recherche d'articles dans Google Scholar

usage :
    from scholar import search_articles
    tab_doc = search_articles('brain tumor classification', 10)
        

@author: CHRISTIAN
"""

import pprint

# pip install scholarly
from scholarly import scholarly
from .publication import Publication



class GoogleScholarExtractor:
    def __init__(self):
        pass


    def search(self,query,n = 5):
        ''' recherche d articles '''           
        search_query = scholarly.search_pubs(query)
        pubs = []
        for i in range(n):
            try:
                pub = next(search_query)
                pubs.append(Publication(scholar_data = pub))
            except Exception as e:
                print(f"Stopped because of {e}")
                return pubs
        return pubs
            



def get_author(generator):
    ''' lecture de l inofrmation '''
    try:
        doc = next(generator)
    except Exception as e:
        doc = None
        print('Excp:'+str(e))
    return doc    
    
def test_scholar():
    ''' test de la connexion google scholar '''    
    pp = pprint.PrettyPrinter(2)
    tab_author = ['xxxx bidule', 'Steven A. Cholewiak']
    for author in tab_author:
        generator = scholarly.search_author(author)
        doc = get_author(generator)
        if doc is None:
            print('Author not found:'+author)
        else:    
            print('Author found:'+author)
            pp.pprint(doc)    
    '''    
    {'affiliation': 'Vision Scientist',
     'citedby': 297,
     'email': '@berkeley.edu',
     'filled': False,
     'id': '4bahYMkAAAAJ',
     'interests': ['Depth Cues',
                   '3D Shape',
                   'Shape from Texture & Shading',
                   'Naive Physics',
                   'Haptics'],
     'name': 'Steven A. Cholewiak, PhD',
     'url_picture': 'https://scholar.google.com/citations?view_op=medium_photo&user=4bahYMkAAAAJ'}
    '''
        
    
# if True:
#     test_scholar()
'''    
    Quick example demonstrating how to retrieve an author's profile 
    then retrieve the titles of the papers that cite his most popular (cited) paper.
'''    

def seach_author(author='Steven A Cholewiak'):    
    # Retrieve the author's data, fill-in, and print
    search_query = scholarly.search_author('Steven A Cholewiak')
    try:
        author_p = next(search_query).fill()
        # print(author)
    except:
        return None, [], []
    
    # Print the titles of the author's publications
    auth_pub_lst = [pub.bib['title'] for pub in author_p.publications]
    # print([pub.bib['title'] for pub in author_p.publications])
    
    # Take a closer look at the first publication
    pub = author_p.publications[0].fill()
    auth_cit_lst = [citation.bib['title'] for citation in pub.citedby]
    # print(pub)
    
    # Which papers cited that publication?
    # print(auth_cit_lst)    
    return author_p, auth_pub_lst, auth_cit_lst
    
def seach_author_test():
    ''' test search author '''
    pp = pprint.PrettyPrinter(2)
    author = 'Steven A Cholewiak'
    author_p, auth_pub_lst, auth_cit_lst = seach_author(author)
    if author_p is None:
        print('-Author not found:'+author)
    if author_p is not None:
        for doc in [author_p, auth_pub_lst, auth_cit_lst]:
            pp.pprint(doc)
            
def search_articles(query, n=5):
    ''' recherche d articles '''           
    search_query = scholarly.search_pubs(query)
    tab_doc = []
    for i in range(0, n):
        try:
            doc = next(search_query)
            tab_doc.append(doc)
        except:
            doc = None
            return tab_doc
    return tab_doc    
        
def search_articles_test():
    ''' test de la fonction recherche d'articles '''
    pp = pprint.PrettyPrinter(2)
    query = 'building a second brain tumor classification deep learning'
    query = 'pegea confoderata'
    tab_doc =  search_articles(query)
    for doc in tab_doc:
        pp.pprint(doc)
    return tab_doc    
        