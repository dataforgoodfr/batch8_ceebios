


DATA_MODEL = [
    "title",
    "abstract",
    "author",
    "url",
    "doi",
    "journal",
    "cites",
    "year",
]


class Publication:
    def __init__(self,scholar_data = None):

        if scholar_data is not None:
            self.load_from_scholar(scholar_data)

    def load_from_scholar(self,data):
        self._data = data
        bib = data.bib
        self.title = bib.get("title")
        self.abstract = bib.get("abstract")
        self.author = bib.get("author")
        self.url = bib.get("url")
        self.journal = bib.get("journal")
        self.cites = bib.get("cites")
        self.year = bib.get("year")
        self.doi = None

    def to_dict(self):
        return {x : getattr(self,x) for x in DATA_MODEL}

    def __repr__(self):
        return f"Publication(title={self.title})"
    