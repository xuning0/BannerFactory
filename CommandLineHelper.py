import ImageProcess
from PIL import Image
import time
import os


def generate(input_path, tag, title, desc, output, tag_type):
    im = Image.open(input_path)
    ttype = tag_type
    if ttype is None:
        ttype = 0
    im = ImageProcess.process(im, tag, title, desc, ttype)

    image_name = int(time.time())
    dir_name = output
    if dir_name is None:
        dir_name = '/Users/xuning/Desktop'

    im.save(os.path.join(dir_name, 'Web_' + str(image_name) + '.jpg'),
            quality=ImageProcess.SAVE_IMAGE_QUALITY,
            optimize=True)

    app_image = ImageProcess.crop_around_center(im, ImageProcess.dst_small_size)
    app_image.save(os.path.join(dir_name, 'App_' + str(image_name) + '.jpg'),
                   quality=ImageProcess.SAVE_IMAGE_QUALITY,
                   optimize=True)
