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
from configs.constants import COLORS


class TwitterSaver(Saver):
    def __init__(self, downloader: Downloader, **kwargs):
        """初始化
        Optional args:
            target_dir(str): 默认的存储dir
        """
        self.downloader: Downloader = downloader
        self.target_dir = kwargs.get("target_dir", module_config.get("target_dir"))

    
    @LoggerWrapper(logger)
    def save_all(self, entry_list: list[dict], target_dir = None) -> list[str]:
        ret = []
        size = len(entry_list)
        with tqdm(total=size, desc="Entry download Progress", colour="green", dynamic_ncols=True) as pbar:
            for i in range(len(entry_list)):
                entry = entry_list[i]
                logger.debug("Entry download progress [{}/{}]".format(i + 1, size))
                ret.append(self.save(entry, target_dir))
                pbar.update(1)
        return ret


    @LoggerWrapper(logger, True)
    def save(self, entry: dict, target_dir = None) -> str:
        target_dir = self.target_dir if target_dir is None else target_dir
        try:
            entry_id = entry.get("entry_id")
            if entry_id == None or entry_id == "":
                logger.error("entry id is empty")
                return
            entry_target_dir = os.path.abspath(os.path.join(target_dir, entry_id))
            self.create_dir(entry_target_dir)
            result = self.get_result(entry)
            self.save_json(entry, entry_target_dir)
            self.save_result(result, entry_target_dir)
            logger.debug(f"Entry saved at: {entry_target_dir}")
            tqdm.write(f"{COLORS['green']}Entry saved at: {entry_target_dir}{COLORS['reset']}")
            return entry_target_dir
        except Exception as ex:
            logger.exception(ex)
    
    
    def save_result(self, result: dict, target_dir: str) -> str:
        medias = self.get_medias(result)
        self.save_medias(medias, target_dir)
        return target_dir


    def get_medias(self, result: dict) -> list:
        return result.get("twitter_info", {}).get("medias", [])


    def get_result(self, entry: dict) -> dict:
        return entry.get("content_info", {}).get("result", {})


    def create_dir(self, target_dir: str):
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)
            
            
    def save_medias(self, medias: list, target_dir: str):
        total_count = len(medias)
        with tqdm(total=total_count, desc="Media  Progress  ", colour="cyan", leave=False, dynamic_ncols=True) as pbar:
            for index in range(len(medias)):
                logger.debug("Media download progress [{}/{}]".format(index + 1, total_count))
                self.save_media_info(medias[index], target_dir, index + 1)
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
            file_name = self.save_file(file_name, url)
            logger.debug("Media saved at: {}".format(file_name))
            tqdm.write(f"{COLORS['cyan']}Media saved at: {file_name}{COLORS['reset']}")
            return file_name
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
        

    def save_json(self, json_data: dict, target_dir: str) -> str:
        try:
            file_name = os.path.join(target_dir, "entry.json")
            with open(file_name, "w", encoding = "utf8") as f:
                f.write(get_formatted_json_str(json_data))
                f.close()
            return os.path.abspath(file_name)
        except Exception as ex:
            logger.exception(ex)
    
    
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        logger.critical("Please input the path of saving entry")
        exit(-1)
    file_name = sys.argv[1]
    f = open(file_name, "rb")
    try:
        entry_list = json.loads(f.read().decode("utf8"))
    finally:
        f.close()
    saver = TwitterSaver(CommonDownloader())
    if isinstance(entry_list, list):
        saver.save_all(entry_list)
    else:
        saver.save(entry_list)
