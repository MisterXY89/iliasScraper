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
