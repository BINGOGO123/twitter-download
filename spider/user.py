import sys
import requests
from configs.config import headers
import json
from . import logger
from tool.decorators import LoggerWrapper

@LoggerWrapper(logger)
def get_user_info(screen_name: str) -> dict:
    """根据用户的screen_name查询用户信息

    Args:
        screen_name (str): 用户的唯一标识ID

    Returns:
        dict: 用户信息，包含name,screen_name,rest_id三个字段
    """
    try:
        url = 'https://x.com/i/api/graphql/-0XdHI-mrHWBQd8-oLo1aA/ProfileSpotlightsQuery?variables={"screen_name":"' + screen_name + '"}'
        result = requests.get(url, headers = headers)
        user_info_result = result.json()
        user_info = {}
        if user_info_result.get("data") != None:
            if user_info_result.get("data").get("user_result_by_screen_name") != None:
                if user_info_result.get("data").get("user_result_by_screen_name").get("result") != None:
                    user_info["rest_id"] = user_info_result.get("data").get("user_result_by_screen_name").get("result").get("rest_id")
                    if user_info_result.get("data").get("user_result_by_screen_name").get("result").get("legacy") != None:
                        user_info["name"] = user_info_result.get("data").get("user_result_by_screen_name").get("result").get("legacy").get("name")
                        user_info["screen_name"] = user_info_result.get("data").get("user_result_by_screen_name").get("result").get("legacy").get("screen_name")
        return user_info
    except Exception as ex:
        logger.error(ex)
        return {}

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        logger.error("Please input screen_name of the user")
        exit(-1)
    screen_name = sys.argv[1]
    user_info = get_user_info(screen_name)
    print(json.dumps(user_info, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))