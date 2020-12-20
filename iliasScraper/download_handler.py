
import os
import fleep

class DownloadHandler:
    """
    docstring for RequestHandler.
    """

    def __init__(self, request_handler):
        self.request_handler = request_handler

    def download(self, file_dict, path):
        path = os.getcwd() + "/" + path
        if len(path) == 0:
            path = "test"
        self._verify_path(path)
        url = file_dict["url"]
        file_name = file_dict["file_name"]
        file = self.request_handler.get_file(url)
        file_loc = path+"/"+file_name
        open(file_loc, "wb").write(file.content)

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

        os.rename(r""+file_loc,r""+file_loc+"."+extension)

    def _verify_path(self, path):
        folder_list = path.split("/")
        for i in range(0, len(folder_list)):
            sub_path = "/"+"/".join(folder_list[1:i+3])
            if not os.path.exists(sub_path):
                # todo check windows
                original_umask = os.umask(000)
                os.makedirs(sub_path, mode=0o777), #mode = 0o666)
                os.umask(original_umask)
        return 1
