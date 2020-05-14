sudo apt -y update
sudo apt -y install python3-pip
sudo apt -y install libopencv-dev

pip3 install -r requirements.txt --no-cache-dir

#mkdir ~/.aws
#cp credentials ~/.aws/credentials
#python3 boto.py
#export PYTHONPATH=/home/$USER/image-quality-assessment/src
curl -o ./PyTorch-YOLOv3/weights/yolov3.weights  https://pjreddie.com/media/files/yolov3.weights

python3 main.py
