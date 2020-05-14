import urllib.request
import urllib.parse
import json
import os
import shutil
def download(json_obj, folder_name):
    if not json_obj or not 'file_names' in json_obj:
        return False

    if os.path.isdir(folder_name):
        shutil.rmtree(folder_name)
    os.mkdir(folder_name)
    for filename in json_obj['file_names']:
        try:
            url_obj = urllib.parse.urlparse(filename)
            print ('[MSG] Downloading file: ', url_obj.path.split('/')[-1])
            f, h = urllib.request.urlretrieve(filename, folder_name + '/' + url_obj.path.split('/')[-1])
        except:
            print ('[WANRING] URL Error when downloading: ', filename)
    return True


if __name__ == '__main__':
    json_obj = json.loads('{"event_id":"456", "file_names": ["https://cdn.eso.org/images/screen/eso1907a.jpg"]}')
    json_obj = json.loads('{"event_id": "18", "file_names": ["https://firebasestorage.googleapis.com/v0/b/justshare-10b29.appspot.com/o/photos%2F122447dc-b9a1-4faa-aa39-4df40306974d.jpg?alt=media&token=01941832-5dcb-48a4-b63f-5ca2146445e0"]}')
    download(json_obj, 'images')
