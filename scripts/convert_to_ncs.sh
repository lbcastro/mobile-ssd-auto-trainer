#!/bin/bash

python3 /opt/intel/computer_vision_sdk/deployment_tools/model_optimizer/mo_caffe.py --data_type=FP16 --input_model=$1 --batch 1
