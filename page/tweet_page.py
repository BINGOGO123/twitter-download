from . import logger
from tool.decorators import LoggerWrapper
from abc import abstractmethod
from .common_page import AbstractPage

class AbstractTweetPage(AbstractPage): 
    @LoggerWrapper(logger)
    def get_info(self, rest_id: str, limited_count: int = 999999999) -> list:
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
                response_json = self.downloader.get_tw_response_json_by_url(next_url)
                response_info = self.parse_response_info(response_json)
                next_url = self.get_next_url(rest_id, response_info)
                current_entry_info = self.get_valid_response_info(response_info)
                all_entry_info += current_entry_info
                # 打印本页所有信息数量
                logger.info("The count of current round is {}, all count is {}".format(len(current_entry_info), len(all_entry_info)))
                # 如果本页没有了，则终止
                if len(current_entry_info) == 0:
                    break
                # 如果目前数量已经超过上限，则终止
                if len(all_entry_info) >= limited_count:
                    logger.info("Current count {} has exceeded the limited count {}. terminated.".format(len(current_entry_info), limited_count))
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
    def parse_response_info(self, data: dict) -> dict:
        """解析response

        Args:
            data (dict): response

        Returns:
            dict: 解析后的结果
        """
        pass
    


    def get_valid_response_info(self, response_info: dict) -> dict:
        """获取有效的信息

        Args:
            response_info (dict): response的解析结果

        Returns:
            dict: 有效结果
        """
        return response_info[:-2]
