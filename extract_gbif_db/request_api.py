import requests
import time
from json.decoder import JSONDecodeError
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed


CHUNK_SIZE = 1000
LIMIT = int(6.6e6)  # 6 586 578 differents species referenced on gbif.org


def request_api(offset):
    """request gbif API to get 1 specy. see: https://www.gbif.org/developer/summary (section Page)"""
    # url = "https://api.gbif.org/v1/species/?offset={offset}&limit={limit}".format(
    #     offset=offset, limit=CHUNK_SIZE
    # )
    url = "https://api.gbif.org/v1/species/"
    payload = {'offset': offset, 'limit': CHUNK_SIZE}
    try:
        r = requests.get(url, params=payload)
        data = r.json()
        results = data.get("results")
        return results
    except JSONDecodeError:
        return {}


def fetch_data(nb_workers=30):
    data = []
    with ThreadPoolExecutor(max_workers=nb_workers) as executor:
        future_to_request = {
            executor.submit(request_api, offset)
            for offset in range(0, LIMIT + CHUNK_SIZE, CHUNK_SIZE)
        }
        for future in tqdm(as_completed(future_to_request)):
            fetched_data = future.result()
            data.extend(fetched_data)
    print("#### saving extract ####")
    df = pd.DataFrame(data)
    df.to_csv("gbif_extract.csv")


if __name__ == "__main__":
    print("### fetching api.gbif.org ###")
    start = time.time()
    fetch_data()
    print("--- wall time : {:.2f} s ---".format(time.time() - start))
