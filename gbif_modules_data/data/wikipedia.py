import wikipedia
import webbrowser
import bs4 as bs
import time
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed


class WikipediaError(Exception):
    pass


def get_wikipedia_summary(query):
    try:
        summary = wikipedia.summary(query, redirect=True, auto_suggest=False)
        return query, summary
    except wikipedia.exceptions.PageError as e:
        return query, None


def main(nb_workers=4):
    data = pd.read_csv(
        r"C:\Users\tonth\Documents\ceebios\GBIF\gbif_extract.csv",
        usecols=["scientificName", "canonicalName"],
    )
    species = data.canonicalName.unique().tolist()

    summaries = []
    with ThreadPoolExecutor(max_workers=nb_workers) as executor:
        future_to_summary = {
            executor.submit(get_wikipedia_summary, query) for query in species
        }
        for future in tqdm(as_completed(future_to_summary)):
            fetched_data = future.result()
            summaries.append(fetched_data)
    print("#### saving extract ####")
    df = pd.DataFrame(summaries, columns=["name", "summary"])
    df.to_csv("summaries_1.csv")


# if __name__ == "__main__":
#     print("### extracting wikipedia's summaries ###")
#     start = time.time()
#     main(nb_workers=16)
#     print("--- wall time : {:.2f} s ---".format(time.time() - start))


class WikipediaExtractor:
    def __init__(self, lang="fr"):

        # Set language for future search
        wikipedia.set_lang(lang)
        # print(f"[INFO] Wikipedia bot initialized in {lang.upper()}")

    def search_pages(
        self, query, return_pages=True, results=5, category=None, best_match=False
    ):

        page_names = wikipedia.search(query, results=results)

        if return_pages:

            if category is not None:

                if best_match:
                    for page in page_names:
                        page = WikipediaPage(page)
                        if page.has_category_like(category):
                            return page
                    return None

                else:
                    pages = []
                    for page in page_names:
                        page = WikipediaPage(page)
                        if page.has_category_like(category):
                            pages.append(page)

            else:

                if best_match:
                    return WikipediaPage(page_names[0])
                else:
                    return [WikipediaPage(page) for page in page_names]
        else:
            if best_match:
                return page_names[0]
            else:
                return page_names

    def search_biology_page(self, query, results=5):

        # Warning harcoded french parameter
        category = "biologie"

        # Search using wikipedia API
        page = self.search_pages(
            query,
            results=results,
            category=category,
            best_match=True,
            return_pages=True,
        )
        return page


class WikipediaPage(wikipedia.WikipediaPage):

    ATTRS = [
        "categories",
        "content",
        "summary",
        "images",
        "links",
        "original_title",
        "pageid",
        "parentid",
        "references",
        "summary",
        "url",
    ]

    def get_categories(self, as_string=False):
        cats = self.categories
        cats = [cat.rsplit(":", 1)[-1] for cat in cats]

        if as_string:
            return "|".join(cats)
        else:
            return cats

    def has_category_like(self, query):
        return query.lower() in self.get_categories(as_string=True).lower()

    def get_description(self):
        return self.content

    def get_beautifulsoup_page(self, html):
        return bs.BeautifulSoup(html, "lxml")

    def get_species_image(self, as_img=False, thumbnail=True):
        page = self.get_beautifulsoup_page(self.html())

        image_url = (
            "https:" + page.find("div", class_="images").find("img").attrs["src"]
        )
        if thumbnail == False:
            image_url = image_url.replace("/thumb/", "/").rsplit("/", 1)[0]

        if as_img:
            r = requests.get(image_url)
            img = Image.open(BytesIO(r.content), "r")
            return img
        else:
            return image_url

    def is_species(self):

        # Warning check if it works for other species than animals
        # Hardcoded category info
        taxobox = "taxobox-animal"

        return taxobox in self.get_categories(as_string=True).lower()

    def open(self):
        webbrowser.open(self.url)

    def explore(self):

        for attribute in self.ATTRS:
            if not attribute.startswith("_"):
                try:
                    print("-" * 3, attribute, "-" * 50)
                    content = getattr(self, attribute)
                    print(attribute)
                    if isinstance(content, str):
                        print(content[:500])
                    else:
                        print(content)
                    print("")
                except Exception as e:
                    print(f"-- Skipped attribute {attribute} because of {e}")

    def to_dict(self):

        return {a: getattr(self, a) for a in self.ATTRS}
