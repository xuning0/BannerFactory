from PIL import Image, ImageFont, ImageDraw
from Error import IrregularError
from TextLabel import TextLabel


dst_large_size = (1250, 540)
dst_small_size = (1080, 540)

# 标题和描述所占目标大尺寸的百分比位置：x1, y1, x2, y2 ，左上点和右下点
roi_of_large_size = (0.12, 0.38, 0.88, 0.85)

left_padding = 152
bottom_padding = 83

title_max_width = 800
title_font = ImageFont.truetype('SourceHanSansCN-Bold.otf', 49)
title_to_description_spacing = 50
title_line_spacing = 17

description_max_width = 945
description_font = ImageFont.truetype('SourceHanSansCN-Regular.otf', 36)
description_line_spacing = 10

tag_y = 74
tag_height = 76
tag_font = ImageFont.truetype('SourceHanSansCN-Bold.otf', 38)

TAG_TYPE_COLLECTION = 0
TAG_TYPE_ACTIVITY = 1
TAG_TYPE_SIGNING_WRITER = 2
TAG_TYPE_HOT = 3

TAG_COLOR_LIST = [(88, 184, 232), (240, 173, 67), (255, 90, 113), (255, 90, 113)]

SAVE_IMAGE_QUALITY = 50


def process(image, tag, title, description, tag_type=TAG_TYPE_COLLECTION):
    if image.width < dst_large_size[0] or image.height < dst_large_size[1]:
        raise IrregularError('图片尺寸小于目标裁剪尺寸')

    im = _scale_by_width_or_height(image)
    im = crop_around_center(im, dst_large_size)

    description_label_image, description_label_height = _description_label(description)
    title_label_image, title_label_height = _title_label(title)
    description_label_y = int(dst_large_size[1] - bottom_padding - description_label_height)
    title_label_y = int(description_label_y - title_label_height - title_to_description_spacing)

    _draw_gradient(im, title_label_y, dst_large_size[1])

    im.paste(title_label_image, (left_padding, title_label_y), title_label_image)
    im.paste(description_label_image, (left_padding, description_label_y), description_label_image)

    _draw_tag(im, tag, tag_type)

    return im


def crop_around_center(image, dst_size):
    return image.crop(((image.width - dst_size[0]) / 2,
                       (image.height - dst_size[1]) / 2,
                       (image.width + dst_size[0]) / 2,
                       (image.height + dst_size[1]) / 2))


# ----------- Private ------------
def _scale_by_width_or_height(image):
    trying_height = dst_large_size[0] / image.width * image.height
    if trying_height > dst_large_size[1]:
        return image.resize((dst_large_size[0], int(trying_height)))
    else:
        return image.resize((int(dst_large_size[1] / image.height * image.width), dst_large_size[1]))


def _description_label(description):
    label = TextLabel(description, description_font, 2, description_max_width, description_line_spacing)
    label_image = label.label()
    return label_image, label.fittingSize[1]


def _title_label(title):
    label = TextLabel(title, title_font, 2, title_max_width, title_line_spacing)
    label_image = label.label()
    return label_image, label.fittingSize[1]


def _draw_gradient(image, y1, y2):
    w = image.width
    h = y2 - y1
    gradient_view = Image.new('RGBA', (w, h))
    d = ImageDraw.ImageDraw(gradient_view)
    for y in range(gradient_view.height):
        d.line((0, y, w, y), (0, 0, 0, int(y / h * 0.7 * 255)))
    image.paste(gradient_view, (0, y1), gradient_view)


def _draw_tag(image, tag, tag_type):
    label = TextLabel(tag, tag_font)
    label_image = label.label()

    type = tag_type
    if tag_type > len(TAG_COLOR_LIST) - 3:
        type = 0
    color = TAG_COLOR_LIST[type]

    # trick: 绘制N倍图，然后以抗锯齿模式resize成1倍尺寸
    trick_scale = 4
    trick_tag_view_size = ((label.fittingSize[0] + tag_height) * trick_scale, tag_height * trick_scale)
    tag_view = Image.new('RGBA', trick_tag_view_size, (*color, 0))
    draw = ImageDraw.Draw(tag_view)
    draw.pieslice((0, 0, trick_tag_view_size[1], trick_tag_view_size[1]), 90, 270, color)
    draw.rectangle((trick_tag_view_size[1] / 2, 0, trick_tag_view_size[1] / 2 + label.fittingSize[0] * trick_scale,
                    trick_tag_view_size[1]), color)
    draw.pieslice((label.fittingSize[0] * trick_scale, 0, trick_tag_view_size[0], trick_tag_view_size[1]),
                  270, 90, color)
    tag_view = tag_view.resize((label.fittingSize[0] + tag_height, tag_height), Image.ANTIALIAS)

    tag_view.paste(label_image, (int(tag_height / 2), int((tag_height - label.fittingSize[1]) / 2)), label_image)

    image.paste(tag_view, (left_padding, tag_y), tag_view)
