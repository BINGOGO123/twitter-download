from .common_saver import AbstractSaver
from tool.decorators import LoggerWrapper
from . import logger
import os
from tool.tool import get_formatted_json_str
from . import module_config
import sys
import json

class TwitterSaver(AbstractSaver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_dir = kwargs.get("target_dir", module_config.get("target_dir"))


    @LoggerWrapper(logger, True)
    def save(self, pointer: dict, target_dir = None) -> list[str]:
        if target_dir == None:
            target_dir = self.target_dir
        try:
            result_list = pointer.get("content_info", {}).get("result_list", [])
            result_target_dir_list = []
            total_count = len(result_list)
            for i in range(len(result_list)):
                logger.info("Saving result: {}, total count: {}".format(i + 1, total_count))
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
            return result_target_dir_list
        except Exception as ex:
            logger.exception(ex)
            return []

    
    def create_dir(self, target_dir: str) -> None:
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)
            
            
    def save_media_info_list(self, media_info_list: list, target_dir: str) -> None:
        total_count = len(media_info_list)
        for index in range(len(media_info_list)):
            logger.info("Saving media: {}, total count: {}".format(index + 1, total_count))
            saved_dir = self.save_media_info(media_info_list[index], target_dir, index + 1)
            logger.info("Saved at: {}".format(saved_dir))


    def save_media_info(self, media_info: dict, target_dir: str, order: int) -> str:
        try:
            url = media_info.get("vedio_info", {}).get("url")
            if url == None or url == "":
                url = media_info.get("media_url_https")
            if url == None or url == "":
                return None
            media_name = url.split("?")[0].split("/")[-1]
            save_name = os.path.join(target_dir, "{}_{}".format(order, media_name))
            data = self.downloader.get_tw_response_bytes_by_url(url)
            self.save_media(save_name, data)
            return os.path.abspath(save_name)
        except Exception as ex:
            logger.exception(ex)
            

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
    pointer_list = json.loads(f.read().decode("utf8"))
    saver = TwitterSaver()
    for pointer in pointer_list:
        saver.save(pointer)