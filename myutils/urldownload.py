import urllib.request
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
            f, h = urllib.request.urlretrieve(filename, folder_name + '/' + filename.split('/')[-1])
        except:
            print ('[WANRING] URL Error when downloading: ', filename)
    return True


if __name__ == '__main__':
    json_obj = json.loads('{ "file_names": ["https://i.ibb.co/ZGxxX8W/20.jpg","https://i.ibb.co/Vm8zSHj/19.jpg","https://i.ibb.co/wS1fJd1/18.jpg","https://i.ibb.co/dQH8pJ3/17.jpg","https://i.ibb.co/Xy8JCW2/16.jpg","https://i.ibb.co/7JfMddj/15.jpg","https://i.ibb.co/g4LFLxp/14.jpg","https://i.ibb.co/Kxh0Mhg/13.jpg","https://i.ibb.co/2ktWrkw/12.jpg","https://i.ibb.co/vmVk41M/11.jpg","https://i.ibb.co/CvDscZj/10.jpg","https://i.ibb.co/R07CpTL/9.jpg","https://i.ibb.co/5LwHNS5/8.jpg","https://i.ibb.co/mqmGS0K/7.jpg","https://i.ibb.co/vwd0VLt/6.jpg","https://i.ibb.co/t25T3vg/5.jpg","https://i.ibb.co/TWt0Y4n/4.jpg","https://i.ibb.co/NymXFJT/3.jpg","https://i.ibb.co/mckt67T/2.jpg","https://i.ibb.co/X7Y0mFp/1.jp"], "event_id": "123" }')
    download(json_obj, 'images')
