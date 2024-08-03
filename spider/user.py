import sys
import requests
from configs.config import headers
from . import logger
from tool.decorators import LoggerWrapper
from tool.tool import get_formatted_json_str
from .parse import get_user_info_from_user_response

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
        user_info_response = result.json()
        return get_user_info_from_user_response(user_info_response)
    except Exception as ex:
        logger.exception(ex)
        return {}


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        logger.error("Please input screen_name of the user")
        exit(-1)
    screen_name = sys.argv[1]
    user_info = get_user_info(screen_name)
    print(get_formatted_json_str(user_info))