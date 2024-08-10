from page.tweeted import TweetedTweetPage
from downloader.common_downloader import CommonDownloader
from page.user import UserInfoPage
from persistence.efficient_twitter_saver import EfficientTwitterSaver
from data_manager.resource_data_manager import ResourceDataManager
from database.abstract_db import AbstractDb
import sys

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Please input screen name")
        exit(-1)
    screen_name = sys.argv[1]
    downloader = CommonDownloader()
    tweeted_page = TweetedTweetPage(downloader)
    user_page = UserInfoPage(downloader)
    user_info = user_page.get_info(screen_name)
    rest_id = user_info.get("rest_id")
    twitter_info_list = tweeted_page.get_info(rest_id)
    saver = EfficientTwitterSaver(downloader, ResourceDataManager(AbstractDb.get_default_database()), target_dir = "./new_target/{}/tweeted/".format(rest_id))
    for twitter_info in twitter_info_list:
        saver.save(twitter_info)
    