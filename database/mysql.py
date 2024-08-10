import pymysql
from dbutils.pooled_db import PooledDB
from pymysql.converters import escape_string
from . import logger
from tool.tool import cover
from .err import ConnectException
from .abstract_db import AbstractDb
from tool.decorators import LoggerWrapper
from . import module_config


class Db(AbstractDb):
    @LoggerWrapper(logger)
    def __init__(self, **kwargs):
        """初始化数据库对象，根据传入的参数以及config配置
        Optional args:
            host(str): host
            port(int): port
            user(str): user
            password(str): passwrod
            database(sr): database
        Raises:
            e: 异常
        """
        default_db_connect_params = module_config.get("db_connect_params", {})
        user_db_connect_params = {
            "host": kwargs.get("host", default_db_connect_params.get("host")),
            "port": kwargs.get("port", default_db_connect_params.get("port")),
            "user": kwargs.get("user", default_db_connect_params.get("user")),
            "password": kwargs.get("password", default_db_connect_params.get("password")),
            "database": kwargs.get("database", default_db_connect_params.get("database")),
        }
        user_db_connect_params = cover(default_db_connect_params, user_db_connect_params)
        
        try:
            self.pool = PooledDB(**user_db_connect_params)
        except pymysql.err.OperationalError as e:
            # 表示数据库能连接，但是库名不存在
            if e.args[0] == 1049:
                self.create_database(user_db_connect_params)
                self.pool = PooledDB(**user_db_connect_params)
            else:
                raise e


    @LoggerWrapper(logger)
    def create_database(self, user_db_connect_params: dict) -> None:
        create_db_connect_params = cover({}, user_db_connect_params)
        db = create_db_connect_params.get("database")
        del create_db_connect_params["database"]
        self.pool = PooledDB(**create_db_connect_params)
        try:
            if self.execute("create database if not exists {}".format(db)) == False:
                raise ConnectException("Create database ({}) failed".format(db))
        finally:
            self.pool.close()


    def __del__(self):
        """
        析构对象
        """
        if hasattr(self, "pool"):
            self.pool.close()


    @LoggerWrapper(logger)
    def execute(self, sql: str):
        """
        执行sql语句，正确返回结果，一个元组()，可能为空
        """
        conn = self.pool.connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as ex:
                conn.rollback()
                raise ex
            else:
                return cursor.fetchall()
            finally:
                cursor.close()
        finally:
            conn.close()


    @LoggerWrapper(logger)
    def escape_execute(self, sql: str, *data):
        """
        data中可能存在'和"和\数据，因为传给mysql之后会在转义一次，因此需要在前面加上\转义

        正确返回结果，一个元组()，可能为空
        """
        # 手动组装成sql语句，所以两边需要加上''
        escape_data = ["'{}'".format(escape_string(x)) for x in data]
        escape_sql = sql.format(*escape_data)
        return self.execute(escape_sql)
