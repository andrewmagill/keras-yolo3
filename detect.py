import os
from PIL import Image
from yolo import YOLO

y = YOLO()

TEST_DIR = "/home/bosworth/work/ILSVRC/Data/CLS-LOC/test"
test_images = os.listdir(TEST_DIR)

f = open("submission_results.csv","w")

for fname in test_images[:200]:
    result = y.detect_image(Image.open(os.path.join(TEST_DIR, fname)))
    f.write("%s\n" % " ".join(result[1:]))

f.close()
