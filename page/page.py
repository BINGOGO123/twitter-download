from abc import abstractmethod

class Page:
    def __init__(self):
        pass
    
    
    @abstractmethod
    def get_info(self, *args) -> dict:
        pass
