from PIL import Image, ImageDraw, ImageFilter, ImageFont
from Error import IrregularError
import math


chinese_punctuations_cannot_at_beginning_of_line = '，。、；】》？！：’”）'
chinese_punctuations_cannot_at_end_of_line = '【《‘“'


class TextLabel(object):
    def __init__(self, text, font, number_of_lines=1, max_width=0, line_spacing=0, text_color=(255, 255, 255),
                 use_shadow=False, shadow_offset=(0, 0), shadow_blur=0.0,
                 shadow_color=(0, 0, 0, 255)):
        self.text = text
        self.font = font
        self.number_of_lines = number_of_lines
        self.max_width = max_width
        self.line_spacing = line_spacing
        self.text_color = text_color
        self.use_shadow = use_shadow
        self.shadow_offset = shadow_offset
        self.shadow_blur = shadow_blur
        self.shadow_color = shadow_color

        self.__mutiline_divided_strings = []
        self.__mutiline_divided_strings_height = []
        self.fittingSize = (0, 0)

    def size_to_fit(self):
        if self.number_of_lines == 1:
            text_size = self.font.getsize(self.text)
            if 0 < self.max_width < text_size[0]:
                raise IrregularError('文字在1行内显示不完')
            else:
                if self.use_shadow:
                    self.fittingSize = (math.ceil(text_size[0] + math.fabs(self.shadow_offset[0]) + self.shadow_blur / 2),
                                        math.ceil(text_size[1] + math.fabs(self.shadow_offset[1]) + self.shadow_blur / 2))
                else:
                    self.fittingSize = (math.ceil(text_size[0]), math.ceil(text_size[1]))
        else:  # 多行
            if self.max_width <= 0:
                raise IrregularError('绘制多行文字时必须设置最大宽度')
            else:
                self._divide_string_to_array(self.text)
                if len(self.__mutiline_divided_strings) > 0:
                    total_height = 0
                    for h in self.__mutiline_divided_strings_height:
                        total_height += h
                    total_height += self.line_spacing * (len(self.__mutiline_divided_strings) - 1)

                    text_size = (self.max_width, total_height)

                    if self.use_shadow:
                        self.fittingSize = (math.ceil(text_size[0] + math.fabs(self.shadow_offset[0]) + self.shadow_blur / 2),
                                            math.ceil(text_size[1] + math.fabs(self.shadow_offset[1]) + self.shadow_blur / 2))
                    else:
                        self.fittingSize = text_size

    def draw_label(self, origin, image):
        assert self.fittingSize != (0, 0), 'must call size_to_fit() before'
        if self.number_of_lines == 1:
            if self.use_shadow:
                shadow_label = Image.new('RGBA', self.fittingSize, 0)
                d = ImageDraw.Draw(shadow_label)
                d.text((0, 0),
                       self.text,
                       self.shadow_color,
                       self.font)
                # trick: 还未搞清ps或css上的text-shadow blur的kernel
                shadow_label = shadow_label.filter(ImageFilter.GaussianBlur(self.shadow_blur / 2.0))
                image.paste(shadow_label,
                            (origin[0] + (0 if self.shadow_offset[0] <= 0 else self.shadow_offset[0]),
                             origin[1] + (0 if self.shadow_offset[1] <= 0 else self.shadow_offset[1])),
                            shadow_label)

                d = ImageDraw.Draw(image)
                d.text((origin[0] + (0 if self.shadow_offset[0] > 0 else -self.shadow_offset[0]),
                        origin[1] + (0 if self.shadow_offset[1] > 0 else -self.shadow_offset[1])),
                       self.text,
                       self.text_color,
                       self.font)
            else:
                d = ImageDraw.Draw(image)
                d.text((origin[0], origin[1]), self.text, self.text_color, self.font)
        else:  # 多行
            if len(self.__mutiline_divided_strings) > 0:
                if self.use_shadow:
                    shadow_label = Image.new('RGBA', self.fittingSize, 0)
                    d = ImageDraw.Draw(shadow_label)

                    last_y = 0
                    for i in range(len(self.__mutiline_divided_strings)):
                        d.text((0, last_y),
                               self.__mutiline_divided_strings[i],
                               self.shadow_color,
                               self.font)
                        last_y += (self.__mutiline_divided_strings_height[i] + self.line_spacing)
                    shadow_label = shadow_label.filter(ImageFilter.GaussianBlur(self.shadow_blur / 2))
                    image.paste(shadow_label,
                                (origin[0] + (0 if self.shadow_offset[0] <= 0 else self.shadow_offset[0]),
                                 origin[1] + (0 if self.shadow_offset[1] <= 0 else self.shadow_offset[1])),
                                shadow_label)

                    last_y = 0
                    d = ImageDraw.Draw(image)
                    for i in range(len(self.__mutiline_divided_strings)):
                        d.text((origin[0] + (0 if self.shadow_offset[0] > 0 else -self.shadow_offset[0]),
                                origin[1] + last_y + (0 if self.shadow_offset[1] > 0 else -self.shadow_offset[1])),
                               self.__mutiline_divided_strings[i],
                               self.text_color,
                               self.font)
                        last_y += (self.__mutiline_divided_strings_height[i] + self.line_spacing)
                else:
                    d = ImageDraw.Draw(image)

                    last_y = 0
                    for i in range(len(self.__mutiline_divided_strings)):
                        d.text((origin[0], origin[1] + last_y),
                               self.__mutiline_divided_strings[i],
                               self.text_color,
                               self.font)
                        last_y += (self.__mutiline_divided_strings_height[i] + self.line_spacing)

    def _mutiline_divided_strings_info(self):
        self.__mutiline_divided_strings = []
        self.__mutiline_divided_strings_height = []

        self._divide_string_to_array(self.text)

        return self.__mutiline_divided_strings, self.__mutiline_divided_strings_height

