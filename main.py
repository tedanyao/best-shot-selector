from flask import jsonify
from flask import Flask
from flask import request
from myutils import urldownload
# from myutils import classification
from myutils import return_id
import os
import requests
import json
import urllib.parse
import glob
# import boto

app = Flask(__name__)

port = '8001'
dirname = 'images'
cur_path = os.path.realpath('.')
cluster_path = os.path.join(cur_path, 'clusters')
folder_path = os.path.join(cur_path, dirname)

host_test = 'http://localhost:8002/tests/endpoint'
#host_classifications = 'http://localhost:8002/tests/endpoint'
#host_bestshots = 'http://localhost:8002/tests/endpoint'
host_classifications = 'http://flask-env.eba-m2jsxfrb.us-west-2.elasticbeanstalk.com/pictures/class'
host_bestshots = 'http://flask-env.eba-m2jsxfrb.us-west-2.elasticbeanstalk.com/pictures/is_bestshot'

@app.route('/')
def root_path():
    return jsonify("Hello")

@app.route('/bestshots', methods=['POST'])
def get_bestshots():
    res = download_from_url()
    if not res:
        return jsonify("bestshots error!")

    
    # create a mapping: url => filename
    toURL = {}
    json_obj = request.get_json()
    if not json_obj or not 'file_names' in json_obj:
        return jsonify(False)
    print ('json object: ', json_obj)
    event_id = json_obj['event_id']
    for filename in json_obj['file_names']:
        url_obj = urllib.parse.urlparse(filename)
        toURL[url_obj.path.split('/')[-1]] = filename

    img_paths = glob.glob(folder_path + '/*.jpg')
    print ('img_paths: ', img_paths)
    if len(img_paths) == 0:
        print ("Error: no images downloaded")
        return jsonify("No images downloaded")
    #return "abc"
    
    os.system('python3 imagecluster2/main.py {}'.format(folder_path))

    print ('export PYTHONPATH={}/image-quality-assessment/src;'.format(cur_path))
    os.system('export PYTHONPATH={}/image-quality-assessment/src;'.format(cur_path)
            + ' python3 -m evaluater.predict --base-model-name=MobileNet'
            + ' --weights-file={}/image-quality-assessment/models/MobileNet/weights_mobilenet_technical_0.11.hdf5'.format(cur_path)
            + ' --image-source {}/clusters'.format(cur_path))

    ids = {}
    ids['event_id'] = event_id
    arr = [toURL[item] for item in return_id.find_best(cluster_path)]
    ids['bestshots'] = arr

    # make a request
    token = request.headers.get('Authorization')
    if not token:
        return jsonify("Request does not contain a JWT token!")
    print (token)
    print ('results:', ids)
    send_status = requests.post(host_bestshots, json=ids, headers={'Authorization': 'Bearer ' + token[7:]})
    return ids


@app.route('/classifications', methods=['POST'])
def do_classify():
    res = download_from_url()
    if not res:
        return jsonify("bestshots error!")

    # create a mapping: url => filename
    toURL = {}
    json_obj = request.get_json()
    if not json_obj or not 'file_names' in json_obj:
        return jsonify(False)
    print ('json object: ', json_obj)
    event_id = json_obj['event_id']
    for filename in json_obj['file_names']:
        url_obj = urllib.parse.urlparse(filename)
        toURL[url_obj.path.split('/')[-1]] = filename

    os.system('python3 PyTorch-YOLOv3/main.py {}'.format(folder_path))
    classes = {}
    classes['event_id'] = event_id
    full_path = cur_path + '/result.json'
    data = {}
    with open(full_path) as f:
        data = json.load(f)
    print ('get JSON: ', data)
    class_dict = {}
    for key in data.keys():
        class_dict[toURL[key]] = data[key]
    classes['classes'] = class_dict
#    f = request.get_json()
#    if not f or 'file_names' not in f:
#        return jsonify("invalid json file")
#    print ('json object: ', f)
#    filenames = f['file_names']
#    class_dict = classification.classify(filenames)
#    res = {}
#    res['event_id'] = f['event_id']
#    res['classes'] = class_dict
#
    # make a request
    token = request.headers.get('Authorization')
    if not token:
        return jsonify("Request does not contain a JWT token!")
    print (token)
    send_status = requests.post(host_classifications, json=classes, headers={'Authorization': 'Bearer ' + token[7:]})
    return classes

@app.route('/download', methods=['POST'])
def download_from_url():
    return jsonify(urldownload.download(request.get_json(), folder_path))

@app.route('/test')
def test_post():
    dictToSend = {'question':'what is the answer?'}
    res = requests.post(host_test, json=dictToSend, headers={'Authorization': 'Bearer <your_token>'} )
    dictFromServer = res.json()
    print (dictFromServer)
    return jsonify(dictFromServer)



# ===================================================================================
#  Old Stuff
# ===================================================================================
@app.route('/test_cluster')
def clustering():
    try:
        os.system('python3 imagecluster/main.py {}'.format(folder_path))
        return "finish clustering"
    except:
        return "Error: clustering fail"

@app.route('/test_download_s3', methods=['POST'])
def download_s3():
    if request.method == 'POST':
        f = request.get_json()
        if not f:
            return "invalid json file"
        if 'bucket_name' not in f:
            return "json file does not contain 'bucket_name'"
        bucket_name = f['bucket_name']
        access_key = f['aws_access_key_id']
        secret_key = f['aws_secret_access_key']
        token = f['token']
        # boto.main(bucket_name, access_key, secret_key, token)
        return "finished downloading '" + bucket_name + "'"

@app.route('/test_evaluate')
def evaluate():
    try:
        os.system('python3 -m evaluater.predict --base-model-name=MobileNet --weights-file=/home/$USER/image-quality-assessment/models/MobileNet/weights_mobilenet_technical_0.11.hdf5 --image-source /home/$USER/clusters')
        return "finish evaluating"
    except:
        return "Error: evaluation fail"

@app.route('/test_result')
def result():
    try:
        ids = {}
        ids['bestshots'] = return_id.main()
        return ids
    except:
        return "Error: find ids fail"

    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)
