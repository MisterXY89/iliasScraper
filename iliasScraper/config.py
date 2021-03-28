
import platform

SCRAPER_NAME = "ilias-scraper"
LOGIN_POST_URL = "https://ilias.uni-konstanz.de/ilias/ilias.php?lang=de&client_id=ilias_uni&cmd=post&cmdClass=ilstartupgui&cmdNode=y1&baseClass=ilStartUpGUI&rtoken="


if platform.system() == "windows":
    PATH_DELIMITER = "\\"
else:
    PATH_DELIMITER = "/"
