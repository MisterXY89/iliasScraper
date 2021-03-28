
import os
import sys
import glob
import click
from pathlib import Path
from colorama import Fore, Back, Style

from .scraper import Scraper
from .auth_manager import remove_pwd

CONFIG_FILE = ".config"
HOME = str(Path.home())
PATH = os.path.join(HOME, ".iliasScraper")

version_path = os.path.join(os.path.dirname(__file__),"VERSION")

with open(version_path) as f:
    line = f.readline()
    __version__ = line

@click.group()
@click.version_option(__version__)
def main():
    """CLI for the ilias-scraper"""
    if not os.path.exists(PATH):
        os.makedirs(PATH)


@main.command()
@click.option("-u", '--url', help='Ilias course url', required=True)
@click.option("-n", '--username', help='Your Ilias username', required=True)
@click.option("-c", '--course-name', help='The name of the course, will be used as the name of this scraper', required=True)
@click.option("-d", '--target-dir', help="The ABSOLUTE path for this course folder", required=False)
# @click.option('--ignore', help="Files you want to ignore, seperated by ,")
def create(url, username, course_name, target_dir):
    """
    Create a new scraper with a url and name
    """
    # ignore = ignore.split(",")
    scraper_source = f"""
import sys
from iliasScraper import scraper
if len(sys.argv) == 2:
    skip = sys.argv[1]

user = '{username}'
sc = scraper.Scraper(url='{url}', name='{course_name}', target_dir='{target_dir}')
sc.setup(user)
sc.run()"""
    if course_name == None:
        print("please use ")
        return 0
    course_name = course_name.replace(" ", "_")
    with open(f"{PATH}/{course_name}.py", "w") as scraper_file:
        scraper_file.write(scraper_source)
    print(Fore.GREEN + f"Scraper {course_name} has been created!")


@main.command()
@click.option("-n", '--name', help='Name of the scraper', required=True)
@click.option("-s", '--skip', help='Skip existing files, default=True', required=False)
@click.option("-e", '--fallback-extension', required=False)
def run(name, skip=True, fallback_extension="txt"):
    """
    Run a previously created scraper, name can be specified with
    and without the .py ending
    """
    scraper_file = f"{PATH}/{name}"
    if not ".py" in scraper_file:
        scraper_file += ".py"
    if not os.path.exists(scraper_file):
        print(Fore.RED + "The specified name does not match any configured scrapers.")
        print("Use <<iliasScraper list>> to list all current scrapers.")
        return 0
    os.system(f"python3 {scraper_file} {skip}")

@main.command()
def list(**kwargs):
    """
    List all existing scraper
    """
    files = [f for f in glob.glob(PATH+"/*.py", recursive=True)]
    if not files:
        print(Fore.RED+"There are no scrapers configured."+Style.RESET_ALL)
        return 0
    print(Fore.BLUE + "Currently configured scrapers:"+Style.RESET_ALL)
    for f in files:
        filename_printable = f.split("/")[-1:][0]
        print(f"- {filename_printable}")


@main.command()
@click.option('--username', required=True)
def remove_password(username):
    """
    Remove the stored password
    """
    remove_pwd(username)
    print(Fore.RED + f"Password for {username} has been removed!")

if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print(Fore.BLUE + "ILIAS SCRAPER")
        print(Style.RESET)
        print(Style.DIM + "scraper for ilias platform of of the uni constance")
        print("create a scraper via <create> <url> <title> or run via <run> <name>")
    main()
