from .page import Page
from downloader.common_downloader import CommonDownloader
from downloader.downloader import Downloader
from err.err import *

class AbstractPage(Page):
    def __init__(self, **kwargs):
        downloader = kwargs.get("downloader", CommonDownloader())
        if not isinstance(downloader, Downloader):
            raise ArgsException("The type of args 'downloader' is not downloader.Download")
        self.downloader: Downloader = downloader
