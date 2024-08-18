from data_manager.resource_data_manager import ResourceDataManager
from database import sqlite
from database import mysql
import logging
from configs import get_module_config
from tqdm import tqdm
from data_manager.data_manager import DataManager
import argparse

# 获取配置和 logger
module_config: dict
logger: logging.Logger
module_config, logger = get_module_config(__name__)


def migrate_data(data_manager: DataManager, insert_set: set, from_name: str, to_name: str):
    with tqdm(total=len(insert_set), desc="{} -> {}".format(from_name, to_name), colour="green") as pbar:
        for media in insert_set:
            data_manager.insert_data(media)
            pbar.update(1)
    logger.debug("migrate {} data from {} to {}".format(insert_set, from_name, to_name))


def migrate():
    sqlite_db_name = module_config.get("sqlite_db_name")
    sqlite_manager = ResourceDataManager(sqlite.Db(sqlite_db_name = sqlite_db_name) if sqlite_db_name != None else sqlite.Db())
    
    db_connect_params = module_config.get("db_connect_params", {})
    mysql_manager = ResourceDataManager(mysql.Db(**db_connect_params))

    sqlite_media_set = set(sqlite_manager.get_all_data())
    mysql_media_set = set(mysql_manager.get_all_data())
    
    mysql_insert_set = mysql_media_set - sqlite_media_set
    sqlite_insert_set = sqlite_media_set - mysql_media_set
    
    migrate_data(sqlite_manager, mysql_insert_set, "Mysql", "Sqlite")
    migrate_data(mysql_manager, sqlite_insert_set, "Sqlite", "Mysql")
    
    
def get_args():
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description="Migrate the media records between sqlite and mysql.")

    # 解析命令行参数
    args = parser.parse_args()
    
    return None


if __name__ == "__main__":
    get_args()
    migrate()