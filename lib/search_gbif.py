# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 14:08:30 2020

Module de recherche sur la base gbif https://www.gbif.org/fr/

http://tecfa.unige.ch/perso/lombardf/calvin/teaching/mammiferes-fr-latin.html

@author: CHRISTIAN
"""


from pygbif import species

species.name_suggest(q='Puma concolor')

nb_species = 0
for i in range(0, 10):
    tab_rep = species.name_suggest(q='vespa', offset=i)
    print(len(tab_rep))
    for doc in tab_rep:
        if 'species' in doc:
            nb_species += 1
            print(doc['species'])
            
            
print(nb_species)            

