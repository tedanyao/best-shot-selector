import os
import json
USER = os.environ.get('USER')
IMAGE_SOURCE = '/home/' + USER + '/clusters'

key_filename = 'evaluate.json'

def getMaxScoreId(jsondata):
    maxVal = -float('inf')
    maxId = -1
    for i in range(len(jsondata)):
        if jsondata[i]['mean_score_prediction'] > maxVal:
            maxVal = jsondata[i]['mean_score_prediction']
            maxId = jsondata[i]['image_id']
    return maxId

#print ('Max score ids under path \'' + IMAGE_SOURCE + '\':')
#for dirpath, dirnames, filenames in os.walk(IMAGE_SOURCE):
#    if filenames:
#        if key_filename in filenames:
#            full_path = dirpath + '/' + key_filename
#            with open(full_path) as f:
#                data = json.load(f)
#                max_id = getMaxScoreId(data)
#                print (max_id + '.jpg')
#        else:
#            raise("Error: Folders that has images is missing " + key_filename)

def find_best(folder_path):
    outputs = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        if filenames:
            full_path = dirpath + '/' + key_filename
            try:
                with open(full_path) as f:
                    data = json.load(f)
                    max_id = getMaxScoreId(data)
                    filename = max_id + '.jpg'
                    print (filename)
                    outputs.append(filename)
            except:
                print("ERROR: Folder '" + dirpath + "' has images but " + key_filename + " is missing.")
    return outputs

if __name__ == '__main__':
    main()
