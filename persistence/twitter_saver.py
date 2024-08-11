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
        for i in range(len(pointer_list)):
            pointer = pointer_list[i]
            logger.info("Twitter saving progress [{}/{}]".format(i + 1, size))
            ret += self.save(pointer, target_dir)
        return ret


    @LoggerWrapper(logger, True)
    def save(self, pointer: dict, target_dir = None) -> list[str]:
        if target_dir == None:
            target_dir = self.target_dir
            
        result_target_dir_list = []
        try:
            result_list = pointer.get("content_info", {}).get("result_list", [])
            total_count = len(result_list)
            for i in range(len(result_list)):
                logger.info("Result saving progress [{}/{}]".format(i + 1, total_count))
                result = result_list[i]
                rest_id = result.get("rest_id")
                if rest_id == None or rest_id == "":
                    logger.warning("rest id is empty")
                    continue
                result_target_dir = os.path.join(target_dir, rest_id)
                self.create_dir(result_target_dir)
                result_target_dir_list.append(os.path.abspath(result_target_dir))
                media_info_list = result.get("twitter_info", {}).get("medias", [])
                self.save_media_info_list(media_info_list, result_target_dir)
                self.save_result_json(result, result_target_dir)
        except Exception as ex:
            logger.exception(ex)
        return result_target_dir_list



    def create_dir(self, target_dir: str) -> None:
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)
            
            
    def save_media_info_list(self, media_info_list: list, target_dir: str) -> None:
        total_count = len(media_info_list)
        for index in range(len(media_info_list)):
            logger.info("Media saving progress [{}/{}]".format(index + 1, total_count))
            save_name = self.save_media_info(media_info_list[index], target_dir, index + 1)
            logger.info("Media saved at: {}".format(save_name))

    def save_media_info(self, media_info: dict, target_dir: str, order: int) -> str:
        try:
            url = media_info.get("vedio_info", {}).get("url")
            if url == None or url == "":
                url = media_info.get("media_url_https")
            if url == None or url == "":
                return
            save_name = self.generate_save_name(target_dir, order, url)
            if os.path.isfile(save_name):
                logger.error("{} has existed".format(save_name))
                return
            data = self.get_data_by_url(url)
            save_name = self.save_media(save_name, data)
            self.save_record(save_name, data, url)
            return save_name
        except Exception as ex:
            logger.exception(ex)


    def save_record(self, save_name:str, data: bytes, url: str):
        pass   


    def generate_save_name(self, target_dir, order, url):
        media_name = url.split("?")[0].split("/")[-1]
        save_name = os.path.join(target_dir, "{}_{}".format(order, media_name))
        return os.path.abspath(save_name)


    def get_data_by_url(self, url: str) -> bytes:
        data = self.downloader.get_tw_response_bytes_by_url(url)
        return data
            

    def save_media(self, file_name: str, content: bytes) -> str:
        f = open(file_name, "wb")
        f.write(content)
        f.close()
        return os.path.abspath(file_name)
        

    def save_result_json(self, result: dict, result_target_dir: str) -> str:
        filename = os.path.join(result_target_dir, "result.json")
        f = open(filename, "w", encoding = "utf8")
        f.write(get_formatted_json_str(result))
        f.close()
        return os.path.abspath(filename)
    
    
if __name__ == "__main__":
    if (len(sys.argv) < 2):
        logger.error("Please input the path of save pointer")
        exit(-1)
    filename = sys.argv[1]
    f = open(filename, "rb")
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
