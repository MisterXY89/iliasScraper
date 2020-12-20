
import requests

from .ilias_exceptions import LoginFailedError
from .config import LOGIN_POST_URL
from .auth_manager import get_pwd

class LoginHandler:
    """
    Handle login with
    """

    def __init__(self, username):
        self.payload = {
                "username": username,
                "password": get_pwd(),
                "cmd[doStandardAuthentication]": "Anmelden"
        }
        self.session = requests.Session()

    def login(self):
        with self.session as session_r:
            login_resp = session_r.post(LOGIN_POST_URL, data=self.payload)
            if login_resp.status_code != 200:
                raise LoginFailedError(f"Login failed with status_code {login_resp.status_code}")
        return session_r
