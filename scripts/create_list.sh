#!/bin/bash

root_dir="datasets/"
sub_dir=ImageSets/Main
cur_dir=$(cd $( dirname ${BASH_SOURCE[0]} ) && cd .. && pwd )
for dataset in trainval test
do
  dst_file=$cur_dir/$root_dir/$1/$dataset.txt
  if [ -f $dst_file ]
  then
    rm -f $dst_file
  fi
  for name in $1
  do
    echo "Create list for $name $dataset..."
    dataset_file=$cur_dir/$root_dir/$1/$sub_dir/$dataset.txt

    img_file=$cur_dir/$dataset"_img.txt"
    echo $img_file
    cp $dataset_file $img_file
    sed -i 's/\s.*$//' $img_file
    sed -i "s/^/$name\/JPEGImages\//g" $img_file

    label_file=$cur_dir/$dataset"_label.txt"
    cp $dataset_file $label_file
    sed -i 's/[^ ]* //' $label_file
    sed -i "s/^/$name\/Annotations\//g" $label_file

    paste -d' ' $img_file $label_file >> $dst_file

    rm -f $label_file
    rm -f $img_file
  done

  # Generate image name and size infomation.
  if [ $dataset == "test" ]
  then
    $CAFFE_PATH/build/tools/get_image_size $root_dir $dst_file $cur_dir/$root_dir/$1/$dataset"_name_size.txt"
  fi

  # Shuffle trainval file.
  if [ $dataset == "trainval" ]
  then
    rand_file=$dst_file.random
    cat $dst_file | perl -MList::Util=shuffle -e 'print shuffle(<STDIN>);' > $rand_file
    mv $rand_file $dst_file
  fi
done


