from abc import ABCMeta, abstractmethod
from . import module_config
import importlib
from tool.decorators import LoggerWrapper
from . import logger

class AbstractDb(metaclass = ABCMeta):
    @abstractmethod
    def execute(self, sql):
        pass


    @abstractmethod
    def escape_execute(self, sql, *data):
        pass

    
    @LoggerWrapper(logger)
    def get_default_database():
        # 根据config返回默认数据库及配置
        package_name = ".{}".format(module_config.get("default_database_type"))
        package = __name__.rsplit('.', 1)[0]  # 获取当前模块的包名
        db = importlib.import_module(package_name, package = package)
        return db.Db()
