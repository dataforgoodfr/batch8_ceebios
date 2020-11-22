# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 19:10:35 2020

@author: CHRISTIAN
"""

'''
!pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.2.4/en_core_sci_sm-0.2.4.tar.gz --user
'''

import scispacy                                                        
import spacy                                                        
import en_core_sci_sm
from spacy import displacy                    
                            
import pandas as pd
import pprint
pp = pprint.PrettyPrinter(2)

from scispacy.abbreviation import AbbreviationDetector


def explore__text_byScispacy(text=None):
    global pp
    
    if text is None:
        text = "Spinal and bulbar muscular atrophy (SBMA) is an \
                   inherited motor neuron disease caused by the expansion \
                   of a polyglutamine tract within the androgen receptor (AR). \
                   SBMA can be caused by this easily."
               
               
    print('Input text:')
    pp.pprint(text)
    print('- load model: en_core_sci_sm')
    nlp = en_core_sci_sm.load()
    doc = nlp(text)
    print("- returned object type: <class 'spacy.tokens.doc.Doc'>")
    print(type(doc)) 
    # print(list(doc.sents))
    
    print('nb entities:', len(doc.ents))
    for x in doc.ents:
        print(str(x))
    ent_bc = {}
    for x in doc.ents: 
        ent_bc[x.text] = x.label_
    pp.pprint(ent_bc)
    # trans_df = pd.DataFrame(table)    

    # Add the abbreviation pipe to the spacy pipeline.
    abbreviation_pipe = AbbreviationDetector(nlp)
    nlp.add_pipe(abbreviation_pipe)
    print("Abbreviations FOUND", "\t", "Definition")
    doc = nlp(text)
    for abrv in doc._.abbreviations:
    	print(f"{abrv} \t ({abrv.start}, {abrv.end}) {abrv._.long_form}")
        
    displacy_image = displacy.render(doc, jupyter = True, style = 'ent') 
    print(displacy_image)                             

'''
nlp_cr = en_ner_craft_md.load()
import en_ner_bc5cdr_md
nlp_bc = en_ner_bc5cdr_md.load()
nlp_bi = en_ner_bionlp13cg_md.load()
nlp_jn = en_ner_jnlpba_md.load()

table= {'doi':[], 'Entity':[], 'Class':[]}
doc = nlp_bc(text)
ent_bc = {}
for x in doc.ents:
    ent_bc[x.text] = x.label_
for key in ent_bc:
    table['doi'].append(doi)
    table['Entity'].append(key)
    table['Class'].append(ent_bc[key])
trans_df = pd.DataFrame(table)    
'''
