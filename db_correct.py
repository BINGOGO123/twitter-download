from data_manager.resource_data_manager import ResourceDataManager
import logging
from configs import get_module_config
import os
from tool.tool import generate_md5_hash
from data_manager.media import Media
from database.abstract_db import AbstractDb
import sys
from tool.decorators import LoggerWrapper
from tqdm import tqdm
import argparse


# 获取配置和 logger
module_config: dict
logger: logging.Logger
module_config, logger = get_module_config(__name__)


def get_md5_from_file(file_name: str) -> str:
    f = open(file_name, "rb")
    try:
        data = f.read()
    finally:
        f.close()
    return generate_md5_hash(data)


def is_valid_data(md5_check, storage_path, media_url, content_md5):
    return (
        media_url is not None
        and storage_path is not None
        and os.path.isfile(storage_path)
        and (not md5_check or content_md5 == get_md5_from_file(storage_path))
    )


def is_valid_media(media: Media, md5_check: bool) -> bool:
    storage_path = media.get_storage_path()
    media_url = media.get_media_url()
    content_md5 = media.get_content_md5()
    return is_valid_data(md5_check, storage_path, media_url, content_md5)


@LoggerWrapper(logger)
def db_checker(md5_check, db_correct_remove_invalid):
    manager = ResourceDataManager(AbstractDb.get_default_database())
    media_list = manager.get_all_data()
    invalid_media_list = []
    with tqdm(total=len(media_list), desc="Check media progress", colour="green") as pbar:
        for media in media_list:
            if not is_valid_media(media, md5_check):
                invalid_media_list.append(media)
                logger.debug(media)
                if (db_correct_remove_invalid):
                    manager.delete_data_info_by_storage_path(media.get_storage_path())
            pbar.update(1)
    logger.info("Total [{}] invalid media".format(len(invalid_media_list)))
    
    
def get_args():
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description="Check the correctness of the default database.")
    parser.add_argument("-m", "--md5-check", type=bool, help="check the md5 of the file and of the value storaged in database")
    parser.add_argument("-r", "--remove_invalid", type=bool, help="remove the invalid database record while checking the database")

    # 解析命令行参数
    args = parser.parse_args()
    
    # 获取对应的参数
    md5_check = args.md5_check if args.md5_check != None else module_config.get("md5_check")
    db_correct_remove_invalid = args.remove_invalid if args.remove_invalid != None else module_config.get("db_correct_remove_invalid")
    
    return md5_check, db_correct_remove_invalid


if __name__ == "__main__":
    md5_check, db_correct_remove_invalid = get_args()
    logger.info("md5_check: {}, db_correct_remove_invalid: {}".format(str(md5_check), str(db_correct_remove_invalid)))
    
    db_checker(md5_check, db_correct_remove_invalid)
