from data_manager.resource_data_manager import ResourceDataManager
import logging
from configs import get_module_config
import os
from tool.tool import generate_md5_hash
from data_manager.media import Media
from database.abstract_db import AbstractDb
import sys
from tool.decorators import LoggerWrapper


# 获取配置和 logger
module_config: dict
logger: logging.Logger
module_config, logger = get_module_config(__name__)


def get_md5_from_file(file_name: str) -> str:
    f = open(file_name, "wb")
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
        and (not md5_check or content_md5 == generate_md5_hash(storage_path))
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
    for media in media_list:
        if not is_valid_media(media, md5_check):
            invalid_media_list.append(media)
            logger.info(media)
            if (db_correct_remove_invalid):
                manager.delete_data_info_by_storage_path(media.get_storage_path())
    
    logger.info("Total {} invalid media info".format(len(invalid_media_list)))


if __name__ == "__main__":
    md5_check = module_config.get("module_config", False)
    db_correct_remove_invalid = module_config.get("db_correct_remove_invalid", False)
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "t" or sys.argv[1].lower() == "true":
            db_correct_remove_invalid = True
        elif sys.argv[1].lower() == "f" or sys.argv[1].lower() == "false":
            db_correct_remove_invalid = False
        else:
            logger.error("Invalid argv [{}]. Supported values: T, F.".format(sys.argv[1]))
            exit(-1)

    db_checker(md5_check, db_correct_remove_invalid)
