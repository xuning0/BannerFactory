from PIL import Image, ImageFont, ImageDraw
from Error import IrregularError
from TextLabel import TextLabel
import os
import CommonUtil
from ConfigManager import ConfigManager

TAG_TYPE_COLLECTION = 0
TAG_TYPE_ACTIVITY = 1
TAG_TYPE_SIGNING_WRITER = 2
TAG_TYPE_HOT = 3

TAG_COLOR_LIST = [(88, 184, 232), (240, 173, 67), (255, 90, 113), (255, 90, 113)]

SAVE_IMAGE_QUALITY = 55


def process(config_type, image, tag, title, description, tag_type=TAG_TYPE_COLLECTION):
    if image.width < ConfigManager().main_w(config_type) or image.height < ConfigManager().main_h(config_type):
        raise IrregularError('图片尺寸小于目标裁剪尺寸（{}x{}）'.format(ConfigManager().main_w(config_type), ConfigManager().main_h(config_type)))

    im = _scale_by_width_or_height(image, config_type)
    im = _crop_around_center(im, (ConfigManager().main_w(config_type), ConfigManager().main_h(config_type)))

    description_label = _description_label(description, config_type)
    title_label = _title_label(title, config_type)
    description_label_y = int(
        ConfigManager().main_h(config_type) - ConfigManager().desc_b(config_type) - description_label.fittingSize[1])
    title_label_y = int(
        description_label_y - title_label.fittingSize[1] - ConfigManager().title_bottom_spacing_to_desc_y(config_type))

    _draw_gradient(im, title_label_y, ConfigManager().main_h(config_type))

    title_label.draw_label((ConfigManager().title_x(config_type), title_label_y), im)
    description_label.draw_label((ConfigManager().desc_x(config_type), description_label_y), im)

    _draw_tag(im, tag, tag_type, config_type)

    return im


def _crop_around_center(image, dst_size):
    return image.crop(((image.width - dst_size[0]) / 2,
                       (image.height - dst_size[1]) / 2,
                       (image.width + dst_size[0]) / 2,
                       (image.height + dst_size[1]) / 2))


# ----------- Private ------------
def _scale_by_width_or_height(image, config_type):
    trying_height = ConfigManager().main_w(config_type) / image.width * image.height
    if trying_height > ConfigManager().main_h(config_type):
        return image.resize((ConfigManager().main_w(config_type), int(trying_height)))
    else:
        return image.resize((int(ConfigManager().main_h(config_type) / image.height * image.width),
                             ConfigManager().main_h(config_type)))


def _description_label(description, config_type):
    label = TextLabel(description,
                      ImageFont.truetype(
                          os.path.join(CommonUtil.resource_abs_path(), ConfigManager().desc_font(config_type)),
                          ConfigManager().desc_font_size(config_type)),
                      2,
                      ConfigManager().desc_max_width(config_type),
                      ConfigManager().desc_line_spacing(config_type),
                      use_shadow=True,
                      shadow_offset=(0, 3),
                      shadow_blur=7,
                      shadow_color=(0, 0, 0, 128))
    label.size_to_fit()
    return label


def _title_label(title, config_type):
    label = TextLabel(title,
                      ImageFont.truetype(
                          os.path.join(CommonUtil.resource_abs_path(), ConfigManager().title_font(config_type)),
                          ConfigManager().title_font_size(config_type)),
                      2,
                      ConfigManager().title_max_width(config_type),
                      ConfigManager().title_line_spacing(config_type),
                      use_shadow=True,
                      shadow_offset=(0, 3),
                      shadow_blur=7,
                      shadow_color=(0, 0, 0, 128))
    label.size_to_fit()
    return label


def _draw_gradient(image, y1, y2):
    w = image.width
    h = y2 - y1
    gradient_view = Image.new('RGBA', (w, h))
    d = ImageDraw.ImageDraw(gradient_view)
    for y in range(gradient_view.height):
        d.line((0, y, w, y), (0, 0, 0, int(y / h * 0.7 * 255)))
    image.paste(gradient_view, (0, y1), gradient_view)


def _draw_tag(image, tag, tag_type, config_type):
    label = TextLabel(tag,
                      ImageFont.truetype(
                          os.path.join(CommonUtil.resource_abs_path(), ConfigManager().tag_font(config_type)),
                          ConfigManager().tag_font_size(config_type)))
    label.size_to_fit()

    ttype = tag_type
    if tag_type > len(TAG_COLOR_LIST) - 1:
        ttype = 0
    color = TAG_COLOR_LIST[ttype]

    # trick: 绘制N倍图，然后以抗锯齿模式resize成1倍尺寸
    tag_height = ConfigManager().tag_h(config_type)
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

    label.draw_label((int(tag_height / 2), int((tag_height - label.fittingSize[1]) / 2)), tag_view)

    image.paste(tag_view, (ConfigManager().tag_x(config_type), ConfigManager().tag_y(config_type)), tag_view)
