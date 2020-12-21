
import os
import fleep
import platform

class DownloadHandler:
    """
    docstring for RequestHandler.
    """

    def __init__(self, request_handler, target_dir):
        self.request_handler = request_handler
        self.target_dir = target_dir
        if platform.system() == "windows":
            self.PATH_DELIMITER = "\\"
        else:
            self.PATH_DELIMITER = "/"


    def _determine_extension(self, file_loc):
        with open(file_loc, "rb") as file:
            info = fleep.get(file.read(256))
        if not info.extension:
            # default extension
            extension = "txt"
        else:
            extension = info.extension[0]
        if extension == "ai":
            extension = "pdf"
        elif extension == "pages":
            extension = "zip"
        return extension

    def download(self, file_dict, file_path, ignore_endings):
        path = ""
        if not self.target_dir[:-1] == self.PATH_DELIMITER:
            self.target_dir += self.PATH_DELIMITER

        # relative path in script execution dir
        if self.target_dir == self.PATH_DELIMITER:
            path += os.getcwd()

        # else: an absolute path has been set and will be used
        path += self.target_dir + file_path

        # create path if does not exist
        self._verify_path(path)
        url = file_dict["url"]
        file_name = file_dict["file_name"]
        file = self.request_handler.get_file(url)
        file_loc = path+self.PATH_DELIMITER+file_name
        # save file without file-ending
        open(file_loc, "wb").write(file.content)
        # set file-ending
        extension = self._determine_extension(file_loc)
        # if extension in ignore_endings:
        #     # delete file
        os.rename(r""+file_loc,r""+file_loc+"."+extension)

    def _verify_path(self, path):
        folder_list = path.split(self.PATH_DELIMITER)
        for i in range(0, len(folder_list)):
            sub_path = self.PATH_DELIMITER+self.PATH_DELIMITER.join(folder_list[1:i+3])
            if not os.path.exists(sub_path):
                # todo check windows
                original_umask = os.umask(000)
                os.makedirs(sub_path, mode=0o777), #mode = 0o666)
                os.umask(original_umask)
        return 1
