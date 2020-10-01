import wikipedia
import time
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_wikipedia_summary(query):
    try:
        summary = wikipedia.summary(query, redirect=True, auto_suggest=False)
        return query, summary
    except wikipedia.exceptions.PageError as e:
        return query, None

def main(nb_workers=4):
    data = pd.read_csv(
            r'C:\Users\tonth\Documents\ceebios\GBIF\gbif_extract.csv',
            usecols=['scientificName', 'canonicalName']
        )
    species = data.canonicalName.unique().tolist()

    summaries = []
    with ThreadPoolExecutor(max_workers=nb_workers) as executor:
        future_to_summary = {
            executor.submit(get_wikipedia_summary, query)
            for query in species
        }
        for future in tqdm(as_completed(future_to_summary)):
            fetched_data = future.result()
            summaries.append(fetched_data)
    print("#### saving extract ####")
    df = pd.DataFrame(summaries, columns = ['name','summary'])
    df.to_csv("summaries_1.csv")



if __name__ == "__main__":
    print("### extracting wikipedia's summaries ###")
    start = time.time()
    main(nb_workers=16)
    print("--- wall time : {:.2f} s ---".format(time.time() - start))




