from abc import abstractmethod

class Parser:
    def __init__(self):
        pass
    
    
    @abstractmethod
    def parse(response: dict):
        pass