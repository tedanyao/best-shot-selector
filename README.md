# Best Shot Selector
This is a flask WebAPI service.


# APIs
### Download buckets from S3
Request type: POST  
Request url: http://localhost:8001/download  
Sample reqeust body:  
```
{
    "bucket_name": "yylbucket",
    "aws_access_key_id": "ASIAROPSWYQXJ6Z35E7T",
    "aws_secret_access_key": "wzHMdvUV54Bx9jyzZgPZ2H1sQFugo9v6HdZL0GIt",
    "token": "xxxxx"
}
```

### Get the best shots in a bucket
Request type: POST  
Request url: http://localhost:8001/bestshots  
Format: application/json  
Sample request:  
```
{
  "location": "<s3_url>"
  "folder_name": "<folder_name>"
}
```
Sample response:  
```
{
  "bestshot": ["aaa.jpg", "bbb.jpg"]
}
```


### Testing using curl
```
curl localhost:8001/download -H 'Content-Type: application/json' -d '<JSON>'
```
