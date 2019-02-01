#!/bin/bash
cur_dir=$(cd $( dirname ${BASH_SOURCE[0]} ) && cd .. && pwd )
weights_file="$cur_dir/templates/mobilenet_iter_73000.caffemodel"

if [ ! -f $weights_file ]; then
    wget -O $weights_file "https://drive.google.com/uc?export=download&id=0B3gersZ2cHIxVFI1Rjd5aDgwOG8"
fi

$CAFFE_PATH/build/tools/caffe train -solver="$cur_dir/datasets/$1/solver_train.prototxt" \
-weights=$weights_file \
-gpu 0
