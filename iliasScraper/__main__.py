import sys
import glob
import click
from colorama import Fore, Back, Style

from .scraper import Scraper

config_file = ".config"

@click.group()
@click.version_option("1.0.0")
def main():
    """CLI for the ilias-scraper"""

@main.command()
@click.argument('path', required=True)
def config(**kwargs):
    path = kwargs.get(path)
    with open(config_file, "wb") as cf_file:
        cf_file.write(path)

@main.command()
@click.argument('url', required=True)
@click.argument('username', required=True)
@click.argument('course_name', required=True)
def create(**kwargs):
    """
    Create a new scraper with a url and name
    """
    url = kwargs.get("url")
    course_name = kwargs.get("course_name")
    username = kwargs.get("username")
    scraper_source = f"""
from iliasScraper import scraper
user = "tilman.kerl"
sc = scraper.Scraper(url='{url}', name='{course_name}')
sc.setup({username})
sc.run()
    """
    with open(f"{course_name}.py", "w") as scraper_file:
        scraper_file.write(scraper_source)


@main.command()
@click.argument('name', required=False)
def run(**kwargs):
    """
    Run a previously created scraper
    """
    with open(config_file, "rb") as cf_file:
        path = cf_file.read(path)
    files = [f for f in glob.glob(path + "*.py", recursive=True)]
    for f in files:
        print(f)

@main.command()
def show(**kwargs):
    """
    Run a previously created scraper
    """
    click.echo(kwargs)
    pass


@main.command()
@click.argument('username', required=True)
def reset_password(**kwargs):
    """
    Run a previously created scraper
    """
    username = kwargs.get("username")
    reset_pwd(username)
    print(f"Password for user {username} has been removed.")

if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print(Fore.BLUE + "ILIAS SCRAPER")
        print(Style.RESET)
        print(Style.DIM + "scraper for ilias platform of of the uni constance")
        print("create a scraper via <create> <url> <title> or run via <run> <name>")
    main()
