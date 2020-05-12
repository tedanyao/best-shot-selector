import boto3
import os

def main(bucket_name, access_key, secret_key, token):
    print ('boto3.main()', access_key, secret_key)
    USER = os.environ.get('USER')
    
    s3 = boto3.resource('s3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=token)
    #    s3 = boto3.resource('s3')

    bucket = s3.Bucket(bucket_name)
    client  = boto3.client('s3')
    
    response = client.list_objects_v2(Bucket=bucket_name)
    for filename in response['Contents']:
        print (filename['Key'])
        if filename['Key'][-1] == '/':
            continue
        
        # create dirs
        dir_path = '/'.join(filename['Key'].split('/')[:-1])
        print ('dir_path:', dir_path)
        if dir_path and not os.path.isdir(dir_path):
            os.makedirs(dir_path)
    
        # download file
        bucket.download_file(filename['Key'], "/home/" + USER + '/' + filename['Key'])
            
    #print (bucket)
    #for obj in bucket.objects.all():
    #    print (obj.key)
    #    if obj.key[-3:] == 'jpg':
    #        bucket.download_file(obj.key, '/home/vagrant/' + obj.key)



if __name__ == '__main__':
        main('yylbucket', 'ASIAROPSWYQXDBACLMPY', 'E5j0ROObpPvdXxdiZp/QqubbuniVgQcVVCe11ZEc', 'FwoGZXIvYXdzEKL//////////wEaDJl1iH3Qz3iPO1N6ziK9ATdL5/SXj5PXxRoeDQPmIMgmGFcYSK4mmjNYHt1KmUGX/an1c/z7+Sr/DUSvHi9CY2vGWXWFk2YZvu/Hape8XVuPZWyrmNbhGpuYlT/o3fHyAwPr+dPyXLVvkzyz3jFumFBXpMQH2Qpgw/E9oUqO+wGrXNNuQjQ7nJ2qifzRZbj8P/OT/TqLC8XbVGirHO2ONTWM2uVwrfdNYRl5Qaf389NU55jW417r2MeI2vpxUDKR53Uop3JhM6MD6AanRSiW3NL1BTItHpZ5YpazOLM1ocMvDI5Je0c1OaFNc/PDYnPFwhhH5eUU9bHNuYqMfxlvwUth')
