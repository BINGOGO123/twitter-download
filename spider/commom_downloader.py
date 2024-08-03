
from .import module_config
from .import logger
from tool.decorators import LoggerWrapper
import requests
from .downloader import Downloader

class AbstractDownloader(Downloader):
    def __init__(self, headers):
        self.headers = headers
        self.timeout = module_config.get("timeout")
        self.request_max_count = module_config.get("request_max_count")
        
    @LoggerWrapper(logger)
    def get_response_json_by_url(self, url: str) -> dict:
        """通过url获取json信息

        Args:
            url (str): url

        Returns:
            list: json信息
        """
        counter = 1
        while True:
            try:
                response = requests.get(url, headers = self.headers, timeout = self.timeout)
                break
            # 这里不会捕获KeyboardInterrupt
            except Exception:
                logger.exception("第{}次失败".format(counter))
                counter += 1
                if counter >= self.request_max_count:
                    logger.error("达到失败次数上限{}".format(counter))
                    return {}
        response.raise_for_status()
        return response.json()