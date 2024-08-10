from page.tweeted import TweetedTweetPage
from downloader.common_downloader import CommonDownloader
from page.user import UserInfoPage
from persistence.efficient_twitter_saver import EfficientTwitterSaver
from data_manager.resource_data_manager import ResourceDataManager
from database.abstract_db import AbstractDb
import argparse
from configs import get_module_config
import logging
from page.favorite import FavoriteTweetPage
from page.twitter import TwitterInfoPage
import os


# 获取配置和 logger
module_config: dict
logger: logging.Logger
module_config, logger = get_module_config(__name__)


def main():
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description="Example script to parse command line arguments.")

    # 添加命令行参数
    parser.add_argument("-s", "--screen-name", type=str, help="the screen name of the user, this is a unique name with a prefix '@' which is displayed at the user's homepage, and your input should not include the symbol '@'")
    parser.add_argument("-u", "--user-id", type=str, help="the rest id of the user")
    parser.add_argument("-r", "--twitter-id", type=str, help="the rest id of the twitter you wanted to download")
    parser.add_argument("-t", "--type", type=str, help="the user info type you wanted to downloaded, all supported types: favorite, tweeted")
    parser.add_argument("-d", "--target-dir", type=str, help="the target dir for saving infomation")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    screen_name = args.screen_name if args.screen_name != None else module_config.get("screen_name")
    user_id = args.user_id if args.user_id != None else module_config.get("user_id")
    twitter_id = args.twitter_id if args.twitter_id != None else module_config.get("twitter_id")
    download_type = args.type if args.type != None else module_config.get("download_type")
    twitter_download_dir = args.target_dir if args.target_dir != None else module_config.get("twitter_download_dir")
    tweeted_download_dir = args.target_dir if args.target_dir != None else module_config.get("tweeted_download_dir")
    favorite_download_dir = args.target_dir if args.target_dir != None else module_config.get("favorite_download_dir")

    if twitter_id != None:
        logger.info("Download twitter info with twitter id [{}]. Target dir is [{}].".format(twitter_id, twitter_download_dir))
        download_by_twitter_id(twitter_id, twitter_download_dir)
    elif download_type == None:
        logger.info("No type is specified, supported values: favorite, tweeted.")
        exit(-1)
    elif screen_name != None:
        if download_type.lower() == "tweeted":
            logger.info("Download [{}] info with screen name [{}]. Target dir is [{}].".format(download_type, screen_name, tweeted_download_dir))
            download_tweeted_by_screen_name(screen_name, tweeted_download_dir)
        elif download_type.lower() == "favorite":
            logger.info("Download [{}] info with screen name [{}]. Target dir is [{}].".format(download_type, screen_name, favorite_download_dir))
            download_favorite_by_screen_name(screen_name, favorite_download_dir)
        else:
            logger.error("Invalid type of [{}], supported values: favorite, tweeted.".format(download_type))
            exit(-1)
    elif user_id != None:
        if download_type.lower() == "tweeted":
            logger.info("Download [{}] info with user id [{}]. Target dir is [{}].".format(download_type, user_id, tweeted_download_dir))
            download_tweeted_by_user_id(screen_name, tweeted_download_dir)
        elif download_type.lower() == "favorite":
            logger.info("Download [{}] info with user id [{}]. Target dir is [{}].".format(download_type, user_id, favorite_download_dir))
            download_favorite_by_user_id(screen_name, favorite_download_dir)
        else:
            logger.error("Invalid type of [{}], supported values: favorite, tweeted.".format(download_type))
            exit(-1)
    else:
        logger.error("At least one args of --twitter-id, --screen-name, --user-id are required.")
        exit(-1)


def download_tweeted_by_screen_name(screen_name: str, target_dir: str):
    downloader = CommonDownloader()
    user_page = UserInfoPage(downloader)
    user_info = user_page.get_info(screen_name)
    rest_id = user_info.get("rest_id")
    download_tweeted_by_user_id(rest_id, target_dir)

        
def download_tweeted_by_user_id(user_id: str, target_dir: str):
    downloader = CommonDownloader()
    page = TweetedTweetPage(downloader)
    twitter_info_list = page.get_info(user_id)
    saver = EfficientTwitterSaver(downloader, ResourceDataManager(AbstractDb.get_default_database()), target_dir = os.path.join(target_dir, user_id))
    for twitter_info in twitter_info_list:
        saver.save(twitter_info)
        
        
def download_favorite_by_screen_name(screen_name: str, target_dir: str):
    downloader = CommonDownloader()
    user_page = UserInfoPage(downloader)
    user_info = user_page.get_info(screen_name)
    rest_id = user_info.get("rest_id")
    download_favorite_by_user_id(rest_id, target_dir)

        
def download_favorite_by_user_id(user_id: str, target_dir: str):
    downloader = CommonDownloader()
    page = FavoriteTweetPage(downloader)
    twitter_info_list = page.get_info(user_id)
    saver = EfficientTwitterSaver(downloader, ResourceDataManager(AbstractDb.get_default_database()), target_dir = os.path.join(target_dir, user_id))
    for twitter_info in twitter_info_list:
        saver.save(twitter_info)
        
def download_by_twitter_id(twitter_id: str, target_dir: str):
    downloader = CommonDownloader()
    page = TwitterInfoPage(downloader)
    twitter_info_list = page.get_info(twitter_id)
    saver = EfficientTwitterSaver(downloader, ResourceDataManager(AbstractDb.get_default_database()), target_dir = os.path.join(target_dir, twitter_id))
    for twitter_info in twitter_info_list:
        saver.save(twitter_info)

if __name__ == "__main__":
    main()