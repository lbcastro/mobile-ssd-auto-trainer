#!/bin/bash
cur_dir=$(cd $( dirname ${BASH_SOURCE[0]} ) && cd .. && pwd )
session_dir=$1

weights_file="$cur_dir/templates/mobilenet_iter_73000.caffemodel"

if [ ! -f $weights_file ]; then
    wget -O $weights_file "https://drive.google.com/uc?export=download&id=0B3gersZ2cHIxVFI1Rjd5aDgwOG8"
fi

$CAFFE_PATH/build/tools/caffe train -solver="$session_dir/training/solver_train.prototxt" \
-weights=$weights_file \
-gpu 0 2>&1 | tee $session_dir/training/train.log
