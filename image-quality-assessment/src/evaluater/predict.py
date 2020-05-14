
import os
import glob
import json
import argparse
from utils.utils import calc_mean_score, save_json
from handlers.model_builder import Nima
from handlers.data_generator import TestDataGenerator


def image_file_to_json(img_path):
    img_dir = os.path.dirname(img_path)
    img_id = os.path.basename(img_path).split('.')[0]

    return img_dir, [{'image_id': img_id}]

# YY
# def image_dir_to_json_tree(img_dir, img_type='jpg'):
#     print ('img_dir: ', img_dir)
#     img_paths = []
#     for dirpath, dirnames, filenames in os.walk(img_dir):
#         for f in filenames:
#             img_paths.append(dirpath + '/' + f)
#     print ('all files:', img_paths)
#     samples = []
#     for img_path in img_paths:
#         img_id = os.path.basename(img_path).split('.')[0]
#         samples.append({'image_id': img_id})
# 
#     return samples


def image_dir_to_json(img_dir, img_type='jpg'):
    img_paths = glob.glob(os.path.join(img_dir, '*.'+img_type))
    print ('img_paths:', img_paths)
    samples = []
    for img_path in img_paths:
        img_id = os.path.basename(img_path).split('.')[0]
        samples.append({'image_id': img_id})

    return samples


def predict(model, data_generator):
    return model.predict_generator(data_generator, workers=8, use_multiprocessing=False, verbose=1)


def main(base_model_name, weights_file, image_source, predictions_file, img_format='jpg'):
    # load samples
    if os.path.isfile(image_source):
        image_dir, samples = image_file_to_json(image_source)
    else:
        image_dir = image_source
        print ('image_dir:', image_dir)
        samples = image_dir_to_json(image_dir, img_type='jpg') # YY
        print ('samples:', samples) # YY
        if len(samples) == 1:
            samples[0]['mean_score_prediction'] = 5.0
            print(json.dumps(samples, indent=2))
            if predictions_file is not None:
                save_json(samples, image_dir + '/' + 'evaluate.json') # YY
            return


    # build model and load weights
    nima = Nima(base_model_name, weights=None)
    nima.build()
    nima.nima_model.load_weights(weights_file)

    # initialize data generator
    data_generator = TestDataGenerator(samples, image_dir, 64, 10, nima.preprocessing_function(),
                                       img_format=img_format)

    # get predictions
    predictions = predict(nima.nima_model, data_generator)

    # calc mean scores and add to samples
    for i, sample in enumerate(samples):
        sample['mean_score_prediction'] = calc_mean_score(predictions[i])

    print(json.dumps(samples, indent=2))

    if predictions_file is not None:
        save_json(samples, image_dir + '/' + 'evaluate.json') # YY


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base-model-name', help='CNN base model name', required=True)
    parser.add_argument('-w', '--weights-file', help='path of weights file', required=True)
    parser.add_argument('-is', '--image-source', help='image directory or file', required=True)
    parser.add_argument('-pf', '--predictions-file', help='file with predictions', required=False, default=None)

    args = parser.parse_args()

    # YY
    # main(**args.__dict__)
    for dirpath, dirnames, filenames in os.walk(args.image_source):
        if filenames:
            main(args.base_model_name, args.weights_file, dirpath, dirpath)
