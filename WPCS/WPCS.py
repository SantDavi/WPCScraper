
from .fetcher import WPCSFetcher

class WPCS:
    def __init__(self):
        pass

    def get_page_content(self, initial_urls, req_method):
        return WPCSFetcher(initial_urls, req_method)

