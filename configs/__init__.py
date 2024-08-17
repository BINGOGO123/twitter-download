import json
from json.decoder import JSONDecodeError
from .default_config import default_config
from tool.tool import cover
import logging
import os
import datetime

try:
    f = open("config.json", "r", encoding="utf8")
    user_config = json.loads(f.read())
    f.close()
except FileNotFoundError:
    user_config = {}
except JSONDecodeError:
    print("Error format of config.json")
    exit(-1)

base_config = {}
cover(base_config, default_config)
cover(base_config, user_config)


def get_module_config(module_name: str) -> tuple[dict, logging.Logger]:
    """从base_config根据模块名称获取对应配置

    Args:
        base_config (dict): 总配置
        module_name (str): 模块名称

    Returns:
        list[dict, logging.Logger]: 第一个变量为模块配置, 第二个变量为模块logger
    """
    logger = logging.getLogger(module_name)

    default_module_config = base_config.get("default", {})
    module_config = base_config.get(module_name, {})
    module_config = cover(default_module_config, module_config)

    initialLogger(logger, module_name, **module_config.get("logs"))
    return module_config, logger


def initialLogger(
    logger: logging.Logger,
    name: str,
    logs_dir: str,
    logger_level: str,
    file_level: str,
    stream_level: str,
    **args
) -> None:
    """初始化日志对象

    Args:
        logger (logging.Logger): 日志对象
        name (str): 日志文件名称
        logs_dir (str): 日志文件存放目录
        logger_level (str): 日志输出限制等级
        file_level (str): 文件日志输出限制等级
        stream_level (str): 控制台日志输出限制等级
    """
    # 如果不存在logs文件夹则创建
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    handler1 = logging.FileHandler(
        os.path.join(logs_dir, name + "." + str(datetime.date.today()) + ".log"),
        "a",
        encoding="utf8",
    )
    handler2 = logging.StreamHandler()
    handler3 = logging.FileHandler(
        os.path.join(logs_dir, "all." + str(datetime.date.today()) + ".log"),
        "a",
        encoding="utf8",
    )
    formatter1 = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] [%(filename)s] [%(lineno)d] [%(funcName)s] >> %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    formatter2 = logging.Formatter(fmt="[%(levelname)s] >> %(message)s")
    handler1.setFormatter(formatter1)
    handler2.setFormatter(formatter2)
    handler3.setFormatter(formatter2)
    file_level = eval(file_level) if type(file_level) == str else file_level
    stream_level = eval(stream_level) if type(stream_level) == str else stream_level
    logger_level = eval(logger_level) if type(logger_level) == str else logger_level
    handler1.setLevel(file_level)
    handler2.setLevel(stream_level)
    handler3.setLevel(stream_level)
    logger.setLevel(logger_level)
    logger.addHandler(handler1)
    logger.addHandler(handler2)
    logger.addHandler(handler3)