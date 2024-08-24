from .page import Page
from downloader.downloader import Downloader
from err.err import *
from parser.parser import Parser

class AbstractPage(Page):
    def __init__(self, downloader: Downloader, parser: Parser):
        self.downloader = downloader
        self.parser = parser
