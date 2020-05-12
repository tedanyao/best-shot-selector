# Best Shot Selector
This is a flask WebAPI service.

# Installation
1. Download the repository
2. ```source setup.sh```

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
```

# Old Stuff
### Download buckets from S3 (Not Used)
Request type: POST  
Request url: http://hostmachine:8001/classification  
Sample reqeust body:  
```
{
    "file_names": ['a.jpg', 'b.jpg'],
    "aws_access_key_id": "ASIAROPSWYQXJ6Z35E7T",
    "aws_secret_access_key": "wzHMdvUV54Bx9jyzZgPZ2H1sQFugo9v6HdZL0GIt",
    "token": "xxxxx"
}
```
