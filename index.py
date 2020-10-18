import streamlit as st
import numpy as np
import pandas as pd


from pokedex.data import GBIFExtractor
from pokedex.data import load_scimagojrdb

scimagojrdb = load_scimagojrdb()

# Fuzzy search for all species 
st.sidebar.image("app/img/logo-ceebios.png",use_column_width = True)
st.sidebar.markdown("# Ceebios Pokedex")
st.sidebar.markdown("## Taxon finder (latin names)")
query = st.sidebar.text_input("Search species")

if query != "":
    gbif = GBIFExtractor()
    species = gbif.search(query)
    species = "\n".join([f"- {x.name}" for x in species])
    st.sidebar.info(species)


# Exact search
species_str = st.text_input("Enter latin name")

if species_str != "":

    gbif = GBIFExtractor()
    species = gbif.match(species_str)

    st.markdown(f"# {species_str.title()}")


    st.markdown(f"## Species information")

    try:
        img_url = species.get_wikipedia_image()
        st.image(img_url,width = 200)
        st.info(species.get_wikipedia_description()[:500] + " ...")
        st.success(f"Learn more on [wikipedia page]({species.wikipedia_page.url})")
    except:
        st.error(f"Impossible to find information on Wikipedia for species {species_str}")


    st.markdown(f"## Searching scientific publications")
    n_pubs = st.slider("Number of publications",min_value = 1,max_value = 100,value = 5)
    source = st.selectbox('Data source',('coreac', 'google'))
    pubs = species.search_publications(n = n_pubs,as_df = False,source = source)

    for pub in pubs:

        info = f"""#### [{pub.title}]({pub.url})\n{pub.abstract}\n*{pub.year} - {pub.author}*"""
        
        # append the journal name and categories
        if pub.journal:
            info += f'\n\n {pub.journal}'
            categories = scimagojrdb.find_categories(pub.journal)
            if categories:
                info += f' ({",".join(categories)})'
            
        st.info(info)

        # st.write(pubs["title"].tolist())
        # st.write(pubs.drop(columns = ["abstract"]).to_dict(orient = "records"))



