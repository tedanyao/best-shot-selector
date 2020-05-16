# Best Shot Selector
This is a flask WebAPI service with the following functions:  
1. Get the class result of the input url images  
It detects the category of each images.  
input_images = [a1, b1, c1]  
classes = ['people', 'landscape', 'people']  

2. Get the best shots of the input url images  
If there are similar images, it selects the best shot of those similar images.  
For example,  
input_images = [a1, a2, a3, b1, c1, d1, d2]  
best_shots = [a3, b1, c1, d2] (a3 is the best among a*, d2 is the best among d*)  

* All messages are transmitted by HTTP in JSON format  

# Installation
### Environment
* Ubuntu
1. Download the repository
2. ```source setup.sh```
3. RUN: ```python3 main.py```
* CentOS
1. Download the repository
2. ```source setup_centOS.sh```
3. RUN: ```python3 main.py```

### Using a docker container
Please see the folder "Docker" for further instructions.

# APIs
### 1. Get the classes of the images
Request type: POST  
Request url: http://hostmachine:8001/classifications  
Sample reqeust body:  
```
# Note that the header should contain a JWT token
{
    "event_id": "123",
    "file_names": ["url1", "url2"]
}
```
Response:
```
{
    "event_id": "123",
    "classes": {
        "url1": "people",
        "url2": "landscape",
        ...
    }
}
```

### 2. Get the best shots in a bucket
Request type: POST  
Request url: http://hostmachine:8001/bestshots  
Format: application/json  
Sample request:  
```
# Note that the header should contain a JWT token
{
    "event_id": "123",
    "file_names": ["url1", "url2", "url3"]
}
```
Sample response:  
```
{
    "event_id": "123"
    "bestshots": ["url1", "url2"]
}
```
Description:
It performs 4 steps.  
1. Download files from S3.  
2. Do clustering.  
3. Evaluate scores of each image.  
4. Select the best shots and return their ids as a JSON.  

# Testing using curl
```console
# bestshots
curl localhost:8001/bestshots -H 'Content-Type: application/json' -H "Authorization: Bearer XAASERHRSTJ" -d '{"event_id":"123", "file_names": ["https://cdn.eso.org/images/screen/eso1907a.jpg"]}'

# classification
curl localhost:8001/classifications -H 'Content-Type: application/json' -H "Authorization: Bearer AEGERHSZXXT" -d '{"event_id":"456", "file_names": ["https://cdn.eso.org/images/screen/eso1907a.jpg"]}'

# downlaod
curl localhost:8001/download -H 'Content-Type: application/json' -d '{"file_names": ["https://cdn.eso.org/images/screen/eso1907a.jpg"]}'

# send request to another server
curl localhost:8001/test -H 'Content-Type: application/json'

# another test
curl http://ec2-54-221-41-82.compute-1.amazonaws.com:8001/classifications -H 'Content-Type: application/json' -H "Authorization: Bearer AEGERHSZXXT" -d '{ "file_names": ["https://i.ibb.co/ZGxxX8W/20.jpg","https://i.ibb.co/Vm8zSHj/19.jpg","https://i.ibb.co/wS1fJd1/18.jpg","https://i.ibb.co/dQH8pJ3/17.jpg","https://i.ibb.co/Xy8JCW2/16.jpg","https://i.ibb.co/7JfMddj/15.jpg","https://i.ibb.co/g4LFLxp/14.jpg","https://i.ibb.co/Kxh0Mhg/13.jpg","https://i.ibb.co/2ktWrkw/12.jpg","https://i.ibb.co/vmVk41M/11.jpg","https://i.ibb.co/CvDscZj/10.jpg","https://i.ibb.co/R07CpTL/9.jpg","https://i.ibb.co/5LwHNS5/8.jpg","https://i.ibb.co/mqmGS0K/7.jpg","https://i.ibb.co/vwd0VLt/6.jpg","https://i.ibb.co/t25T3vg/5.jpg","https://i.ibb.co/TWt0Y4n/4.jpg","https://i.ibb.co/NymXFJT/3.jpg","https://i.ibb.co/mckt67T/2.jpg","https://i.ibb.co/X7Y0mFp/1.jpg"], "event_id": "123" }'

```
