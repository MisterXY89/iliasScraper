# iliasScraper: revised

iliasScraper is as the name already states, a web scraper which downloads your
materials from any Ilias course. Designed for the university Constance and written in python. <br>
**The folder structure from the Ilias course is kept!** <br>
My initial approach can be found here: [MisterXY89/iliasSpider](https://github.com/MisterXY89/iliasSpider). However this is outdated and doesn't really work anymore. Further this scraper
now supports:
  - keep-structure of the ilias course
  - recursively finding all folders, not only custom specified ones
  - specicy a target dir
  - CLI and package mode
  - file extension detection  

This package uses the old `request` and `bs4`, instead of `scrapy`.

*There is a fork of my old approach [mawenzy/iliasSpider](https://github.com/mawenzy/iliasSpider)
which is actively maintained, if you prefer scrapy.*

For password storing I'll be using the `keyring` package.

**The CLI-mode does currently only support linux-systems.**

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

# if target_dir is not set, the current path is used
# an absolute path has to be used
target_dir = "/home/dragonfly/Documents/Uni/WS201"

sc = scraper.Scraper(
  url = url,
  name = course_name,
  target_dir = target_dir
)

# setup your scraper, on your first usage you will be asked for a password
# if the user is set to "" or something not valid, you will be prompted
# an input to enter your username
sc.setup(username)

# this then runs the scraper and downloads all files and folders in the
# target directory
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
  run              Run a previously created scraper
```
**Example usage:**
```bash
# create a new scraper like this, the name will be changed to "bsc_seminar"
# the scraper will be stored in ~/.iliasScraper/
# the target_dir has to be an ABSOLUTE PATH!
$ iliasScraper create --url https://ilias.uni-konstanz.de/ilias/goto_ilias_uni_crs_1078392.html --username tilman.kerl --course-name "bsc seminar" --target_dir /home/dragonfly/Documents/Uni/WS201
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
keyring
click
```
