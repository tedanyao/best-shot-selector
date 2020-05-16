import os
import json
#USER = os.environ.get('USER')
#IMAGE_SOURCE = '/home/' + USER + '/clusters'

key_filename = 'evaluate.json'

def getMaxScoreId(jsondata):
    maxVal = -float('inf')
    maxId = -1
    for i in range(len(jsondata)):
        if jsondata[i]['mean_score_prediction'] > maxVal:
            maxVal = jsondata[i]['mean_score_prediction']
            maxId = jsondata[i]['image_id']
    return maxId

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
