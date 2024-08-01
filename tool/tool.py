import copy
import os
import logging
import datetime

def cover(o1: dict, o2: dict) -> None:
  """
  o1和o2是dict，用o2覆盖o1中的值

  对于o2和o1键相同且值均为dict类型的情况，递归调用cover处理

  Args:
      o1 (dict): 被覆盖的dict
      o2 (dict): 覆盖的dict
  """
  for key in o2:
    if type(o2.get(key)) == dict and type(o1.get(key)) == dict:
      cover(o1[key], o2[key])
    # 这里一定要copy，否则如果o2[key]也是对象，o1[key]会直接指向o2[key]
    else:
      o1[key] = copy.deepcopy(o2[key])



def initialLogger(logger: logging.Logger, name:str, logs_dir: str, logger_level: str, file_level: str, stream_level: str, **args) -> None:
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
  handler1 = logging.FileHandler(os.path.join(logs_dir, name + "." + str(datetime.date.today()) + ".log"),"a",encoding="utf8")
  handler2 = logging.StreamHandler()
  formatter1 = logging.Formatter(fmt="%(asctime)s [%(levelname)s] [%(filename)s] [%(lineno)d] [%(funcName)s] >> %(message)s",datefmt="%Y-%m-%d %H:%M:%S")
  formatter2 = logging.Formatter(fmt = "[%(levelname)s] >> %(message)s")
  handler1.setFormatter(formatter1)
  handler2.setFormatter(formatter2)
  handler1.setLevel(eval(file_level))
  handler2.setLevel(eval(stream_level))
  logger.setLevel(eval(logger_level))
  logger.addHandler(handler1)
  logger.addHandler(handler2)