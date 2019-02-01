# mobile-ssd-auto-trainer
Automates most of the training procedure for MobileNet SSD.

### Setup:
Just make sure your $CAFFE_PATH environment variable points to your caffe installation, e.g.:

`export CAFFE_PATH=~/caffe/`

Edit train_ssd.py to include:

`dataset_root = Path to your VOC annotated dataset.`

`labels = Array with the labels of the classes you want to train.`

Pre-trained weights are automatically downloaded from https://github.com/chuanqi305/MobileNet-SSD.

To start training just run:

`python train_ssd.py`


More customization coming soon...
