from abc import abstractmethod

class Saver:
    def __init__(self):
        pass
    
    
    @abstractmethod
    def save(self, pointer: dict, target_dir: str) -> str:
        """将指定pointer信息保存到target_dir中，返回保存后的完整路径

        Args:
            pointer (dict): 待保存的信息
            target_dir (str): 目标目录名称

        Returns:
            str: 信息保存的完整路径
        """
        pass