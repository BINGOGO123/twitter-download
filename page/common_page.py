from .page import Page
from downloader.downloader import Downloader
from err.err import *

class AbstractPage(Page):
    def __init__(self, downloader: Downloader):
        self.downloader = downloader
