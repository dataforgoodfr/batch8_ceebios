
import requests
import pandas as pd

# from .gbif import BASE_GBIF_URL
from .wikipedia import WikipediaExtractor,WikipediaError
from .scholar import GoogleScholarExtractor



EXAMPLE_SPECIES = [
    "Vespa Ducalis",
    "Balaenoptera musculus",
]


class Species:
    def __init__(self,data):
        self._data = data


    @property
    def name(self):
        return self.data["species"]
    

    @property
    def data(self):
        return self._data


    @property
    def vernacular_names(self):
        return self.data["vernacularNames"]
    

    @property
    def key(self):
        if "nubKey" in self.data:
            return self.data["nubKey"]
        else:
            return self.data["speciesKey"]


    @property
    def info(self):
        return {x:self.data[x] for x in ["kingdom","phylum","order","genus","species"]}

    def __repr__(self):
        return f"Species(name={self.name})"


    def search_publications(self,n = 5,as_df = True):
        scholar = GoogleScholarExtractor()
        publications = scholar.search(self.name,n = n)

        if as_df:
            return pd.DataFrame([x.to_dict() for x in publications])
        else:
            return publications


    def fetch_description(self):
        # Deprecated
        url = f"{BASE_GBIF_URL}/{self.key}/descriptions"
        r = requests.get(url).json()
        return r


    def fetch_wikipedia_page(self,lang = "fr"):

        if not hasattr(self,"wikipedia_page") or (hasattr(self,"wikipedia_page_lang") and self.wikipedia_page_lang != lang):

            wiki =  WikipediaExtractor(lang = lang)
            page = wiki.search_biology_page(self.name)
            if page.is_species(): #and page.title.lower() == self.name.lower():
                self.wikipedia_page = page
                self.wikpedia_page_lang = lang
            else:
                raise WikipediaError(f"Did not found perfect match on Wikipedia for species {self.name}")


    def open_wikipedia(self):
        self.fetch_wikipedia_page()
        self.wikipedia_page.open()


    def get_wikipedia_description(self):
        self.fetch_wikipedia_page()
        return self.wikipedia_page.content

    def get_wikipedia_image(self,as_img = False):
        self.fetch_wikipedia_page()
        img = self.wikipedia_page.get_species_image(as_img = as_img)
        return img





    