# FIXME: 无法处理\n
    def _divide_string_to_array(self, text):
        if len(text) == 0:
            return
        if self.font.getsize(text)[0] <= self.max_width:
            self._append_substring_info(text)
            return

        just_more_than_index = -1
        text_just_more_than_max_width = ''
        for i in range(1, len(text) + 1):
            if self.font.getsize(text[:i])[0] > self.max_width:
                just_more_than_index = i
                text_just_more_than_max_width = text[:i]
                break

        if _is_allow_at_beginning_of_line(text_just_more_than_max_width[-1]):  # 最后一个字符可以放在句首
            if _is_allow_at_end_of_line(text_just_more_than_max_width[-2]):  # 倒数第二个字符可以放在句尾
                self._append_substring_info(text_just_more_than_max_width[:(just_more_than_index - 1)])
                self._divide_string_to_array(text[(just_more_than_index - 1):])
            else:  # 倒数第二个字符不能放在句尾，向前遍历直到找到可以放到句尾的
                valid_end_line_index = -1
                for n in range(2, len(text_just_more_than_max_width) - 1):
                    if _is_allow_at_end_of_line(text_just_more_than_max_width[-n]):
                        valid_end_line_index = just_more_than_index - n + 1
                        break
                if valid_end_line_index == -1:  # 整句都找不到可以放在句尾的，直接打断
                    self._append_substring_info(text[:(just_more_than_index - 2)])
                    self._divide_string_to_array(text[(just_more_than_index - 2):])
                else:
                    self._append_substring_info(text[:valid_end_line_index])
                    self._divide_string_to_array(text[valid_end_line_index:])
        else:  # 最后一个字符不可以放在句首，向前遍历找到可以放到句首的
            valid_beginning_line_index = -1
            for n in range(2, len(text_just_more_than_max_width) - 1):
                if _is_allow_at_beginning_of_line(text_just_more_than_max_width[-n]):
                    valid_beginning_line_index = just_more_than_index - n + 1
                    break
            if valid_beginning_line_index == -1:  # 整句都找不到可以放在句首的，直接打断
                self._append_substring_info(text[:(just_more_than_index - 2)])
                self._divide_string_to_array(text[(just_more_than_index - 2):])
            else:
                self._append_substring_info(text[:valid_beginning_line_index])
                self._divide_string_to_array(text[valid_beginning_line_index:])

        if 1 < self.number_of_lines < len(self.__mutiline_divided_strings):
            raise IrregularError('文字在{}行内显示不完'.format(self.number_of_lines))

    def _append_substring_info(self, substring):
        self.__mutiline_divided_strings.append(substring)
        self.__mutiline_divided_strings_height.append(self.font.getsize(substring)[1])


def _is_allow_at_beginning_of_line(text):
    return chinese_punctuations_cannot_at_beginning_of_line.find(text) == -1


def _is_allow_at_end_of_line(text):
    return chinese_punctuations_cannot_at_end_of_line.find(text) == -1
