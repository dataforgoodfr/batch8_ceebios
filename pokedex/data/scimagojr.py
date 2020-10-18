import pandas as pd

def load_scimagojrdb():
    if ScimagojrDB.instance:
        return ScimagojrDB.instance
    return ScimagojrDB('scimagojr2019.csv')

class ScimagojrDB():
    instance = None

    def __init__(self, db_path):
        self.df = pd.read_csv(db_path, sep=';')

    def find_categories(self, journal):
        """
        """
        if not journal:
            return []
        journals = self.df.loc[self.df.Title.str.lower().str.contains(journal.lower())]

        # When we have a multiple results we pick the first
        # one with the biggest SJR
        journals.sort_values('SJR', ascending=False, inplace=True)

        try:
            categories = journals.iloc[0].Categories
            return [category[:-4] for category in categories.split(';')]
        except IndexError:
            return None

    