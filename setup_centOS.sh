sudo yum install -y git
sudo yum install -y update
sudo yum install -y python3-pip
sudo pip3 install —upgrade pip

pip install -r requirements.txt 

curl -o ./PyTorch-YOLOv3/weights/yolov3.weights  https://pjreddie.com/media/files/yolov3.weights

# python3 main.py
