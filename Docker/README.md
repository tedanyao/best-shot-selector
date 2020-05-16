# Run inside a container
1. ```docker build -t <tag> .```  
2. ```docker run -p 8001:8001 -d <tag>```  

# AWS beanstalk guide
If you want to deploy the application on AWS Beanstalk, please:  
1. Zip the "Dockerfile" and "Dockerrun.aws.json", as "app.zip."  
2. Upload "app.zip" as an application to AWS beanstalk.  
