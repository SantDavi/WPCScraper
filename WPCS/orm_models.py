from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, BLOB, String, DateTime
from sqlalchemy.sql import func
from hashlib import md5

import requests
import pickle

# Base class for ORM models
Base = declarative_base()

# Define the Response model
class Response(Base):
    __tablename__ = 'response'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    response = Column(BLOB, nullable=False)  # binary dump of (requests.models.Response) type
    response_content_hash = Column(String, nullable=False)  # Store the hash of the content
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, url: str, response: requests.models.Response):
        self.url = url
        self.response = pickle.dumps(response)
        self.response_content_hash = str(md5(response.content).hexdigest())  # Generate hash for the content

    def __repr__(self):
        return f"<Response(hash:md5:{self.response_content_hash})>"
