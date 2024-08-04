from abc import abstractmethod

class Downloader:
    def __init__(self):
        pass

        
    @abstractmethod
    def get_tw_response_json_by_url(self, url: str, params = None, **kwargs) -> dict:
        pass
    
    
    @abstractmethod
    def get_tw_response_bytes_by_url(self, url: str, params = None, **kwargs) -> bytes:
        pass