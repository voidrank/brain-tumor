import PIL.Image
import numpy as np

SIZE = 264
WIDTH = 256
HEIGHT = 256

for index in range(SIZE):
    m = np.array(PIL.Image.open("output/" + str(index) + ".png"))
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if m[i][j] < 100:
                m[i][j] = 0
            elif m[i][j] > 200:
                m[i][j] = 255
            else:
                m[i][j] = 150
    im = PIL.Image.fromarray(np.uint8(m))
    im.save("output/" + str(index) + ".png")
