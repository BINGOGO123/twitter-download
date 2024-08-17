from .twitter_saver import TwitterSaver
from downloader.downloader import Downloader
from data_manager.data_manager import DataManager
from data_manager.media import Media
import os
from . import logger
import sys
from downloader.common_downloader import CommonDownloader
from database.abstract_db import AbstractDb
import json
from data_manager.resource_data_manager import ResourceDataManager
from tool.tool import generate_md5_hash
from downloader.data_strategy import DataStrategy
import hashlib


class Md5DataStrategy(DataStrategy):
    def __init__(self):
        self.hasher = hashlib.md5()
        
    
    def execute(self, data: bytes):
        self.hasher.update(data)
        

    def get_result(self):
        return self.hasher.hexdigest()
    
    

class EfficientTwitterSaver(TwitterSaver):
    def __init__(self, downloader: Downloader, data_manager: DataManager, **kwargs):
        """初始化
        Optional args:
            target_dir(str): 默认的存储dir
        """
        super().__init__(downloader, **kwargs)
        self.data_manager: DataManager = data_manager
        
        
    def save_file(self, file_name: str, url: str) -> str:
        try:
            media_list: list[Media] = self.data_manager.get_data_info_by_url(url)
            if len(media_list) > 0:
                for media in media_list:
                    storage_path = media.get_storage_path()
                    if storage_path != None and os.path.isfile(storage_path):
                        try:
                            with open(storage_path, "rb") as f:
                                data = f.read()
                                logger.debug("Get data from disk, url={}, storage_path={}".format(url, storage_path))
                                file_name = self.save_media_content(file_name, data)
                                self.save_record(file_name, url, generate_md5_hash(data))
                                return file_name
                        except Exception as ex:
                            logger.exception(ex)
        except Exception as ex:
            logger.exception(ex)
        
        file_name = self.save_file_by_url(file_name, url)
        return file_name


    def save_file_by_url(self, file_name, url):
        data_strategy = Md5DataStrategy()
        try:
            file_name = self.downloader.download_file(file_name, url, None, data_strategy)
            if file_name != None:
                self.save_record(file_name, url, data_strategy.get_result())
                return file_name
        except Exception as ex:
            logger.exception(ex)


    def save_media_content(self, file_name, content: bytes):
        try:
            with open(file_name, "wb") as f:
                f.write(content)
        except Exception as ex:
            logger.exception(ex)
        return file_name
    
    
    def save_record(self, file_name:str, url: str, md5: str):
        if file_name != None and md5 != None and url != None:
            self.data_manager.insert_data(Media(media_url = url, storage_path = file_name, content_md5 = md5))
    
    
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
    saver = EfficientTwitterSaver(CommonDownloader(), ResourceDataManager(AbstractDb.get_default_database()))
    if isinstance(pointer_list, list):
        for pointer in pointer_list:
            saver.save(pointer)
    else:
        saver.save(pointer_list)