import os
from PIL import Image

DIRECTORIES = ["input0", "input1", "input2", "input3", "output"]
INDEX_RANGE = 66

for i in range(66):
    for dir_name in DIRECTORIES:
        im = Image.open(os.path.join(dir_name, str(i) + ".png"))
        for j in range(1,4):
            im = im.rotate(90)
            im.save(os.path.join(dir_name, str(i+j*INDEX_RANGE) + ".png"))

