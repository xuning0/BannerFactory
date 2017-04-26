from PIL import Image, ImageFont, ImageDraw
from Error import IrregularError
from TextLabel import TextLabel


test_image = Image.open('test.jpg')
dst_large_size = (1250, 540)
dst_small_size = (1080, 540)

left_padding = 152

title_max_width = 800
title_font = ImageFont.truetype('SourceHanSansCN-Bold.otf', 49)
title_to_description_spacing = 50
title_line_spacing = 17

description_max_width = 945
description_y = 375
description_font = ImageFont.truetype('SourceHanSansCN-Regular.otf', 36)
description_line_spacing = 10

tag_y = 74
tag_height = 76
tag_font = ImageFont.truetype('SourceHanSansCN-Bold.otf', 38)

TAG_TYPE_COLLECTION = 0
TAG_TYPE_ACTIVITY = 1
TAG_TYPE_SIGNING_WRITER = 2
TAG_TYPE_HOT = 3


def process(image, tag, title, description, tag_type=TAG_TYPE_COLLECTION):
    if image.width < dst_large_size[0] or image.height < dst_large_size[1]:
        raise IrregularError('图片尺寸小于目标裁剪尺寸')

    im = _scale_by_width_or_height(image)
    im = im.crop(((im.width - dst_large_size[0]) / 2,
                  (im.height - dst_large_size[1]) / 2,
                  (im.width + dst_large_size[0]) / 2,
                  (im.height + dst_large_size[1]) / 2))
    _draw_description_label(im, description)
    _draw_title_label(im, title)
    _draw_tag(im, tag, tag_type)
    return im


def _scale_by_width_or_height(image):
    trying_height = dst_large_size[0] / image.width * image.height
    if trying_height > dst_large_size[1]:
        return image.resize((dst_large_size[0], int(trying_height)))
    else:
        return image.resize((int(dst_large_size[1] / image.height * image.width), dst_large_size[1]))


def _draw_description_label(image, description):
    label = TextLabel(description, description_font, 2, description_max_width, description_line_spacing)
    label_image = label.label()
    image.paste(label_image, (left_padding, description_y), label_image)


def _draw_title_label(image, title):
    label = TextLabel(title, title_font, 2, title_max_width, title_line_spacing)
    label_image = label.label()
    image.paste(label_image,
                (left_padding, description_y - label.fittingSize[1] - title_to_description_spacing),
                label_image)


def _draw_tag(image, tag, tag_type):
    label = TextLabel(tag, tag_font)
    label_image = label.label()

    color = 0
    if tag_type == TAG_TYPE_COLLECTION:
        color = (88, 184, 232)
    elif tag_type == TAG_TYPE_ACTIVITY:
        color = (240, 173, 67)
    elif tag_type == TAG_TYPE_SIGNING_WRITER or tag_type == TAG_TYPE_HOT:
        color = (255, 90, 113)

    # trick: 绘制2倍图，然后以抗锯齿模式resize成1倍尺寸
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

final_image = process(test_image, '@IT', '晨兴创投 · 刘芹：我才刚刚理解创投行业，虽然我已入行16年了', '这个问题甩给佟丽娅的时候，她的回答也劲爆得很：“只要回家就好。”')
final_image.save('final.jpg')
