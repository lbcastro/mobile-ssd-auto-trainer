#!/bin/bash

#if test -z $1 ;then
#	echo usage: $0 CLASSNUM
#        echo "        for voc the classnum is 21"
#	exit 1
#fi
#echo $1 |grep '^[0-9]*$' >/dev/null 2>&1
#if [ $? != 0 ];then
#	echo usage: $0 CLASSNUM
#        echo "        for voc the classnum is 21"
#	exit 1
#fi

cls_num=$1
cls_num3=$(expr $1 \* 3)
cls_num6=$(expr $1 \* 6)

cur_dir=$(cd $( dirname ${BASH_SOURCE[0]} ) && cd .. && pwd )

trainfile=datasets/$2/train.prototxt
testfile=datasets/$2/test.prototxt
deployfile=datasets/$2/deploy.prototxt
solver_train=datasets/$2/solver_train.prototxt
solver_test=datasets/$2/solver_test.prototxt

cp templates/MobileNetSSD_train_template.prototxt $trainfile
sed -i "s/cls6x/${cls_num6}/g" $trainfile
sed -i "s/cls3x/${cls_num3}/g" $trainfile
sed -i "s/cls1x/${cls_num}/g" $trainfile
sed -i "s|trainval_lmdb|$cur_dir/datasets/$2/lmdb/$2_trainval_lmdb|g" $trainfile
sed -i "s|labelmap.prototxt|$cur_dir/datasets/$2/labelmap_$2.prototxt|g" $trainfile

cp templates/MobileNetSSD_test_template.prototxt $testfile
sed -i "s/cls6x/${cls_num6}/g" $testfile
sed -i "s/cls3x/${cls_num3}/g" $testfile
sed -i "s/cls1x/${cls_num}/g" $testfile
sed -i "s|test_lmdb|$cur_dir/datasets/$2/lmdb/$2_test_lmdb|g" $testfile
sed -i "s|labelmap.prototxt|$cur_dir/datasets/$2/labelmap_$2.prototxt|g" $testfile

cp templates/MobileNetSSD_deploy_template.prototxt $deployfile
sed -i "s/cls6x/${cls_num6}/g" $deployfile
sed -i "s/cls3x/${cls_num3}/g" $deployfile
sed -i "s/cls1x/${cls_num}/g" $deployfile

mkdir -p datasets/$2/snapshots

cp templates/solver_train.prototxt $solver_train
sed -i "s|example/MobileNetSSD_train.prototxt|$cur_dir/$trainfile|g" $solver_train
sed -i "s|example/MobileNetSSD_test.prototxt|$cur_dir/$testfile|g" $solver_train
sed -i "s|snapshot/mobilenet|$cur_dir/datasets/$2/snapshots/$2|g" $solver_train