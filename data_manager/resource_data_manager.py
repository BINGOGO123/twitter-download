from .data_manager import DataManager
from database import mysql
from database import sqlite
from err.err import *
from . import logger
from tool.decorators import LoggerWrapper
from .media import Media
from datetime import datetime
from database.abstract_db import AbstractDb


class ResourceDataManager(DataManager):
    def __init__(self, database: AbstractDb):
        self.database = database
        self.create_table_if_not_exist()
        
        
    def create_table_if_not_exist(self):
        if isinstance(self.database, mysql.Db):
            self.create_table_if_not_exist_mysql()
        elif isinstance(self.database, sqlite.Db):
            self.create_table_if_not_exist_sqlite()
            
            
    def create_table_if_not_exist_mysql(self):
        sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = 'media'"
        ret = self.database.execute(sql)
        if len(ret) > 0:
            return
        self.database.execute(
            """
            CREATE TABLE media (
                `id` INT PRIMARY KEY AUTO_INCREMENT,
                media_url VARCHAR(1000) NOT NULL COMMENT "url链接",
                storage_path VARCHAR(500) NOT NULL COMMENT "存储路径",
                content_md5 CHAR(32) NOT NULL COMMENT "存储文件内容的md5值",
                type_suffix CHAR(32) COMMENT "文件的后缀类型",
                create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT "创建时间",
                lastchange_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间",
                KEY media_url_index (media_url(500)),
                UNIQUE KEY storage_path_index (storage_path)
            );
            """
        )
        
        
    def create_table_if_not_exist_sqlite(self):
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='media'"
        result = self.database.execute(sql)
        if len(result) > 0:
            return
        self.database.execute(
            """
            CREATE TABLE media (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                media_url VARCHAR(1000) NOT NULL, -- url链接
                storage_path VARCHAR(500) NOT NULL UNIQUE, -- 存储路径，确保唯一
                content_md5 CHAR(32) NOT NULL, -- 存储文件内容的md5值
                type_suffix CHAR(32), -- 文件的后缀类型
                create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 创建时间
                lastchange_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP -- 更新时间
            );
            """
        )
        self.database.execute("CREATE INDEX idx_media_url ON media(media_url);")
        self.database.execute("CREATE INDEX idx_storage_path ON media(storage_path);")
        self.database.execute(
            """
            CREATE TRIGGER update_lastchange_time
            AFTER UPDATE ON media
            FOR EACH ROW
            BEGIN
                UPDATE media SET lastchange_time = CURRENT_TIMESTAMP WHERE id = OLD.id;
            END;
            """
        )


    @LoggerWrapper(logger)
    def get_data_info_by_url(self, url: str) -> list[Media]:
        try:
            ret = self.database.escape_execute(
                "select storage_path, media_url, content_md5, type_suffix, create_time, lastchange_time, id from media where media_url = {}",
                url,
            )
            return self.convert_media_list(ret)
        except Exception as ex:
            logger.exception(ex)
        return []

    def convert_media_list(self, ret: list[list]) -> list[Media]:
        return [self.convert_media(one) for one in ret]

    def convert_media(self, one: list) -> Media:
        return Media(
            storage_path=one[0],
            media_url=one[1],
            content_md5=one[2],
            type_suffix=one[3],
            create_time=(
                one[4]
                if not isinstance(one[4], str)
                else datetime.strptime(one[4], "%Y-%m-%d %H:%M:%S")
            ),
            lastchange_time=(
                one[5]
                if not isinstance(one[5], str)
                else datetime.strptime(one[5], "%Y-%m-%d %H:%M:%S")
            ),
            id=one[6],
        )

    @LoggerWrapper(logger)
    def insert_data(self, media: Media):
        try:
            insert_key_list, insert_value_list = self.get_inserted_data(media)
            if len(insert_key_list) == 0:
                logger.error("Noting to be inserted")
                return
            insert_sql = self.get_inserted_sql(insert_key_list)
            self.database.escape_execute(insert_sql, *insert_value_list)
        except Exception as ex:
            logger.exception(ex)


    def get_inserted_sql(self, insert_key_list):
        insert_keys = ",".join(insert_key_list)
        insert_value_placeholders = ",".join(["{}"] * len(insert_key_list))
        insert_sql = "insert into media ({}) values ({})".format(
            insert_keys, insert_value_placeholders
        )
        return insert_sql

    def get_inserted_data(self, media: Media):
        insert_key_list = []
        insert_value_list = []
        if media.get_media_url() != None:
            insert_key_list.append("media_url")
            insert_value_list.append(media.get_media_url())
        if media.get_storage_path() != None:
            insert_key_list.append("storage_path")
            insert_value_list.append(media.get_storage_path())
        if media.get_content_md5() != None:
            insert_key_list.append("content_md5")
            insert_value_list.append(media.get_content_md5())
        if media.get_suffix_type() != None:
            insert_key_list.append("type_suffix")
            insert_value_list.append(media.get_storage_path())
        return insert_key_list, insert_value_list


    @LoggerWrapper(logger)
    def get_all_data(self) -> list[Media]:
        try:
            ret = self.database.execute(
                "select storage_path, media_url, content_md5, type_suffix, create_time, lastchange_time, id from media"
            )
            return self.convert_media_list(ret)
        except Exception as ex:
            logger.exception(ex)
        return []
    
    
    @LoggerWrapper(logger)
    def delete_data_info_by_storage_path(self, storage_path: str) -> bool:
        try:
            self.database.escape_execute(
                "delete from media where storage_path = {}",
                storage_path
            )
            return True
        except Exception as ex:
            logger.exception(ex)
        return False
