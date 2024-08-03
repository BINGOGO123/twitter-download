from . import logger
from tool.decorators import LoggerWrapper
import requests
from abc import abstractmethod

class Tweet:
    def __init__(self, headers):
        self.headers = headers
        
    @LoggerWrapper(logger)
    def get_all_info(self, rest_id: str) -> list:
        """获取一个用户所有twitter信息

        Args:
            rest_id (str): 用户的rest id

        Returns:
            list: 该用户的所有推文信息
        """
        try:
            next_url = self.get_base_url(rest_id)
            all_entry_info = []
            counter = 1
            while next_url != None:
                logger.info("Round :{}".format(counter))
                counter += 1
                entry_info = self.get_info_by_url(next_url)
                next_url = self.get_next_url(rest_id, entry_info)
                current_entry_info = entry_info[:-2]
                all_entry_info += current_entry_info
                # 打印本页所有信息数量
                logger.info("The count of current round is {}, all count is {}".format(len(current_entry_info), len(all_entry_info)))
                # 如果本页没有了，则终止
                if len(current_entry_info) == 0:
                    break
            return all_entry_info
        except Exception as ex:
            logger.exception(ex)
            return []


    def get_next_url(self, rest_id: str, entry_info: list) -> str:
        """获取下一页的url

        Args:
            rest_id (str): 用户id
            entry_info (list): 上一轮获取的信息

        Returns:
            str: 下一页的url
        """
        url_prefix, url_suffix = self.get_url_prefix_suffix(rest_id)
        if len(entry_info) > 0:
            cursor: str = entry_info[-1].get("content_info", {}).get("cursor", None)
            if cursor != None and cursor.strip() != "":
                return url_prefix + '"cursor":"{}",'.format(cursor) + url_suffix
        return None


    def get_base_url(self, rest_id: str) -> str:
        """获取起始url

        Args:
            rest_id (str): 用户id

        Returns:
            str: 起始url
        """
        return "".join(self.get_url_prefix_suffix(rest_id))


    @LoggerWrapper(logger)
    def get_info_by_url(self, url: str) -> dict:
        """通过url获取tw信息

        Args:
            url (str): url

        Returns:
            list: tw信息列表
        """
        try:
            result = requests.get(url, headers = self.headers)
            twitter_result = result.json()
            entries = self.get_entries(twitter_result)
            entry_info_list = self.get_entry_info_list(entries)
            return entry_info_list
        except Exception as ex:
            logger.exception(ex)
            return []


    @abstractmethod
    def get_url_prefix_suffix(self, rest_id: str) -> tuple:
        """获取url的前后缀

        Args:
            rest_id (str): 用户id

        Returns:
            tuple: (url前缀, url后缀)
        """
        pass


    @abstractmethod
    def get_entry_info_list(self, entries: list) -> list:
        """将entries转为entry_info_list

        Args:
            entries (list): entries

        Returns:
            list: entry_info_list
        """
        pass


    @abstractmethod
    def get_entries(self, twitter_result: dict) -> list:
        """从response中获取所有entries

        Args:
            twitter_result (dict): response

        Returns:
            list: entry列表
        """
        pass
        