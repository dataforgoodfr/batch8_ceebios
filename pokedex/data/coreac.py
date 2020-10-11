import requests
import urllib

from .publication import Publication

CORE_API = 'https://core.ac.uk:443/api-v2'
API_KEY="cJmoVEila3gB0zCIM2q1vpZnsKjr9XdG"

class CoreACExtractor:
    def __init__(self):
        pass

    def search(self, query, n=5):
        params = {
            'page':1,
            'pageSize':n,
            'apiKey':API_KEY,
            'citations':'true'
        }
        core_query = ' '.join((urllib.parse.quote(query), 'biomimetism'))
        search_url = '/'.join((CORE_API, 'articles', 'search', core_query))
        response = requests.get(search_url, params).json()
        
        return [Publication.from_coreac(pub) for pub in response['data'] ]