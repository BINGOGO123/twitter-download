import sqlite3
from . import logger
from .abstract_db import AbstractDb
from . import module_config
from tool.decorators import LoggerWrapper


class Db(AbstractDb):
    @LoggerWrapper(logger)
    def __init__(self, **kwargs):
        """初始化创建
        Optional args:
            sqlite_db_name(str): 数据库文件名称
        """
        db: str = kwargs.get("sqlite_db_name", module_config.get("sqlite_db_name"))
        if db.split(".")[-1] != "db":
            db += ".db"
        self.db = sqlite3.connect(db, check_same_thread=False)


    def __del__(self):
        """
        析构对象
        """
        if hasattr(self, "db"):
            self.db.close()


    @LoggerWrapper(logger)
    def execute(self, sql: str):
        """
        执行sql语句，正确返回结果，一个列表[]，可能为空
        """
        cur = self.db.cursor()
        try:
            cur.execute(sql)
            self.db.commit()
        except Exception as ex:
            self.db.rollback()
            raise ex
        else:
            return cur.fetchall()
        finally:
            cur.close()


    @LoggerWrapper(logger)
    def escape_execute(self, sql: str, *data):
        """
        data中可能存在'和"等数据，通过参数化执行sql语句

        正确返回结果，一个列表[]，可能为空
        """
        cur = self.db.cursor()
        sql = sql.format(*(["?"] * len(data)))
        try:
            cur.execute(sql, data)
            self.db.commit()
        except Exception as ex:
            self.db.rollback()
            raise ex
        else:
            return cur.fetchall()
        finally:
            cur.close()
