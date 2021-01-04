
import os
from tqdm import tqdm
from colorama import Fore, Back, Style

from .login_handler import LoginHandler
from .file_parser import FileParser
from .request_handler import RequestHandler
from .download_handler import DownloadHandler


class Controller:
    """
    The controller of the package - here comes everything together
    """

    def __init__(self, username, target_dir, ignore):
        self.request_handler = RequestHandler()
        self._check_version()
        self.username = username
        self.target_dir = target_dir
        self.ignore_endings = ignore
        self.login_handler = LoginHandler(self.username)
        self.test_course_url = "https://ilias.uni-konstanz.de/ilias/goto_ilias_uni_crs_1078392.html"
        self.test_file1 = "https://ilias.uni-konstanz.de/ilias/goto_ilias_uni_file_1078407_download.html"
        self.test_file2 = "https://ilias.uni-konstanz.de/ilias/goto_ilias_uni_file_1091580_download.html"

    def _check_version(self):
        version_path = os.path.join(os.path.dirname(__file__),"VERSION")
        with open(version_path) as f:
            line = f.readline()
            local_version = line.replace("\n", "")
        remote_version = self.request_handler.get_version()
        if remote_version != local_version:
            print(Fore.RED + Style.BRIGHT + Back.BLACK \
            + f"You are using version {local_version}, however version {remote_version} is available.\n" \
            + "THIS VERSION IS DEPRECATED AND POSSIBLY UNSTABLE.\n" \
            + "PLEASE UPDATE VIA:\n" \
            + Style.NORMAL + Fore.BLACK + Back.WHITE \
            + "pip install iliasScraper --upgrade" + Style.RESET_ALL \
            + "\n"+(50*"-")+"\n")

    def collect(self, url):
        file_dict = {}
        print(">> Getting all folder and session urls...")
        all_urls = self.file_parser.get_all_urls(url)#.append(url)
        all_urls.append(url)
        print(Style.RESET_ALL)
        for link in all_urls:
            soup = self.request_handler.get_soup(link)
            file_dict_for_link = self.file_parser.parse(soup)
            file_dict.update(file_dict_for_link)
        return file_dict

    def init_controller(self):
        self.session = self.login_handler.login()
        self.request_handler.init_session(self.session)
        self.file_parser = FileParser(self.request_handler)
        self.download_handler = DownloadHandler(self.request_handler, self.target_dir)

    def download(self, url, name="course name"):
        print(Fore.BLUE + "\t\t ILIAS SCRAPER")
        print(Fore.GREEN + f" - {name} -")
        print(Style.RESET_ALL)
        files = self.collect(url)
        print(">> Starting download")
        for path in files.keys():
            files_for_path = files[path]
            print(Style.DIM + path)
            for file in files_for_path:
                print(file["file_name"])
                self.download_handler.download(file, path, self.ignore_endings)

    def test(self):
        self.download_handler.download({"url":self.test_file2, "file_name":"testfile"}, "")


# controller = Controller("tilman.kerl", "", ignore="None")
# controller.init_controller()
# controller.download(controller.test_course_url, "bsc")
# controller.test()
