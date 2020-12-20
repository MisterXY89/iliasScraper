
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
