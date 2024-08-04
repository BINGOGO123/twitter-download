from .common_page import AbstractPage
from tool.decorators import LoggerWrapper
from . import logger
from abc import abstractmethod

class AbstractSinglePage(AbstractPage):
    @LoggerWrapper(logger)
    def get_info(self, *args) -> dict:
        try:
            # 根据参数生成url
            url = self.get_url(*args)
            # 通过url获取json内容
            data = self.downloader.get_tw_response_json_by_url(url)
            # 解析json内容
            result = self.parse_response_info(data)
            return result
        except Exception as ex:
            logger.exception(ex)
            return {}

        
    @abstractmethod
    def get_url(self, *args) -> str:
        pass
    
    
    @abstractmethod
    def parse_response_info(self, data: dict) -> dict:
        pass
        
