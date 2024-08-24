from .parser import Parser
from abc import abstractmethod

class AbstractParser(Parser):
    
    def parse(self, response: dict) -> list:
        entries = self.get_entries_from_response(response)
        return self.get_entry_info_list_from_entries(entries)
        
    
    
    @abstractmethod
    def get_entries_from_response(self, response: dict) -> list:
        pass
    
    
    @abstractmethod
    def get_entry_info_list_from_entries(entries: list) -> list:
        pass
