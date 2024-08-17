from abc import abstractmethod

class DataStrategy:
    def __init__(self):
        pass
    
    
    @abstractmethod
    def execute(self, data: bytes):
        pass
    
    
    @abstractmethod
    def get_result(self):
        pass