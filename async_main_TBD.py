# from flask import jsonify
# from flask import Flask
# import boto
from myutils import urldownload
from myutils import classification
from myutils import return_id
# from flask import request
import os
import requests
import json
from quart import Quart
from quart import jsonify
from quart import request
#app = Flask(__name__)
app = Quart(__name__)

img_folder_name = 'images'

host_test = 'http://localhost:8002/tests/endpoint'
host_classifications = 'http://localhost:8002/tests/endpoint'
host_bestshots = 'http://localhost:8002/tests/endpoint'
#host_classifications = 'http://localhost:5000/pictures/class'
#host_bestshots = 'http://localhost:5000/pictures/is_bestshot'

@app.route('/')
def root_path():
    return jsonify("Hello")

@app.route('/bestshots', methods=['POST'])
async def get_bestshots():
    res = download_from_url()
    if not res:
        return jsonify("bestshots error!")

    
    # create a mapping: url => filename
    toURL = {}
    json_obj = await request.get_json()
    if not json_obj or not 'file_names' in json_obj:
        return jsonify(False)
    event_id = json_obj['event_id']
    for filename in json_obj['file_names']:
        toURL[filename.split('/')[-1]] = filename

    os.system('python3 imagecluster/main.py {}'.format(img_folder_name))
    os.system('export PYTHONPATH=/home/$USER/image-quality-assessment/src')
    os.system('python3 -m evaluater.predict --base-model-name=MobileNet' 
            + ' --weights-file=/home/$USER/image-quality-assessment/models/MobileNet/weights_mobilenet_technical_0.11.hdf5'
            + ' --image-source /home/$USER/clusters')

    ids = {}
    ids['event_id'] = event_id
    arr = [toURL[item] for item in return_id.main()]
    ids['bestshots'] = arr

    # make a request
    token = request.headers.get('Authorization')
    if not token:
        return jsonify("Request does not contain a JWT token!")
    send_status = requests.post(host_bestshots, json=ids, headers={'Authorization': token})
    return ids


@app.route('/classifications', methods=['POST'])
def do_classify():
    f = request.get_json()
    if not f or 'file_names' not in f:
        return jsonify("invalid json file")
    filenames = f['file_names']
    class_dict = classification.classify(filenames)
    res = {}
    res['event_id'] = f['event_id']
    res['classes'] = class_dict

    # make a request
    token = request.headers.get('Authorization')
    if not token:
        return jsonify("Request does not contain a JWT token!")
    send_status = requests.post(host_classifications, json=res, headers={'Authorization': token})
    return res

@app.route('/download', methods=['POST'])
async def download_from_url():
    return jsonify(urldownload.download(await request.get_json(), img_folder_name))

@app.route('/test')
def test_post():
    dictToSend = {'question':'what is the answer?'}
    res = requests.post(host_test, json=dictToSend, headers={'Authorization': 'Bearer <your_token>'} )
    dictFromServer = res.json()
    print (dictFromServer)
    return jsonify(dictFromServer)



# ===================================================================================
#  Old stuff
# ===================================================================================
@app.route('/cluster')
def clustering():
    try:
        os.system('python3 imagecluster/main.py {}'.format(img_folder_name))
        return "finish clustering"
    except:
        return "Error: clustering fail"

@app.route('/bestshots_old', methods=['GET'])
def bestshots_old():
    os.system('python3 imagecluster/main.py {}'.format(img_folder_name))
    os.system('python3 -m evaluater.predict --base-model-name=MobileNet --weights-file=/home/$USER/image-quality-assessment/models/MobileNet/weights_mobilenet_technical_0.11.hdf5 --image-source /home/$USER/clusters')
    ids = {}
    ids['bestshots'] = return_id.main()
    return ids

@app.route('/download_s3', methods=['POST'])
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
        #os.system("python3 boto.py " + bucket_name + " " + access_key + " " + secret_key)
        return "finished downloading '" + bucket_name + "'"

@app.route('/evaluate')
def evaluate():
    try:
        os.system('python3 -m evaluater.predict --base-model-name=MobileNet --weights-file=/home/$USER/image-quality-assessment/models/MobileNet/weights_mobilenet_technical_0.11.hdf5 --image-source /home/$USER/clusters')
        return "finish evaluating"
    except:
        return "Error: evaluation fail"

@app.route('/result')
def result():
    try:
        ids = {}
        ids['bestshots'] = return_id.main()
        return ids
    except:
        return "Error: find ids fail"

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port='8001')

