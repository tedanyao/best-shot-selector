# Start with a Linux micro-container to keep the image tiny
#FROM ubuntu:18.04
FROM python:3.7
# Document who is responsible for this image
# MAINTAINER Seetharami R. Seelam "sseelam@nyu.edu"

# Install just the Python runtime (no dev)
RUN apt-get update && apt-get install -y python3-dev python3-pip git
#RUN apk add --no-cache python3-dev py3-pip git
# Expose any ports the app is expecting in the environment
# ENV PORT 8001
# EXPOSE $PORT
#RUN pip3 install torch --no-cache-dir
#RUN pip3 install torchvision --no-cache-dir

# Set up a working folder and install the pre-reqs
# RUN mkdir app
#ADD pytorch-cli/requirements.txt /app
RUN git clone https://github.com/tedanyao/best-shot-selector.git
WORKDIR /best-shot-selector
#ADD ./best-shot-selector /app
#RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt 
RUN curl -o ./PyTorch-YOLOv3/weights/yolov3.weights  https://pjreddie.com/media/files/yolov3.weights

EXPOSE 8001
# Add the code as the last Docker layer because it changes the most
#ADD main.py  /app/main.py
# RUN mkdir data
#ADD data/MNIST /data/
# -v data:/data
# Run the service
CMD [ "python3", "main.py" ]
