"""
interface for user & comandline tool
"""

from colorama import Fore, Back, Style

from .controller import Controller
from .auth_manager import set_auth, remove_pwd

class Scraper:
    """
    docstring for Scraper.
    """

    def __init__(self, url="", name="", target_dir="/", ignore=[], skip_existing_files=True):
        self.url = url
        self.name = name.replace(" ", "_").lower()
        self.target_dir = target_dir
        self.ignore = ignore
        self.skip_existing_files = skip_existing_files

    def setup(self, username=""):
        if not username or not "." in username:
            print(Fore.BLUE + "ILIAS SCRAPER" + Style.RESET_ALL)
            print(Style.DIM + "You did not specicy a username so please to it now." + Style.RESET_ALL)
            self.username = input(">> Enter your username: ")
        else:
            self.username = username
        set_auth(username)
        self.controller = Controller(self.username, self.target_dir, self.skip_existing_files, self.ignore)

    def run(self):
        self.controller.init_controller()
        self.controller.download(self.url, name=self.name)

    def remove_password(self, username):
        remove_pwd(username)
