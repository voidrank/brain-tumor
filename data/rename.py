import os

DIRECTORIES = ["input0", "input1", "input2", "input3", "output"]
INDEX_RANGE = range(67, 133)

count = 0
for i in INDEX_RANGE:
    for dir_name in DIRECTORIES:
        os.rename(os.path.join(dir_name, str(i)+".png"), os.path.join(dir_name, str(count)+".png"))
    count = count + 1


