# mobile-ssd-auto-trainer

### Setup:
Just make sure your $CAFFE_PATH environment variable points to your caffe installation, e.g.:

`export CAFFE_PATH=~/caffe/`

Edit train_ssd.py to include:

`dataset_root = Path to your VOC annotated dataset.`

`labels = Array with the labels of the classes you want to train.`

Pre-trained weights are automatically downloaded from https://github.com/chuanqi305/MobileNet-SSD.

To start training just run:

`python train_ssd.py`

The generated weights were validated using a Raspberry Pi and an Intel NCS2, using code from this awesome repository: https://github.com/PINTO0309/MobileNet-SSD-RealSense.

Bash scripts were retrieved from https://github.com/weiliu89/caffe and https://github.com/chuanqi305/MobileNet-SSD.

More customization coming soon...
