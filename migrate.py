from data_manager.resource_data_manager import ResourceDataManager
from database import sqlite
from database import mysql
import logging
from configs import get_module_config

# 获取配置和 logger
module_config: dict
logger: logging.Logger
module_config, logger = get_module_config(__name__)

if __name__ == "__main__":
    sqlite_db_name = module_config.get("sqlite_db_name")
    sqlite_manager = ResourceDataManager(sqlite.Db(sqlite_db_name = sqlite_db_name) if sqlite_db_name != None else sqlite.Db())
    
    db_connect_params = module_config.get("db_connect_params", {})
    mysql_manager = ResourceDataManager(mysql.Db(**db_connect_params))

    sqlite_media_set = set(sqlite_manager.get_all_data())
    mysql_media_set = set(mysql_manager.get_all_data())
    
    mysql_insert_set = mysql_media_set - sqlite_media_set
    sqlite_insert_set = sqlite_media_set - mysql_media_set
    
    for media in mysql_insert_set:
        sqlite_manager.insert_data(media)
        
    for media in sqlite_insert_set:
        mysql_manager.insert_data(media)
    
    logger.info("migrate {} data from mysql to sqlite".format(len(mysql_insert_set)))
    logger.info("migrate {} data from sqlite to mysql".format(len(sqlite_insert_set)))
