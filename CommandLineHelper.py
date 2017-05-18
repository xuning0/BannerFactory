import ImageProcess
from PIL import Image
import time
import os


def generate(input_path, tag, title, desc, output, tag_type):
    im = Image.open(input_path)
    if tag_type is None:
        ttype = 0
    else:
        ttype = int(tag_type)

    web_im = ImageProcess.process(0, im, tag, title, desc, ttype)

    image_name = int(time.time())

    web_im.save(os.path.join(output, 'Web_' + str(image_name) + '.jpg'),
                quality=ImageProcess.SAVE_IMAGE_QUALITY,
                optimize=True)

    app_im = ImageProcess.process(1, im, tag, title, desc, ttype)
    app_im.save(os.path.join(output, 'App_' + str(image_name) + '.jpg'),
                quality=ImageProcess.SAVE_IMAGE_QUALITY,
                optimize=True)
