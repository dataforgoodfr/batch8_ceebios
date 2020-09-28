

import wikipedia
import webbrowser
import bs4 as bs



class BiologyWikipediaBot:
    def __init__(self,lang = "fr"):

        # Set language for future search
        wikipedia.set_lang(lang)
        print(f"[INFO] Wikipedia bot initialized in {lang.upper()}")


    def search_pages(self,query,return_pages = True,results = 5,category = None,best_match = False):

        page_names = wikipedia.search(query,results = results)

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


    def search_biology_page(self,query,results = 5):

        # Warning harcoded french parameter
        category = "biologie"

        # Search using wikipedia API
        page = self.search_pages(query,results = results,category = category,best_match = True,return_pages = True)
        return page









class WikipediaPage(wikipedia.WikipediaPage):

    ATTRS = ["categories","content","summary","images","links","original_title","pageid","parentid","references","summary","url"]


    def get_categories(self):
        cats = self.categories
        cats = [cat.rsplit(":",1)[-1] for cat in cats]
        return cats


    def has_category_like(self,query):
        return query.lower() in "|".join(self.get_categories()).lower()


    def get_latin_name(self):
        """
        References
        - Installing pycld2
            - https://pypi.org/project/pycld2/
            - https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycld2
        - Polyglot (does not work on windows)
            - https://polyglot.readthedocs.io/en/latest/Installation.html
        """

        pass

    def open(self):
        webbrowser.open(self.url)



    def explore(self):

        for attribute in self.ATTRS:
            if not attribute.startswith("_"):
                try:
                    print("-"*3,attribute,"-"*50)
                    content = getattr(self,attribute)
                    print(attribute)
                    if isinstance(content,str):
                        print(content[:500])
                    else:
                        print(content)
                    print("")
                except Exception as e:
                    print(f"-- Skipped attribute {attribute} because of {e}")


    def to_dict(self):
        
        return {a:getattr(self,a) for a in self.ATTRS}

