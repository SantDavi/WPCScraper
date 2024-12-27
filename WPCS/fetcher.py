from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .orm_models import Response as ResponseORMModel, Base
import pickle
from hashlib import md5
import sys

# Database setup
DATABASE_URL = "sqlite:///_responses.db"  # Replace with your database URL

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)  # Create tables if they don't exist
Session = sessionmaker(bind=engine)

class WPCSFetcher:
    def __init__(self, urls, req_method, cache_timeout=None, check_update_rate=None):
        """
        A web content fetching system (WPCS) that interacts with URLs
        and stores or processes their responses using SQLAlchemy.
        """
        self._urls = urls
        self.__req = req_method
        self._generators = []
        self._data = {}
        self._idx = 0
        self._session = Session()  # Initialize a database session

    def fetch_url_content(self, url):
        """
        Fetch the content of a URL and store it in the database.
        """

        #query
        existing_response = (
            self._session.query(ResponseORMModel).filter_by(url=url).first()
        )

        if existing_response:
            response = pickle.loads(existing_response.response)
        else:
            response = self.__req(url)
            orm = ResponseORMModel(url=url, response=response)
            
            self._session.add(orm)
            self._session.commit()

        return response

    def apply(self, fn):
        """
        Apply a function to the content of each URL and generate results.
        """
        for self.__url in self._urls:
            response = self.fetch_url_content(self.__url)
            generator = fn(response)
            self._generators.append(generator)
        return self

    def iter_urls(self, fn):
        """
        Iterate through the generated content and apply a function to extract new URLs.
        """
        self._urls = []
        results = []

        for generator in self._generators:
            for result in generator:
                url = fn(result)
                self._urls.append(url)
                results.append(result)
        
        self._data[self._idx] = results
        self._idx += 1
        return self
    

    def dump_data(self):
        self._urls = []
        results = []

        for generator in self._generators:
            for result in generator:
                results.append(result)
        
        self._data[self._idx] = results
        return self._data