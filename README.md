# iliasScraper: revised

iliasScraper is as the name already states, a web scraper which downloads your
materials from any Ilias course. Designed for the university Constance and written in python. <br>
**The folder structure from the Ilias course is kept!** <br>
My initial approach can be found here: [MisterXY89/iliasSpider](https://github.com/MisterXY89/iliasSpider). However this is outdated and doesn't really work anymore. Further it lacked the keep-structure and recursively
finding all folders features.
This time I am not using scrapy but instead simply going for
the old `request` and `bs4` or with headless selenium.

For password storing I'll be using the keyring package.

**Currently only linux-systems are supported.**

## Install

`pip3 install iliasScraper`
or clone, cd into folder and `pip3 install .`.

## Usage
There are two modes: the *package* and the *cli* mode. Both modes download all files for the respective course in the current directory.

### Package

```python
from iliasScraper import scraper

# your Ilias username, without the @uni-konstanz.de ending
username = "tilman.kerl"
# this is used to identify and later run the configured scraper
course_name = "Bsc Seminar" # -> will be changed to bsc_seminar
# your course url
url = "https://ilias.uni-konstanz.de/ilias/goto_ilias_uni_crs_1078392.html"

sc = scraper.Scraper(url=url, name=course_name)

# setup your scraper, on your first usage you will be asked for a password
# if the user is set to "" or something not valid, you will be prompted
# an input to enter your username
sc.setup(username)

# this then runs the scraper and downloads all files and folders in the
# current directory
sc.run()

# if you choose to store your password previously and want to remove it,
# you can simply to so via
sc.remove_password(username)
```


### CLI
```bash
Usage: iliasScraper [OPTIONS] COMMAND [ARGS]...

  CLI for the ilias-scraper

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  create           Create a new scraper with a url and name
  list             List all existing scraper
  remove-password  Remove the stored password
  run              Run a previously created scraper.
```
**Example usage:**
```bash
# create a new scraper like this, the name will be changed to "bsc_seminar"
# the scraper will be stored in ~/.iliasScraper/
$ iliasScraper create --url https://ilias.uni-konstanz.de/ilias/goto_ilias_uni_crs_1078392.html --username tilman.kerl --course-name "bsc seminar"
> Scraper 'bsc_seminar' has been created!
# you can now run the scraper via
$ iliasScraper run --name bsc_seminar
# to list all currently configured scraper
$ iliasScraper list
> Currently configured scrapers:
> - bsc_seminar.py
# if you choose to store your password previously and want to remove it,
# you can simply to so via
$ iliasScraper remove-password --username tilman.kerl
> The password for tilman.kerl has been removed!
```



## Requirements
```
bs4
requests
fleep
tqdm
colorama
```
