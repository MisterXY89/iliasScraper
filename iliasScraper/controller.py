
import pprint
from tqdm import tqdm
from colorama import Fore, Back, Style

from .login_handler import LoginHandler
from .file_parser import FileParser
from .request_handler import RequestHandler
from .download_handler import DownloadHandler

pp = pprint.PrettyPrinter(indent=4)

class Controller:
    """
    The controller of the package - here comes everything together
    """

    def __init__(self, username):
        self.username = username
        self.login_handler = LoginHandler(self.username)
        self.test_course_url = "https://ilias.uni-konstanz.de/ilias/goto_ilias_uni_crs_1078392.html"
        self.test_file1 = "https://ilias.uni-konstanz.de/ilias/goto_ilias_uni_file_1078407_download.html"
        self.test_file2 = "https://ilias.uni-konstanz.de/ilias/goto_ilias_uni_file_1091580_download.html"

    def collect(self, url):
        file_dict = {}
        print(">> Getting all folder urls...")
        all_urls = self.file_parser.get_all_urls(url)#.append(url)
        all_urls.append(url)
        print(Style.RESET_ALL)
        for link in all_urls:
            soup = self.request_handler.get_soup(link)
            file_dict_for_link = self.file_parser.parse(soup, url=self.test_course_url)
            file_dict.update(file_dict_for_link)
        return file_dict

    def init_controller(self):
        self.session = self.login_handler.login()
        self.request_handler = RequestHandler(self.session)
        self.file_parser = FileParser(self.request_handler)
        self.download_handler = DownloadHandler(self.request_handler)

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
                self.download_handler.download(file, path)

    def test(self):
        self.download_handler.download({"url":self.test_file2, "file_name":"testfile"}, "")


# controller = Controller(controller.test_course_url,
# name="Bachelor-Seminar Datenanalyse und Visualisierung | Master's Seminar Data Analysis and Visualization")
# controller.download()
# controller.test()
