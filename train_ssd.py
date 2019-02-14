import subprocess
import os
import datetime
import shutil
import argparse

# Change dataset_root to where your data is stored. It assumes the following structure:

# dataset_root/
# ---- label/
# -------- images/
# -------- annotations/

dataset_root = ""

IMAGES_ROOT = "images"
ANNOTATIONS_ROOT = "annotations"
TRAIN_IMAGES_ROOT = "JPEGImages"
TRAIN_ANNOTATIONS_ROOT = "Annotations"
TRAIN_MAIN_ROOT = "ImageSets/Main"

# Select labels to use. These must be present in the dataset_root folder.
labels = []

# Background label is always required.
labels.insert(0, "background")

# Retrieves specified data from the main dataset.
images_paths = []
annotations_paths = []

def make_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset', type=str, required=True, help='Folder containing annotated data')
    args = parser.parse_args()
    return args

import xml.etree.ElementTree as ET

def read_content(xml_file: str):

    tree = ET.parse(xml_file)
    root = tree.getroot()

    labels = []

    for boxes in root.iter('object'):

        label = boxes.find('name').text
        labels.append(label)

    return labels

# Creates the labelmap.prototxt file, using the specified labels to automatically generate it.
def generate_labelmap_line(label, name, index):
    return "item {\n\tname: \"" + label + "\"\n\tlabel: " + str(
        index) + "\n\tdisplay_name: \"" + name + "\"\n}"

if __name__ == "__main__":
    args = make_arguments()
    session_root = args.dataset
    dataset_root = os.path.join(session_root, "results", "annotated")

    for file in os.listdir(dataset_root):
        if file.endswith('.xml'):
            continue
        image_path = os.path.join(dataset_root, file)

        if not os.path.isfile(image_path):
            continue

        annotation_path = os.path.splitext(image_path)[0] + '.xml'

        if not os.path.isfile(annotation_path):
            continue

        current_labels = read_content(annotation_path)

        skip = False
        for label in current_labels:
            if label not in labels:
                labels.append(label)

        images_paths.append(image_path)
        annotations_paths.append(annotation_path)

    print(labels)
    if len(images_paths) < 100:
        exit("This training procedure requires at least 100 annotated images. Only " + str(len(images_paths)) + " were provided.")

    # Organize folder structure
    session = os.path.basename(session_root)
    training_path = os.path.join(session_root, "training/")
    os.makedirs(training_path)
    train_images_path = os.path.join(training_path, TRAIN_IMAGES_ROOT)
    os.mkdir(train_images_path)
    train_annotations_path = os.path.join(training_path, TRAIN_ANNOTATIONS_ROOT)
    os.mkdir(train_annotations_path)
    train_main_path = os.path.join(training_path, TRAIN_MAIN_ROOT)
    os.makedirs(train_main_path)

    # Images to ROOT/JPEGImages
    for image_file in images_paths:
        shutil.copyfile(image_file, os.path.join(train_images_path, os.path.basename(image_file)))

    # Annotations to ROOT/Annotations
    for annotation_file in annotations_paths:
        shutil.copyfile(annotation_file,
                        os.path.join(train_annotations_path, os.path.basename(annotation_file)))

    # Divides dataset in train and test paths. Paths to train samples go to
    # ROOT/ImageSets/Main/trainval.txt and paths to test samples go to ROOT/ImageSets/Main/test.txt

    # Percentage of the dataset that is used for testing
    PERCENTAGE_TEST = 10

    index_test = round(100 / PERCENTAGE_TEST)

    counter = 1

    train_file = open(os.path.join(train_main_path, "trainval.txt"), 'w')
    test_file = open(os.path.join(train_main_path, "test.txt"), 'w')

    for image_file in os.listdir(train_images_path):
        image_path = os.path.join(train_images_path, image_file)
        if not os.path.isfile(image_path):
            continue
        annotation_file = os.path.join(train_annotations_path, os.path.splitext(image_file)[0] + '.xml')
        if not os.path.isfile(annotation_file):
            continue

        name = os.path.basename(image_path)
        line = name + " " + os.path.splitext(name)[0] + ".xml\n"

        if counter == index_test:
            counter = 1
            test_file.write(line)
        else:
            train_file.write(line)
            counter += 1

    train_file.close()
    test_file.close()

    scripts_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "scripts")

    # Uses the create_list.sh script to generate test_name_size.txt, test.txt, trainval.txt
    subprocess.run("chmod +x " + os.path.join(scripts_directory, "create_list.sh"), shell=True)
    subprocess.check_call([os.path.join(scripts_directory, "create_list.sh"), session_root])

    labelmap = "labelmap_" + session + ".prototxt"
    labelmap_file = open(os.path.join(training_path, labelmap), 'w')

    count = 0
    for label in labels:
        labelmap_file.write(generate_labelmap_line(label, label, count) + "\n")
        count += 1

    labelmap_file.close()

    plain_text_labelmap = "labels_" + session + ".txt"
    plain_text_labelmap_file = open(os.path.join(training_path, plain_text_labelmap), 'w')
    plain_text_labelmap_file.write('.'.join(labels))
    plain_text_labelmap_file.close()

    # Uses the create_data.sh script to create the lmdb
    subprocess.run("chmod +x " + os.path.join(scripts_directory, "create_data.sh"), shell=True)
    subprocess.check_call([os.path.join(scripts_directory, "create_data.sh"), session_root])

    # Uses the gen_model.sh to generate train, test, deploy and solver .prototxt files
    subprocess.run("chmod +x " + os.path.join(scripts_directory, "gen_model.sh"), shell=True)
    subprocess.check_call([os.path.join(scripts_directory, "gen_model.sh"), session_root, str(len(labels))])

    # Runs the train script pointing to a default mobilenet ssd model
    subprocess.run("chmod +x " + os.path.join(scripts_directory, "train.sh"), shell=True)
    subprocess.check_call([os.path.join(scripts_directory, "train.sh"), session_root])
