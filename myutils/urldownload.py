import urllib.request
import os
import shutil
def download(json_obj, folder_name):
    if not json_obj or not 'file_names' in json_obj:
        return False

    if os.path.isdir(folder_name):
        shutil.rmtree(folder_name)
    os.mkdir(folder_name)
    for filename in json_obj['file_names']:
        urllib.request.urlretrieve(filename, folder_name + '/' + filename.split('/')[-1])
    return True
