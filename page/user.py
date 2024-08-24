import sys
from . import logger
from tool.tool import get_formatted_json_str
from .single_page import AbstractSinglePage
from err.err import *
from downloader.common_downloader import CommonDownloader
from parser.user_parser import UserParser


class UserInfoPage(AbstractSinglePage):
    def get_url(self, *args):
        if len(args) == 0:
            raise ArgsException("At least one arg required")
        if not isinstance(args[0], str):
            raise ArgsException("The first arg must be str")
        return 'https://x.com/i/api/graphql/-0XdHI-mrHWBQd8-oLo1aA/ProfileSpotlightsQuery?variables={"screen_name":"' + args[0] + '"}'


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        logger.critical("Please input screen_name of the user")
        exit(-1)
    screen_name = sys.argv[1]
    downloader = UserInfoPage(CommonDownloader(), UserParser())
    user_info = downloader.get_info(screen_name)
    print(get_formatted_json_str(user_info))