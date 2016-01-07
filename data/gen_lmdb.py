import numpy as np
import lmdb
import sys
import PIL
import os

# Change this contant to your pycaffe path
PY_CAFFE_DIR = "/home/lancy/caffe/python"
sys.path.insert(0, PY_CAFFE_DIR)

import caffe


DIRECTORIES = ["input0", "input1", "input2", "input3", "output"]
WIDTH = 256
HEIGHT = 256
TRAIN_SET = range(200)
TEST_SET = range(200, 264)

def make_lmdb_input(lmdbname, channel_directories, range_set):

    X = np.zeros((len(range_set), len(channel_directories), WIDTH, HEIGHT), dtype=np.double)
    map_size = X.nbytes * 10
    
    env = lmdb.open(lmdbname, map_size=map_size)

    count = 0
    for i in range_set:
        with env.begin(write=True) as txn:
            filename = str(i) + ".png"
            datum = caffe.proto.caffe_pb2.Datum()
            datum.channels = X.shape[1]
            datum.height = X.shape[2]
            datum.width = X.shape[3]
            for j in range(len(channel_directories)):
                dirname = channel_directories[j]
                X[count][j] = np.asarray(PIL.Image.open(os.path.join(dirname, filename)), dtype=np.double) / 255
            datum.data = X[count].tobytes()
            str_id = '{:08}'.format(count)
            txn.put(str_id.encode("ascii"), datum.SerializeToString())
            count += 1
            
def make_lmdb_output(lmdbname, range_set):
    
    X = np.zeros((len(range_set), 1, WIDTH, HEIGHT), dtype=np.uint8)
    map_size = X.nbytes * 10
    
    env = lmdb.open(lmdbname, map_size=map_size)

    count = 0;
    for i in range_set:
        with env.begin(write=True) as txn:
            filename = str(i) + ".png"
            datum = caffe.proto.caffe_pb2.Datum()
            datum.channels = X.shape[1]
            datum.height = X.shape[2]
            datum.width = X.shape[3]
            m = np.asarray(PIL.Image.open(os.path.join("output", filename)), dtype=np.double)
            for i in range(WIDTH):
                for j in range(HEIGHT):
                    if m[i][j] > 200:
                        X[count][0][i][j] = 2
                    elif m[i][j] >= 100:
                        X[count][0][i][j] = 1
                    else:
                        X[count][0][i][j] = 0
            datum.data = X[count].tobytes()
            str_id = "{:08}".format(count)
            txn.put(str_id.encode("ascii"), datum.SerializeToString())
            count += 1

make_lmdb_input("train_input_lmdb", ["input" + str(i) for i in range(4)], TRAIN_SET)
make_lmdb_output("train_output_lmdb", TRAIN_SET)

make_lmdb_input("test_input_lmdb", ["input" + str(i) for i in range(4)], TEST_SET)
make_lmdb_output("test_output_lmdb", TEST_SET)

