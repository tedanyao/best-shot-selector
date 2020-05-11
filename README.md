# Best Shot Selector
This is a flask WebAPI service.


# APIs
### 1. Get the classes of the images
Request type: POST  
Request url: http://awsmachine.com:8001/classification  
Sample reqeust body:  
```
{
    "file_names": ['a.jpg', 'b.jpg']
}
```
Response:
```
{
    "classes": [
        "url1": "people",
        "url2": "landscape",
        ...
    ]
}
```

### 2. Get the best shots in a bucket
Request type: POST  
Request url: http://awsmachine.com:8001/bestshots  
Format: application/json  
Sample request:  

Sample response:  
```
{
    "file_names": ["url1", "url2", "url3"]
}
```
```
{
  "bestshot": ["aaa.jpg", "bbb.jpg"]
}
```
Description:
It performs 4 steps.  
1. Download files from S3.  
2. Do clustering.  
3. Evaluate scores of each image.  
4. Select the best shots and return their ids as a JSON.  

# Testing using curl
```
curl localhost:8001/bestshots -H 'Content-Type: application/json' -d '<JSON>'
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
