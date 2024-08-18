from abc import abstractmethod

class Gallary:
    def __init__(self):
        pass
    
    
    @abstractmethod
    def generate(self, source_dir_list: list[str], target_dir: str, title: str) -> str:
        pass
