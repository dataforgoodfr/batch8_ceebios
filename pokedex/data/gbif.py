import requests
import time
import pandas as pd
import urllib.parse
from tqdm import tqdm,tqdm_notebook
from concurrent.futures import ThreadPoolExecutor, as_completed
from json.decoder import JSONDecodeError


from .species import Species
from .species_list import SpeciesList



"""
TODO 
- Get all species from a given class or kingdom
- Wrapper with visualizations for group of species
- Get list of values for sub hierarchies for easy search 
"""



CHUNK_SIZE = 1000
LIMIT = int(6.6e6)  # 6 586 578 differents species referenced on gbif.org
BASE_GBIF_URL = "https://api.gbif.org/v1/species/"


class GBIFError(Exception):
    pass



class GBIFExtractor:
    def __init__(self):
        """Wrapper to extract data from GBIF API
        Documentation for the core API here https://www.gbif.org/developer/species
        """
        pass


    def match(self,query,as_json = False):

        endpoint = f"/match?name={urllib.parse.quote(query)}"
        r = self.fetch_page(endpoint,no_payload = True)

        if r["matchType"] == "NONE":
            raise GBIFError(f"No species found on GBIF with name: '{query}'")
        else:
            if as_json:
                return r
            else:
                return Species(data = r)


    def search(self,query,as_json = False,drop_duplicates = True,limit = 1000):

        endpoint = f"/search?q={urllib.parse.quote(query)}&rank=SPECIES&limit={limit}"
        r = self.fetch_page(endpoint,no_payload = True)

        if r["count"] == 0:
            raise GBIFError(f"No search results found on GBIF with query: '{query}'")
        else:
            if as_json:
                return r
            else:

                results = r["results"]

                if drop_duplicates:
                    species = []
                    seen = []
                    for result in results:
                        s = result["species"]
                        if s not in seen:
                            seen.append(s)
                            species.append(result)
                else:
                    species = results

                species = [Species(data = x) for x in species]
                return species


    def fetch_all_children(self,key):

        parent = self.fetch_page(endpoint = key)
        n_results = parent["numDescendants"] # Not sure to use the numDescendants as it refers to all species ?
        n_results = None
        data = self.fetch(endpoint = f"{key}/children",n_results = n_results)
        return data



    def fetch(self,endpoint,n_results = None,n_workers = 8,limit = 1000):
        data = []

        # When number of results is not known 
        # Iterate till there is no page left
        if n_results is None:

            pbar = tqdm_notebook()
            offset = 0
            results = self.fetch_page(endpoint,offset = offset)
            done = results["endOfRecords"]
            data.extend(results["results"])
            while done == False:
                offset += limit
                results = self.fetch_page(endpoint,offset = offset)
                done = results["endOfRecords"]
                data.extend(results["results"])
                pbar.update(offset)

        # If number of results is known we can use parallelism
        else:

            with ThreadPoolExecutor(max_workers=n_workers) as executor:
                future_to_request = {
                    executor.submit(self.fetch_page,endpoint,offset)
                    for offset in range(0, limit + n_results, n_results)
                }
                for future in tqdm(as_completed(future_to_request)):
                    fetched_data = future.result()
                    data.extend(fetched_data["results"])


        df = SpeciesList(data)
        return df


    def fetch_page(self,endpoint,offset = 0,no_payload = False):
        """request gbif API to get 1 specy. see: https://www.gbif.org/developer/summary (section Page)"""
        # url = "https://api.gbif.org/v1/species/?offset={offset}&limit={limit}".format(
        #     offset=offset, limit=CHUNK_SIZE
        # )

        url = urllib.parse.urljoin(BASE_GBIF_URL,str(endpoint).strip("/"))
        payload = {'offset': offset, 'limit': CHUNK_SIZE}
        try:
            if no_payload:
                r = requests.get(url)
            else:
                r = requests.get(url, params=payload)
            data = r.json()
            return data
        except JSONDecodeError:
            return {}





# if __name__ == "__main__":
#     print("### fetching api.gbif.org ###")
#     start = time.time()
#     fetch_data()
#     print("--- wall time : {:.2f} s ---".format(time.time() - start))
