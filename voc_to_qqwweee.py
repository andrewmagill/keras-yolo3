#
# This script is intended to convert ImageNet annotations (which are written in Pascal
# VOC format) to the one file one line per image format qqwweee uses in this project
#

import xml.etree.ElementTree as ET
import os

CWD = os.getcwd()
ROOT = os.path.abspath(os.path.join(CWD, os.pardir))
ILSVRC = "ILSVRC"
IMAGES = "Data"
ANNOTATIONS = "Annotations"
TRAIN = "CLS-LOC/train"
VAL = "CLS-LOC/val"
MODEL_DATA = "model_data"
OUT_FILENAME = "train.txt"

# limit the number of images per class
LIMIT = 20 # 500

ANNOTATIONS_BASEPATH_TRAIN = os.path.join(ROOT, ILSVRC, ANNOTATIONS, TRAIN)
ANNOTATIONS_BASEPATH_VAL = os.path.join(ROOT, ILSVRC, ANNOTATIONS, VAL)

IMAGES_BASEPATH_TRAIN = os.path.join(ROOT, ILSVRC, IMAGES, TRAIN)
IMAGES_BASEPATH_VAL = os.path.join(ROOT, ILSVRC, IMAGES, VAL)

classes = os.listdir(ANNOTATIONS_BASEPATH_TRAIN)

# write out list of classes
with open(os.path.join(CWD, MODEL_DATA, "voc_classes.txt"), "w") as f:
        for wnid in classes:
            f.write("%s\n" % wnid)

# convert train annotations
outfile = open(os.path.join(CWD, OUT_FILENAME), "w")

for wnid in classes:
    image_path = os.path.join(IMAGES_BASEPATH_TRAIN, wnid)
    class_path = os.path.join(ANNOTATIONS_BASEPATH_TRAIN, wnid)
    files = os.listdir(class_path)
    for filename in files[:LIMIT]:

        print(filename)
        outfile.write(os.path.join(image_path, filename.replace(".xml",".JPEG")))

        with open(os.path.join(class_path, filename)) as f:
            tree=ET.parse(f)

        root = tree.getroot()

        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult)==1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (int(xmlbox.find('xmin').text),
                    int(xmlbox.find('ymin').text), 
                    int(xmlbox.find('xmax').text), 
                    int(xmlbox.find('ymax').text))
            outfile.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

        outfile.write("\n")

outfile.close()

# TODO convert val annotation
# test does not have annotations
