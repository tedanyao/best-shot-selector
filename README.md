# Best Shot Selector
This is a flask WebAPI service.


# APIs
### Download buckets from S3
Request type: POST  
Request url: http://awsmachine.com:8001/classification  
Sample reqeust body:  
```
{
    "file_names": ['a.jpg', 'b.jpg'],
    //"aws_access_key_id": "ASIAROPSWYQXJ6Z35E7T",
    //"aws_secret_access_key": "wzHMdvUV54Bx9jyzZgPZ2H1sQFugo9v6HdZL0GIt",
    //"token": "xxxxx"
}
```

### Get the best shots in a bucket
Request type: POST  
Request url: http://awsmachine.com:8001/bestshots  
Format: application/json  
Sample request:  

Sample response:  
```
{
    "bucket_name": "yylbucket",
    "folder_name": "xxxx",
    //"aws_access_key_id": "ASIAROPSWYQXJ6Z35E7T",
    //"aws_secret_access_key": "wzHMdvUV54Bx9jyzZgPZ2H1sQFugo9v6HdZL0GIt",
    //"token": "xxxxx"
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

### Testing using curl
```
curl localhost:8001/download -H 'Content-Type: application/json' -d '<JSON>'
```
