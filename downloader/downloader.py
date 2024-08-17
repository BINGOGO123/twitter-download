from abc import abstractmethod
from .data_strategy import DataStrategy

class Downloader:
    def __init__(self):
        pass

        
    @abstractmethod
    def get_tw_response_json_by_url(self, url: str, params = None, **kwargs) -> dict:
        pass
    
    
    @abstractmethod
    def get_tw_response_bytes_by_url(self, url: str, params = None, **kwargs) -> bytes:
        pass
    
    
    @abstractmethod
    def download_file(self, file_name: str, url: str, params = None, data_strategy: DataStrategy = None, **kwargs) -> str:
        pass