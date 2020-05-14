from __future__ import division
#import magic
import urllib.request
#from app import app
#from flask import Flask, flash, request, redirect, render_template
#from werkzeug.utils import secure_filename

import numpy as np
#from IPython.display import display
from PIL import Image

from models import *
from utils import *
import os, sys, time, datetime, random
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torch.autograd import Variable

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import NullLocator
import json

from PIL import Image
from models import *
from utils.utils import *
from utils.datasets import *
import shutil

#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS = set(['jpg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#@app.route('/<filename>', methods = ['GET'])
#def show_result(filename):
#    filename = 'res_' + filename.replace(".jpg", ".png")
#    app.logger.info('showing: %s', filename)
#    return render_template('result.html', user_image=filename)

def go_to_inference(folder_name):
    image_folder = folder_name
    model_def = "PyTorch-YOLOv3/config/yolov3.cfg"
    #weights_path = "PyTorch-YOLOv3/weights/yolov3-tiny.weights"
    weights_path = "PyTorch-YOLOv3/weights/yolov3.weights"
    class_path = "PyTorch-YOLOv3/data/coco.names"
    conf_thres = 0.8
    nms_thres = 0.4
    batch_size = 1
    n_cpu = 0
    img_size = 416
    #checkpoint_model = "yolov3_ckpt_500.pth"

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    os.makedirs("output", exist_ok=True)

    # Set up model
    model = Darknet(model_def, img_size=img_size).to(device)

    if weights_path.endswith(".weights"):
        # Load darknet weights
        print ('here')
        model.load_darknet_weights(weights_path)
    else:
        # Load checkpoint weights
        print ('there')
        model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))

    model.eval()  # Set in evaluation mode

    dataloader = DataLoader(
        ImageFolder(image_folder, img_size=img_size),
        batch_size=batch_size,
        shuffle=False,
        num_workers=n_cpu,
    )

    classes = load_classes(class_path)  # Extracts class labels from file

    Tensor = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor

    imgs = []  # Stores image paths
    img_detections = []  # Stores detections for each image index

    print("\nPerforming object detection:")
    prev_time = time.time()
    for batch_i, (img_paths, input_imgs) in enumerate(dataloader):
        # Configure input
        input_imgs = Variable(input_imgs.type(Tensor))

        # Get detections
        with torch.no_grad():
            detections = model(input_imgs)
            detections = non_max_suppression(detections, conf_thres, nms_thres)

        # Log progress
        current_time = time.time()
        inference_time = datetime.timedelta(seconds=current_time - prev_time)
        prev_time = current_time
        print("\t+ Batch %d, Inference Time: %s" % (batch_i, inference_time))

        # Save image and detections
        imgs.extend(img_paths)
        img_detections.extend(detections)

    # Bounding-box colors
    #cmap = plt.get_cmap("tab20b")
    #colors = [cmap(i) for i in np.linspace(0, 1, 20)]

    #print("\nSaving images:")
    # Iterate through images and save plot of detections
    class_dict = {}
    for img_i, (path, detections) in enumerate(zip(imgs, img_detections)):
        mypath = path.split('/')[-1]
        print("(%d) Image: '%s'" % (img_i, path))

        # Create plot
        img = np.array(Image.open(path))
        #plt.figure()
        #fig, ax = plt.subplots(1, figsize=(12, 9))
        #ax.imshow(img)
        print ('=============',path)
        class_dict[mypath] = 'landscape'

        # Draw bounding boxes and labels of detections
        if detections is not None:
            # Rescale boxes to original image
            detections = rescale_boxes(detections, img_size, img.shape[:2])
            unique_labels = detections[:, -1].cpu().unique()
            n_cls_preds = len(unique_labels)
            #bbox_colors = random.sample(colors, n_cls_preds)
            for x1, y1, x2, y2, conf, cls_conf, cls_pred in detections:

                #print("\t+ Label: %s, Conf: %.5f" % (classes[int(cls_pred)], cls_conf.item()))
                c = classes[int(cls_pred)]
                print ('class: ', c)
                if c == 'person':
                    class_dict[mypath] = 'people'

                #box_w = x2 - x1
                #box_h = y2 - y1

                #color = bbox_colors[int(np.where(unique_labels == int(cls_pred))[0])]
                ## Create a Rectangle patch
                #bbox = patches.Rectangle((x1, y1), box_w, box_h, linewidth=2, edgecolor=color, facecolor="none")
                ## Add the bbox to the plot
                #ax.add_patch(bbox)
                ## Add label
                #plt.text(
                #    x1,
                #    y1,
                #    s=classes[int(cls_pred)],
                #    color="white",
                #    verticalalignment="top",
                #    bbox={"color": color, "pad": 0},
                #)

        # Save generated image with detections
        #plt.axis("off")
        #plt.gca().xaxis.set_major_locator(NullLocator())
        #plt.gca().yaxis.set_major_locator(NullLocator())
        #filename = path.split("/")[-1].split(".")[0]
        #app.logger.info("saving static/res_" + filename +".png")
        #plt.savefig(f"static/res_{filename}.png", bbox_inches="tight", pad_inches=0.0)
        #plt.close()
        #return "image saved"
    print (class_dict)
    with open('result.json', 'w') as outfile:
        json.dump(class_dict, outfile)

if __name__ == "__main__":
    folder_path = 'images'
    go_to_inference(folder_path)

