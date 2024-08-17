from .downloader import Downloader
from . import logger
from . import module_config
from tool.decorators import LoggerWrapper
import requests
from tool.tool import cover
import copy
from tqdm import tqdm
import sys
from .data_strategy import DataStrategy


class CommonDownloader(Downloader):
    def __init__(self, **kwargs):
        """初始化
        Optional Args:
            requests_kwargs(dict): 请求参数
            request_max_count(int): 请求最大次数
        """
        self.default_requests_kwargs = kwargs.get(
            "requests_kwargs", module_config.get("requests_kwargs")
        )
        self.request_max_count = kwargs.get(
            "request_max_count", module_config.get("request_max_count")
        )


    def get_tw_response_by_url(
        self, url: str, params=None, **kwargs
    ) -> requests.Response:
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
    def get_tw_response_json_by_url(self, url: str, params=None, **kwargs) -> dict:
        """通过url请求获取json结果
        Args:
            url(str): url
            params(str): params
            kwargs: 其他请求参数
        """
        try:
            response = self.get_tw_response_by_url(url, params, **kwargs)
            if response != None:
                return response.json()
        except Exception as ex:
            logger.exception(ex)
        return {}


    @LoggerWrapper(logger)
    def get_tw_response_bytes_by_url(self, url: str, params=None, **kwargs) -> bytes:
        """通过url请求获取二进制结果
        Args:
            url(str): url
            params(str): params
            kwargs: 其他请求参数
        """
        try:
            response = self.get_tw_response_by_url(url, params, **kwargs)
            if response != None:
                return response.content
        except Exception as ex:
            logger.exception(ex)
        return bytes()


    @LoggerWrapper(logger)
    def download_file(self, file_name: str, url: str, params=None, data_strategy: DataStrategy = None, **kwargs) -> str:
        with requests.get(url, params=params, stream=True, **kwargs) as r:
            r.raise_for_status()  # 检查响应状态码

            # 获取文件总大小
            total_size = int(r.headers.get("content-length", 0))

            # 以二进制模式打开文件，'wb+'表示可读写
            with open(file_name, "wb") as f, tqdm(
                desc=file_name,
                total=total_size,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
                colour="yellow",
                leave=False
            ) as bar:
                for data in r.iter_content(chunk_size=1024):
                    # 写入文件
                    size = f.write(data)
                    if data_strategy != None:
                        data_strategy.execute(data)
                    # 更新进度条
                    bar.update(size)
        return file_name


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        logger.critical("Please input media url")
        exit(-1)
    url = sys.argv[1]
    file_name = url.split("/")[-1].split("?")[0]
    downloader = CommonDownloader()
    downloader.download_file(file_name, url)
