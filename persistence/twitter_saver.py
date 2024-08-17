from .saver import Saver
from tool.decorators import LoggerWrapper
from . import logger
import os
from tool.tool import get_formatted_json_str
from . import module_config
import sys
import json
from downloader.downloader import Downloader
from downloader.common_downloader import CommonDownloader
from tqdm import tqdm

# 定义颜色代码
colors = {
    'red': '\033[91m',
    'green': '\033[92m',
    'blue': '\033[94m',
    'yellow': '\033[93m',
    'reset': '\033[0m',
    'pink': '\033[95m',
    'brown': '\033[33m\033[2m',
    'purple': '\033[95m',
    'orange': '\033[33m',
    'cyan': '\033[36m'
}


class TwitterSaver(Saver):
    def __init__(self, downloader: Downloader, **kwargs):
        """初始化
        Optional args:
            target_dir(str): 默认的存储dir
        """
        self.downloader: Downloader = downloader
        self.target_dir = kwargs.get("target_dir", module_config.get("target_dir"))
        
    
    @LoggerWrapper(logger)
    def save_all(self, pointer_list: list[dict], target_dir = None) -> list[str]:
        ret = []
        size = len(pointer_list)
        with tqdm(total=size, desc="Twitter download Progress", colour="green", dynamic_ncols=True) as pbar:
            for i in range(len(pointer_list)):
                pointer = pointer_list[i]
                logger.debug("Twitter saving progress [{}/{}]".format(i + 1, size))
                ret += self.save(pointer, target_dir)
                pbar.update(1)
        return ret


    @LoggerWrapper(logger, True)
    def save(self, pointer: dict, target_dir = None) -> list[str]:
        target_dir = self.target_dir if target_dir is None else target_dir
        result_target_dir_list = []
        try:
            result_list = self.get_result_list(pointer)
            total_count = len(result_list)
            with tqdm(total=total_count, desc="Result download Progress ", colour="blue", leave=False, dynamic_ncols=True) as pbar:
                for i in range(total_count):
                    logger.debug("Result saving progress [{}/{}]".format(i + 1, total_count))
                    result = result_list[i]
                    result_target_dir = self.save_result(result, target_dir)
                    pbar.write(f"{colors['blue']}Result saved  at: {result_target_dir}{colors['reset']}")
                    result_target_dir_list.append(result_target_dir)
                    pbar.update(1)
        except Exception as ex:
            logger.exception(ex)
        return result_target_dir_list
    
    
    def save_result(self, result: dict, target_dir: str) -> str:
        rest_id = result.get("rest_id")
        if rest_id == None or rest_id == "":
            logger.error("rest id is empty")
            return
        result_target_dir = os.path.abspath(os.path.join(target_dir, rest_id))
        self.create_dir(result_target_dir)
        self.save_result_json(result, result_target_dir)
        medias = self.get_medias(result)
        self.save_medias(medias, result_target_dir)
        return result_target_dir


    def get_medias(self, result: dict) -> list:
        return result.get("twitter_info", {}).get("medias", [])


    def get_result_list(self, pointer: dict) -> list:
        return pointer.get("content_info", {}).get("result_list", [])


    def create_dir(self, target_dir: str):
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)
            
            
    def save_medias(self, medias: list, target_dir: str):
        total_count = len(medias)
        with tqdm(total=total_count, desc="Media download Progress  ", colour="cyan", leave=False, dynamic_ncols=True) as pbar:
            for index in range(len(medias)):
                logger.debug("Media saving progress [{}/{}]".format(index + 1, total_count))
                file_name = self.save_media_info(medias[index], target_dir, index + 1)
                logger.debug("Media saved at: {}".format(file_name))
                pbar.write(f"{colors['cyan']}Media saved at: {file_name}{colors['reset']}")
                pbar.update(1)


    def save_media_info(self, media_info: dict, target_dir: str, order: int) -> str:
        try:
            url = self.get_url(media_info)
            if url == None or url == "":
                logger.error("Media has no download url")
                return
            file_name = self.generate_save_name(target_dir, order, url)
            if os.path.isfile(file_name):
                logger.debug("{} has existed".format(file_name))
                return
            return self.save_file(file_name, url)
        except Exception as ex:
            logger.exception(ex)


    def get_url(self, media_info):
        url = media_info.get("vedio_info", {}).get("url")
        if url == None or url == "":
            url = media_info.get("media_url_https")
        return url


    def generate_save_name(self, target_dir, order, url):
        media_name = url.split("?")[0].split("/")[-1]
        save_name = os.path.join(target_dir, "{}_{}".format(order, media_name))
        return os.path.abspath(save_name)
    
    
    def save_file(self, file_name: str, url: str) -> str:
        try:
            self.downloader.download_file(file_name, url)
        except Exception as ex:
            logger.exception(ex)
        return file_name
        

    def save_result_json(self, result: dict, result_target_dir: str) -> str:
        try:
            file_name = os.path.join(result_target_dir, "result.json")
            with open(file_name, "w", encoding = "utf8") as f:
                f.write(get_formatted_json_str(result))
                f.close()
            return os.path.abspath(file_name)
        except Exception as ex:
            logger.exception(ex)
    
    
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        logger.critical("Please input the path of save pointer")
        exit(-1)
    file_name = sys.argv[1]
    f = open(file_name, "rb")
    try:
        pointer_list = json.loads(f.read().decode("utf8"))
    finally:
        f.close()
    saver = TwitterSaver(CommonDownloader())
    if isinstance(pointer_list, list):
        for pointer in pointer_list:
            saver.save(pointer)
    else:
        saver.save(pointer_list)
