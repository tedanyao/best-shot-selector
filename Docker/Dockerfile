# Start with a Linux micro-container to keep the image tiny
#FROM ubuntu:18.04
FROM python:3.7

# Install just the Python runtime (no dev)
RUN apt-get update && apt-get install -y python3-dev python3-pip git

# Set up a working folder and install the pre-reqs
RUN git clone https://github.com/tedanyao/best-shot-selector.git
WORKDIR /best-shot-selector
RUN pip3 install -r requirements.txt 
RUN curl -o ./PyTorch-YOLOv3/weights/yolov3.weights  https://pjreddie.com/media/files/yolov3.weights

# Expose ports
EXPOSE 8001

# Run the service
CMD [ "python3", "main.py" ]
