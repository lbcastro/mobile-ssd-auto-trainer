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

session_dir=$1
session=$(basename "$1")
training_dir=$session_dir/training
root_dir=$(cd $( dirname ${BASH_SOURCE[0]} ) && cd .. && pwd )

cls_num=$2
cls_num3=$(expr $2 \* 3)
cls_num6=$(expr $2 \* 6)

trainfile=$training_dir/train.prototxt
testfile=$training_dir/test.prototxt
deployfile=$training_dir/deploy.prototxt
solver_train=$training_dir/solver_train.prototxt
solver_test=$training_dir/solver_test.prototxt

cp $root_dir/templates/MobileNetSSD_train_template.prototxt $trainfile
sed -i "s/cls6x/${cls_num6}/g" $trainfile
sed -i "s/cls3x/${cls_num3}/g" $trainfile
sed -i "s/cls1x/${cls_num}/g" $trainfile
sed -i "s|trainval_lmdb|"$training_dir"/lmdb/"$session"_trainval_lmdb|g" $trainfile
sed -i "s|labelmap.prototxt|"$training_dir"/labelmap_"$session".prototxt|g" $trainfile

cp $root_dir/templates/MobileNetSSD_test_template.prototxt $testfile
sed -i "s/cls6x/${cls_num6}/g" $testfile
sed -i "s/cls3x/${cls_num3}/g" $testfile
sed -i "s/cls1x/${cls_num}/g" $testfile
sed -i "s|test_lmdb|"$training_dir"/lmdb/"$session"_test_lmdb|g" $testfile
sed -i "s|labelmap.prototxt|"$training_dir"/labelmap_"$session".prototxt|g" $testfile

cp $root_dir/templates/MobileNetSSD_deploy_template.prototxt $deployfile
sed -i "s/cls6x/${cls_num6}/g" $deployfile
sed -i "s/cls3x/${cls_num3}/g" $deployfile
sed -i "s/cls1x/${cls_num}/g" $deployfile

mkdir -p $training_dir/snapshots

cp $root_dir/templates/solver_train.prototxt $solver_train
sed -i "s|example/MobileNetSSD_train.prototxt|$trainfile|g" $solver_train
sed -i "s|example/MobileNetSSD_test.prototxt|$testfile|g" $solver_train
sed -i "s|snapshot/mobilenet|"$training_dir"/snapshots/"$session"|g" $solver_train
