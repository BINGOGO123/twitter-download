from abc import abstractmethod
from .media import Media

class DataManager:
    def __init__(self):
        pass
    
    
    @abstractmethod
    def get_data_info_by_url(self, url: str) -> list[Media]:
        pass
    
    
    @abstractmethod
    def insert_data(self, media: Media):
        pass
    
    
    @abstractmethod
    def get_all_data(self) -> list[Media]:
        pass
