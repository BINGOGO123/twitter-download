import sys
from . import logger
from tool.tool import get_formatted_json_str
from .parse import get_user_info_from_user_response
from .single_page import AbstractSinglePage
from err.err import *


class UserInfoPage(AbstractSinglePage):
    def get_url(self, *args):
        if len(args) == 0:
            raise ArgsException("At least one arg required")
        if not isinstance(args[0], str):
            raise ArgsException("The first arg must be str")
        return 'https://x.com/i/api/graphql/-0XdHI-mrHWBQd8-oLo1aA/ProfileSpotlightsQuery?variables={"screen_name":"' + args[0] + '"}'
    
    def parse_response_info(self, data: dict) -> dict:
        return get_user_info_from_user_response(data)


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        logger.error("Please input screen_name of the user")
        exit(-1)
    screen_name = sys.argv[1]
    downloader = UserInfoPage()
    user_info = downloader.get_info(screen_name)
    print(get_formatted_json_str(user_info))