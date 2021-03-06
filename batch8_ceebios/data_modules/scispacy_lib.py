# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 19:10:35 2020

@author: CHRISTIAN
"""

"""
!pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.2.4/en_core_sci_sm-0.2.4.tar.gz --user
"""

import pprint
import time

import en_core_sci_sm
import pandas as pd
from spacy import displacy

pp = pprint.PrettyPrinter(2)

from scispacy.abbreviation import AbbreviationDetector

from flashtext import KeywordProcessor

if False:  # local desktop working
    os.chdir("D:/ecomdataforgoodfr/Ceebios/batch8_ceebios/base_open_source")
    print(os.getcwd())

df_canonicalName = None
nlpbif = None


# flashtext: Span of keywords extracted


def test_flashtext():
    keyword_processor = KeywordProcessor()
    keyword_processor.add_keyword("Big Apple", "New York")
    keyword_processor.add_keyword("Bay Area")
    keywords_found = keyword_processor.extract_keywords(
        "I love big Apple and Bay Area.", span_info=True
    )
    print(keywords_found)


def load_gbif_categories(gbif_extract_file="../data/gbif_extract_categories.csv"):
    """ load gbif categies dataset """
    """ input: csv file name """
    """ ourput: fleshtext keyword_processor """

    df_canonicalName = pd.read_csv(gbif_extract_file, sep=";")
    print(
        gbif_extract_file,
        ", loaded",
        df_canonicalName.shape,
        list(df_canonicalName.columns),
    )
    kwords = list(df_canonicalName["name"].values)
    keyword_processor = KeywordProcessor()
    for k in kwords:
        tab = k.split(" ")
        for y in tab:
            if len(y) > 0:
                keyword_processor.add_keyword(y)
    print("len(keyword_processor):", len(keyword_processor))

    # ['family' 'genus' 'species' 'subspecies']
    print(df_canonicalName["rank"].unique())
    return keyword_processor


keyprocessor = None
nlpbif = None


def search_canonicalNameFlesh(text=None):
    global keyprocessor
    global nlpbif

    resp = []
    if keyprocessor is None or text is None:
        keyprocessor = load_gbif_categories()
        nlpbif = en_core_sci_sm.load()
        print("- Keyprocessor and nlp, loaded")

    if text is not None:
        doc = nlpbif(text)
        print("nb entities:", len(doc.ents))
        data = []
        for x in doc.ents:
            x = str(x).lower()
            tab = x.split(" ")
            for y in tab:
                if len(y) > 0:
                    data.append(y)
        keywords_found = keyprocessor.extract_keywords(" ".join(data), span_info=True)
        if (len(keywords_found)) > 0:
            for k in keywords_found:  # ('pterocladiophilaceae', 735, 755)]
                if k[0] not in resp:
                    resp.append(k[0])
    return resp


def test_search_canonicalNameFlesh():
    text = "Distribution and movement patterns of Antarctic blue whales Balaenoptera \
        musculus intermedia at large temporal and spatial scales are still \
        poorly understood. The objective of this study was \
        to explore spatio-temporal distribution patterns of\
        Antarctic blue whales in the Atlantic sector of the Southern Ocean,\
        using passive acoustic monitoring data. Multi-year dat\
        a were collected between 2008 and 2013 by\
        11 recorders deployed in the Weddell Sea and along \
        the Greenwich meridian. \
        Antarctic blue whale Z-calls were detected via spectrogram cross-correlation.\
        A Blue Whale Index was developed to quantify the proportion of time \
        during which acoustic energy from Antarctic blue whales dominated\
        over background noise. Our results show that Antarctic \
        blue whales were acoustically present year-round, \
        with most call detections between January and April.\
        During austral summer, the number of detected calls \
        peaked synchronously throughout the study area in most\
        years, and hence, no directed meridional movement \
        pattern was detectable. During austral winter,\
        vocalizations were recorded at latitudes \
        as high as 69°S, with sea ice cover exceeding 90%,\
        suggesting that some Antarctic blue whales overwinter\
        in Antarctic waters. Polynyas likely \
        serve as an important habitat for baleen whales during\
        austral winter, providing food and reliable access \
        to open water for breathing. Overall, our results \
        support increasing evidence of a complex \
        and non-obligatory migratory behavior of Antarctic blue whales,\
        potentially involving temporally and spatially dynamic \
        migration routes and destinations, as well as variable \
        timing of migration to and from the feeding grounds."

    print("Test1, with first load:")
    ts = time.time()
    text = text.replace("whales", " pterocladiophilaceae")
    resp = search_canonicalNameFlesh(text)
    print("response time:", time.time() - ts)
    print(resp)

    print("Test2, same initial load already made:")
    ts = time.time()
    resp = search_canonicalNameFlesh(text)
    print("response time:", time.time() - ts)
    print(resp)


def search_canonicalName(
    text=None, gbif_extract_file="../data/gbif_extract_canonicalName_short.csv"
):
    """ search on gbif canonical names """
    global df_canonicalName, nlpbif
    if df_canonicalName is None or text is None:
        df_canonicalName = pd.read_csv(gbif_extract_file, sep=";")
        print(
            gbif_extract_file,
            ", loaded",
            df_canonicalName.shape,
            list(df_canonicalName.columns),
        )
        print(df_canonicalName.shape)
        nlpbif = en_core_sci_sm.load()

    if text is not None and df_canonicalName is not None:
        resp = []
        doc = nlpbif(text)
        print("nb entities:", len(doc.ents))
        for x in doc.ents:
            # print(x)
            tabw = str(x).lower().split(" ")
            for w in tabw:
                print(x, "-", w)
                df = df_canonicalName[df_canonicalName["canonicalName_word"] == w]
                # print(df)
                if len(df) > 0:
                    resp.append({"name": w, "key": df["tab_key"].values[0]})
        return resp
    return


def explore__text_byScispacy(text=None):
    global pp

    if text is None:
        text = "Spinal and bulbar muscular atrophy (SBMA) is an \
                   inherited motor neuron disease caused by the expansion \
                   of a polyglutamine tract within the androgen receptor (AR). \
                   SBMA can be caused by this easily."

    text = "Passive acoustic monitoring is an efficient way to provide insights \
            on the ecology of large whales. This approach allows for long-term and \
            species-specific monitoring over large areas. In this study, \
            we examined six years (2010 to 2015) of continuous acoustic \
            recordings at up to seven different locations in the Central and Southern Indian Basin to assess the peak periods of presence, seasonality and migration movements of Antarctic blue whales (Balaenoptera musculus intermedia). An automated method is used to detect the Antarctic blue whale stereotyped call, known as Z-call. Detection results are analyzed in terms of distribution, seasonal presence and diel pattern of emission at each site. Z-calls are detected year-round at each site, except for one located in the equatorial Indian Ocean, and display highly seasonal distribution. This seasonality is stable across years for every site, but varies between sites. Z-calls are mainly detected during autumn and spring at the subantarctic locations, suggesting that these sites are on the Antarctic blue whale migration routes, and mostly during winter at the subtropical sites. In addition to these seasonal trends, there is a significant diel pattern in Z-call emission, with more Z-calls in daytime than in nighttime. This diel pattern may be related to the blue whale feeding ecology."

    text = "Distribution and movement patterns of Antarctic blue whales Balaenoptera \
        musculus intermedia at large temporal and spatial scales are still \
        poorly understood. The objective of this study was \
        to explore spatio-temporal distribution patterns of\
        Antarctic blue whales in the Atlantic sector of the Southern Ocean,\
        using passive acoustic monitoring data. Multi-year dat\
        a were collected between 2008 and 2013 by\
        11 recorders deployed in the Weddell Sea and along \
        the Greenwich meridian. \
        Antarctic blue whale Z-calls were detected via spectrogram cross-correlation.\
        A Blue Whale Index was developed to quantify the proportion of time \
        during which acoustic energy from Antarctic blue whales dominated\
        over background noise. Our results show that Antarctic \
        blue whales were acoustically present year-round, \
        with most call detections between January and April.\
        During austral summer, the number of detected calls \
        peaked synchronously throughout the study area in most\
        years, and hence, no directed meridional movement \
        pattern was detectable. During austral winter,\
        vocalizations were recorded at latitudes \
        as high as 69°S, with sea ice cover exceeding 90%,\
        suggesting that some Antarctic blue whales overwinter\
        in Antarctic waters. Polynyas likely \
        serve as an important habitat for baleen whales during\
        austral winter, providing food and reliable access \
        to open water for breathing. Overall, our results \
        support increasing evidence of a complex \
        and non-obligatory migratory behavior of Antarctic blue whales,\
        potentially involving temporally and spatially dynamic \
        migration routes and destinations, as well as variable \
        timing of migration to and from the feeding grounds."
    print("Input text:")
    pp.pprint(text)
    print("- load model: en_core_sci_sm")
    nlp = en_core_sci_sm.load()
    ts = time.time()
    doc = nlp(text)
    print(time.time() - ts)
    print("- returned object type: <class 'spacy.tokens.doc.Doc'>")
    print(type(doc))
    # print(list(doc.sents))

    print("nb entities:", len(doc.ents))
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
    ts = time.time()
    doc = nlp(text)
    print(time.time() - ts)
    for abrv in doc._.abbreviations:
        print(f"{abrv} \t ({abrv.start}, {abrv.end}) {abrv._.long_form}")

    displacy_image = displacy.render(doc, jupyter=True, style="ent")
    print(displacy_image)


"""
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
"""
