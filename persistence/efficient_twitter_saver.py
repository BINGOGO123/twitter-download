from .twitter_saver import TwitterSaver
from downloader.downloader import Downloader
from data_manager.data_manager import DataManager
from data_manager.media import Media
import os
from . import logger
import hashlib
import sys
from downloader.common_downloader import CommonDownloader
from database.abstract_db import AbstractDb
import json
from data_manager.resource_data_manager import ResourceDataManager


class EfficientTwitterSaver(TwitterSaver):
    def __init__(self, downloader: Downloader, data_manager: DataManager, **kwargs):
        """初始化
        Optional args:
            target_dir(str): 默认的存储dir
        """
        super().__init__(downloader, **kwargs)
        self.data_manager: DataManager = data_manager


    def generate_md5_hash(self, data_bytes: bytes) -> str:
        # 创建一个md5 hash对象
        md5_hash = hashlib.md5()

        # 更新hash对象的数据
        md5_hash.update(data_bytes)

        # 获取十六进制形式的哈希值
        hex_digest = md5_hash.hexdigest()

        return hex_digest


    def save_media(self, save_name, content: bytes):
        save_name = os.path.abspath(save_name)
        if os.path.isfile(save_name):
            logger.error("{} has existed".format(save_name))
            return
        save_name = super().save_media(save_name, content)
        return save_name
    
    
    def save_record(self, save_name:str, data: bytes, url: str):
        if save_name != None and data != None and url != None:
            self.data_manager.insert_data(Media(media_url = url, storage_path = save_name, content_md5 = self.generate_md5_hash(data)))


    def get_data_by_url(self, url: str) -> bytes:
        try:
            media_list: list[Media] = self.data_manager.get_data_info_by_url(url)
            if len(media_list) > 0:
                for media in media_list:
                    storage_path = media.get_storage_path()
                    if storage_path != None and os.path.isfile(storage_path):
                        f = open(storage_path, "rb")
                        try:
                            data = f.read()
                            logger.info("Get data from disk, url={}, storage_path={}".format(url, storage_path))
                            return data
                        finally:
                            f.close()
        except Exception as ex:
            logger.error(ex)
        return super().get_data_by_url(url)
    
    
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