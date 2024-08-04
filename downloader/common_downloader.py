from .downloader import Downloader
from . import logger
from . import module_config
from tool.decorators import LoggerWrapper
import requests
from tool.tool import cover
import copy

class CommonDownloader(Downloader):
    def __init__(self, **kwargs):
        """初始化
        Args:
            request_max_count(int): 请求最大次数
        """
        self.default_requests_kwargs = kwargs.get("requests_kwargs", module_config.get("requests_kwargs"))
        self.request_max_count = kwargs.get("request_max_count", module_config.get("request_max_count"))
        

    def get_tw_response_by_url(self, url: str, params = None, **kwargs) -> requests.Response:
        requests_kwargs = copy.deepcopy(self.default_requests_kwargs)
        cover(requests_kwargs, kwargs)
        counter = 1
        while True:
            try:
                response = requests.get(url, params, **requests_kwargs)
                response.raise_for_status()
                return response
            # 这里不会捕获KeyboardInterrupt
            except Exception:
                logger.exception("第{}次失败".format(counter))
                if counter >= self.request_max_count:
                    logger.error("达到失败次数上限{}".format(counter))
                    return None
                counter += 1


    @LoggerWrapper(logger)
    def get_tw_response_json_by_url(self, url: str, params = None, **kwargs) -> dict:
        response = self.get_tw_response_by_url(url, params, **kwargs)
        return response.json() if response != None else {}


    @LoggerWrapper(logger)
    def get_tw_response_bytes_by_url(self, url: str, params = None, **kwargs) -> bytes:
        response = self.get_tw_response_by_url(url, params, **kwargs)
        return response.content if response != None else bytes()
