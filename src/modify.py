import glob
from PIL import Image
import os

path = "../docs/files/original/*.jpg"

files = sorted(glob.glob(path))

w = 2400

for i in range(len(files)):
    file = files[i]
    img = Image.open(file)   
    img_resize = img.resize((w, int(w * img.size[1] / img.size[0])))

    opath = file.replace("/original/", "/large/")

    if not os.path.exists(opath):
        img_resize.save(opath)
