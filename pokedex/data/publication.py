from enum import Enum


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
    def __init__(self):
        pass


    @classmethod
    def from_scholar(cls,data):
        pub = Publication()
        # Be sure we have the journal
        # name
        data.fill()
        pub.data = data
        bib = data.bib
        pub.title = bib.get("title")
        pub.abstract = bib.get("abstract")
        pub.author = bib.get("author")
        pub.url = bib.get("url")
        pub.journal = bib.get("journal")
        pub.cites = bib.get("cites")
        pub.year = bib.get("year")
        pub.doi = None
        return pub

    @classmethod
    def from_coreac(cls, data):
        pub = Publication()
        pub.data = data
        pub.title = data.get("title")
        pub.abstract = data.get("description")
        pub.author = data.get("authors")
        pub.url = data.get("downloadUrl")
        pub.journal = data.get("publisher")
        pub.cites = data.get("citations")
        pub.year = data.get("year")
        pub.doi = data.get("doi")
        return pub

    def to_dict(self):
        return {x : getattr(self,x) for x in DATA_MODEL}

    def __repr__(self):
        return f"Publication(title={self.title})"
    