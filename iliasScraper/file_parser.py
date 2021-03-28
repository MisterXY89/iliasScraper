
import re
from tqdm import tqdm
from colorama import Fore, Back, Style

class FileParser:
    """
    docstring for FileParser.
    """

    def __init__(self, request_handler, skip_existing_files=True, existing_files=[]):
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
        self.skip_existing_files = skip_existing_files
        self.existing_files = existing_files


    def filter_ignored(self, img_list):
        def filter_(title):
            return any(map(lambda el: el in title.lower(), self.ignore))
        return [tag for tag in img_list if not filter_(tag["title"])]

    def _extract_href(self, img):
        element = list(img.parent.parent.find_all("a"))[0]
        return element["href"]

    def _pathify_folder_name(self, folder_name):
        folder_name = "_".join(folder_name.split(" "))
        folder_name = "_".join(folder_name.split("|"))
        folder_name = "_".join(folder_name.split("'"))
        folder_name = "_".join(folder_name.split(":"))
        folder_name = re.sub("_+", "_", folder_name)
        return folder_name

    def _extract_file_name(self, img):
        # why was index = 1 ????
        element = list(img.parent.parent.parent.find_all("a"))[0]
        return element.text

    def _extract_symbol_name(self, a_tag):
        imgs = a_tag.find_all("img")
        if imgs:
            return str(imgs[0]["title"].lower())
        return ""

    def update_dir_dict(self, img_list, path):
        """
        """
        dir_dict = {}
        for img in img_list:
            img_title = img["title"].lower()
            # print(f"{img_title=}")
            if self.file_id in img_title:
                if not path in dir_dict:
                    dir_dict[path] = []
                filename = self._extract_file_name(img)
                # print(f"{filename=}")
                if self.skip_existing_files and filename in self.existing_files:
                    print("continue")
                    continue
                dir_dict[path].append({
                        "url": self._extract_href(img),
                        "file_name": filename
                        })
        return dir_dict

    def _is_sitzung(self, tag, soup, add_q=False):
        if add_q:
            sitzungen = soup.find_all("img", title="Symbol Sitzung")
            sitzungen_no = len(sitzungen)
            if sitzungen_no == 1:
                return True
            return False

        img = tag.parent.parent.parent.parent.parent.find_all("img", class_="ilListItemIcon")
        if img:
            img = img[0]
            title = img["title"].lower()
            if "sitzung" in title or "session" in title:
                return True
        return False

    def get_all_urls(self, url):
        # print(40*"~")
        # print(f"{url=}")
        soup = self.request_handler.get_soup(url)
        links = soup.find_all('a', class_="il_ContainerItemTitle")
        if not links or url in self.all_urls:
            self.all_urls.append(url)
            return 1
        else:
            sitzung_q = self._is_sitzung(url, soup=soup, add_q=True)
            # print(f"{sitzung_q=}")
            if "fold" in url or sitzung_q:
                self.all_urls.append(url)
                print(Style.DIM + url + Style.RESET_ALL)
            for link in links:
                if not link.has_attr("href") or link in self.all_urls:
                    continue
                href = link['href']
                if not "https" in href:
                    href = f"https://ilias.uni-konstanz.de/ilias/{href}"

                if "fold" in href or self._is_sitzung(link, soup=soup):
                    self.get_all_urls(href)

        return list(set(self.all_urls))

    def extract_path_from_breadcrumb(self, breadcrumb_string):
        total_path_list = breadcrumb_string.split("\n")
        split_index = list(map(lambda item: "Lehrveranstaltung" in item, total_path_list)).index(True)
        path_list = total_path_list[split_index+1:][:-1]
        return path_list

    def parse(self, soup):
        breadcrumb_string = soup.find_all("ol", class_="breadcrumb")
        if not breadcrumb_string:
            return {}
        breadcrumb_string = breadcrumb_string[0].text
        path = "/".join(list(map(lambda x: self._pathify_folder_name(x),
                        self.extract_path_from_breadcrumb(breadcrumb_string))))

        # ilContainerListItemOuter
        # - ilContainerListItemIcon
        # - ilContainerListItemContent

        all_img_tags = soup.find_all("img", class_="ilListItemIcon")
        f_img_tags = self.filter_ignored(all_img_tags)

        dir_dict = self.update_dir_dict(f_img_tags, path)

        return dir_dict
