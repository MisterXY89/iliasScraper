
import requests
from bs4 import BeautifulSoup

class RequestHandler:
    """
    docstring for RequestHandler.
    """

    def __init__(self):
        self.parser = "html.parser"

    def init_session(self, session):
        self.session = session

    def get_soup(self, url):
        if not self.session:
            return False
        try:
            response = self.session.get(url)
        except Exception as err:
            print(f"Error: {err}")
            # raise err
            print(f"WITH FOLLOWING URL: {url=}")
            raise err
            return False
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, self.parser)
            # print(f"OK! Url: {url}")
            return soup
        else:
            print(f'Something went wrong. Got the following response code: {response.status_code}')
            return None

    def get_file(self, url):
        if not self.session:
            return False
        try:
            response = self.session.get(url, allow_redirects=True)
        except Exception as err:
            print(f"Error: {err}")
            print(f"With the following: {url=}")
            raise err
            return False
        if response.status_code == 200:
            return response
        else:
            print(f'Something went wrong. Got the following response code: {response.status_code}')
            return None

    def get_version(self):
        try:
            response = requests.get("https://raw.githubusercontent.com/MisterXY89/iliasScraper/main/iliasScraper/VERSION")
        except Exception as err:
            print(f"Error: {err}")
            print(f"With the following: {url=}")
            raise err
            return False
        if response.status_code == 200:
            return response.text.replace("\n", "")
        else:
            print(f'Something went wrong. Got the following response code: {response.status_code}')
            return None
