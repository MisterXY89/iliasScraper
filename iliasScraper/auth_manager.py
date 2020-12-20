
# -*- coding: utf-8 -*-

import sys
import getpass
import keyring
from .config import SCRAPER_NAME
from colorama import Fore, Back, Style

PASSWORD = ""

def store_pwd(pwd,username):
	keyring.set_password(SCRAPER_NAME, username, pwd)

def read_pwd(username):
	return keyring.get_password(SCRAPER_NAME, username)

def set_auth(username):
	global PASSWORD

	if read_pwd(username) != None:
		PASSWORD = read_pwd(username)
	else:
		print(Fore.RED + "For your first run you have to set a password, you can choose to store it or enter it for every run." + Style.RESET_ALL)
		print(">> Please enter your password: ")
		PASSWORD = getpass.getpass()
		print(">> Would you like to store the password encrpyted for the future? [y/N]")
		should_store = str(sys.stdin.readline()[:-1])
		if should_store == "y":
			store_pwd(PASSWORD, username)

def remove_pwd(username):
	keyring.delete_password(SCRAPER_NAME, username)

def get_pwd():
	return PASSWORD
