#sudo apt update
#sudo apt install python3-pip
#pip3 install -r requirements.txt

#mkdir ~/.aws
#cp credentials ~/.aws/credentials
#python3 boto.py

python3 imagecluster/main.py

#export PYTHONPATH=/home/$USER/image-quality-assessment/src

python3 -m evaluater.predict --base-model-name=MobileNet --weights-file=/home/$USER/image-quality-assessment/models/MobileNet/weights_mobilenet_technical_0.11.hdf5 --image-source /home/$USER/clusters

python3 return_id.py
