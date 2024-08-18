import os
import logging
from configs import get_module_config
import argparse
from gallary.common_gallary import CommonGallary

# 获取配置和 logger
module_config: dict
logger: logging.Logger
module_config, logger = get_module_config(__name__)


def get_args():
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description="Generate the gallary.")
    parser.add_argument("-s", "--source-dir", type=str, help="the source dir which is used to generate gallay")
    parser.add_argument("-t", "--target-dir", type=str, help="the target dir to keep generated result")


    # 解析命令行参数
    args = parser.parse_args()
    
    # 获取对应的参数
    source_dir = args.source_dir
    target_dir = args.target_dir if args.target_dir != None else module_config.get("gallary_dir")
    
    return source_dir, target_dir


if __name__ == "__main__":
    source_dir, target_dir = get_args()
    
    if source_dir == None:
        logger.critical("Please input the source dir which is used to generate gallay.")
        exit(-1)
        
    if target_dir == None:
        logger.critical("Please input the target dir to keep generated result.")
        exit(-1)
        
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    logger.info("source dir: {}, target_dir: {}".format(source_dir, target_dir))
    gallary = CommonGallary()
    gallary.generate([source_dir], target_dir, source_dir)

