
import re
from tqdm import tqdm
from colorama import Fore, Back, Style

class FileParser:
    """
    docstring for FileParser.
    """

    def __init__(self, request_handler):
        self.parser = 'html.parser'
        self.ignore = ["weblink", "test", "forum", "übung", "inhaltsseite"]
        self.file_id = "datei"
        self.folder_id = "ordner"
        self.current_path = "/"
        self.dir_dict = {}
        self.done_folders = []
        self.folder_todo = []
        self.todo_folders_index = 0
        self.layer = 0
        self.request_handler = request_handler
        self.all_urls = []


    def filter_ignored(self, img_list):
        def filter_(title):
            return any(map(lambda el: el in title.lower(), self.ignore))
        return [tag for tag in img_list if not filter_(tag["title"])]

    def _extract_href(self, img):
        return img.parent["href"]

    def _pathify_folder_name(self, folder_name):
        folder_name = "_".join(folder_name.split(" "))
        folder_name = "_".join(folder_name.split("|"))
        folder_name = "_".join(folder_name.split("'"))
        folder_name = re.sub("_+", "_", folder_name)
        return folder_name

    def _extract_file_name(self, img):
        return img.parent.parent.parent.find_all("a")[1].text

    def update_dir_dict(self, img_list, path):
        """
        """
        dir_dict = {}
        for img in img_list:
            img_title = img["title"].lower()
            if self.file_id in img_title:
                # todo: split current path and thus create real sub dicts
                if not path in dir_dict:
                    dir_dict[path] = []
                dir_dict[path].append({
                        "url": self._extract_href(img),
                        "file_name": self._extract_file_name(img)
                        })
        return dir_dict

    def get_all_urls(self, url):
        soup = self.request_handler.get_soup(url)
        links = soup.find_all('a')
        if links is None or len(links) == 0 or url in self.all_urls:
            self.all_urls.append(url)
            return 1
        else:
            if "fold" in url:
                self.all_urls.append(url)
                print(Style.DIM + url)
            for link in links:
                if not link.has_attr("href"):
                    continue
                href = link['href']
                if "https" in href and "fold" in href:
                    self.get_all_urls(href)
        return list(set(self.all_urls))

    def extract_path_from_breadcrumb(self, breadcrumb_string):
        total_path_list = breadcrumb_string.split("\n")
        split_index = list(map(lambda item: "Lehrveranstaltung" in item, total_path_list)).index(True)
        path_list = total_path_list[split_index+1:][:-1]
        return path_list

    def parse(self, soup, url="/"):


        breadcrumb_string = soup.find_all("ol", class_="breadcrumb")[0].text
        path = "/".join(list(map(lambda x: self._pathify_folder_name(x),
                        self.extract_path_from_breadcrumb(breadcrumb_string))))


        all_img_tags = soup.find_all("img", class_="ilListItemIcon")
        f_img_tags = self.filter_ignored(all_img_tags)

        dir_dict = self.update_dir_dict(f_img_tags, path)

        return dir_dict
