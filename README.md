# Best Shot Selector
This is a flask WebAPI service.


# APIs
### 1. Get the classes of the images
Request type: POST  
Request url: http://awsmachine.com:8001/classifications  
Sample reqeust body:  

```
refresh_token
{
    "event_id": "xxx",
    "file_names": ["url1", "url2"]
}
```
Response:
```
{
    "event_id": "xxx",
    "classes": {
        "url1": "people",
        "url2": "landscape",
        ...
    }
}
```

### 2. Get the best shots in a bucket
Request type: POST  
Request url: http://awsmachine.com:8001/bestshots  
Format: application/json  
Sample request:  
```
{
    "event_id": "xxx",
    "file_names": ["url1", "url2", "url3"]
}
```
Sample response:  
```
{
    "event_id": "xxx"
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
# test bestshots
curl localhost:8001/bestshots -H 'Content-Type: application/json' -d '{"file_names": ["https://cdn.eso.org/images/screen/eso1907a.jpg"]}'

# test classification
curl localhost:8001/classifications -H 'Content-Type: application/json' -d '{"file_names": ["https://cdn.eso.org/images/screen/eso1907a.jpg"]}'

# test downlaod
curl localhost:8001/download -H 'Content-Type: application/json' -d '{"file_names": ["https://cdn.eso.org/images/screen/eso1907a.jpg"]}'

# test sending request to another server
curl localhost:8001/test -H 'Content-Type: application/json'
```

# Old Stuff
### Download buckets from S3 (Not Used)
Request type: POST  
Request url: http://awsmachine.com:8001/classification  
Sample reqeust body:  
```
{
    "file_names": ['a.jpg', 'b.jpg'],
    "aws_access_key_id": "ASIAROPSWYQXJ6Z35E7T",
    "aws_secret_access_key": "wzHMdvUV54Bx9jyzZgPZ2H1sQFugo9v6HdZL0GIt",
    "token": "xxxxx"
}
```
