import subprocess
import os
import datetime
import shutil

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

for label in labels:
    label_dir = os.path.join(dataset_root, label)
    if os.path.isdir(label_dir):

        images_root = os.path.join(label_dir, IMAGES_ROOT)

        for image_file in os.listdir(images_root):
            image_path = os.path.join(images_root, image_file)
            if not os.path.isfile(image_path):
                continue
            images_paths.append(image_path)
            annotations_paths.append(
                os.path.splitext(image_path.replace(IMAGES_ROOT, ANNOTATIONS_ROOT))[0] + '.xml')

# Organize folder structure
now = datetime.datetime.now()
session = now.strftime("%Y%m%d_%H%M")
session_path = os.path.join("datasets/", session)
os.makedirs(session_path)
train_images_path = os.path.join(session_path, TRAIN_IMAGES_ROOT)
os.mkdir(train_images_path)
train_annotations_path = os.path.join(session_path, TRAIN_ANNOTATIONS_ROOT)
os.mkdir(train_annotations_path)
train_main_path = os.path.join(session_path, TRAIN_MAIN_ROOT)
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

# Uses the create_list.sh script to generate test_name_size.txt, test.txt, trainval.txt
subprocess.run("chmod +x ./scripts/create_list.sh", shell=True)
subprocess.check_call(['./scripts/create_list.sh', session])


# Creates the labelmap.prototxt file, using the specified labels to automatically generate it.
def generate_labelmap_line(label, name, index):
    return "item {\n\tname: \"" + label + "\"\n\tlabel: " + str(
        index) + "\n\tdisplay_name: \"" + name + "\"\n}"


labelmap = "labelmap_" + session + ".prototxt"
labelmap_file = open(os.path.join(session_path, labelmap), 'w')

count = 0
for label in labels:
    labelmap_file.write(generate_labelmap_line(label, label, count) + "\n")
    count += 1

labelmap_file.close()

# Uses the create_data.sh script to create the lmdb
subprocess.run("chmod +x ./scripts/create_data.sh", shell=True)
subprocess.check_call(['./scripts/create_data.sh', session])

# Uses the gen_model.sh to generate train, test, deploy and solver .prototxt files
subprocess.run("chmod +x ./scripts/gen_model.sh", shell=True)
subprocess.check_call(['./scripts/gen_model.sh', str(len(labels)), session])

# Runs the train script pointing to a default mobilenet ssd model
subprocess.run("chmod +x ./scripts/train.sh", shell=True)
subprocess.check_call(['./scripts/train.sh', session])
