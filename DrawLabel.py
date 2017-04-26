from PIL import Image, ImageDraw, ImageFont

test_text = 'Apple这个问题《甩给佟丽娅的时候》，她的回答也劲爆得很：“只要回家就好。”'
test_font = ImageFont.truetype('SourceHanSansCN-Regular.otf', 36)

divided_strings = []
chinese_punctuations_cannot_at_beginning_of_line = '，。、；】》？！：’”）'
chinese_punctuations_cannot_at_end_of_line = '【《‘“'


def draw(text, font, number_of_lines=1, max_width=0, line_spacing=0, text_color=(255, 255, 255), background_color=0):
    if number_of_lines == 1:
        text_size = font.getsize(text)
        if 0 < max_width < text_size[0]:
            print('文字在1行内显示不完')
            return
        else:
            label = Image.new('RGBA', text_size, background_color)
            d = ImageDraw.Draw(label)
            d.text((0, 0), text, text_color, font)
    else:  # 多行
        if max_width <= 0:
            print('绘制多行文字时必须设置最大宽度')
            return
        else:
            global divided_strings
            divided_strings = []
            _divide_string_to_array(text, font, number_of_lines, max_width)
            if len(divided_strings) > 0:
                label = Image.new('RGBA', (
                    max_width, 50 * len(divided_strings) + line_spacing * (len(divided_strings) - 1)),
                                  background_color)
                d = ImageDraw.Draw(label)
                for i in range(len(divided_strings)):
                    d.text((0, i * (50 + line_spacing)), divided_strings[i], text_color, font)

    label.show()


def _divide_string_to_array(text, font, number_of_lines, max_width):
    global divided_strings

    if len(text) == 0:
        return
    if font.getsize(text)[0] <= max_width:
        divided_strings.append(text)
        return

    just_more_than_index = -1
    text_just_more_than_max_width = ''
    for i in range(1, len(text)):
        if font.getsize(text[:i])[0] > max_width:
            just_more_than_index = i
            text_just_more_than_max_width = text[:i]
            break

    if _is_allow_at_beginning_of_line(text_just_more_than_max_width[-1]):  # 最后一个字符可以放在句首
        if _is_allow_at_end_of_line(text_just_more_than_max_width[-2]):  # 倒数第二个字符可以放在句尾
            divided_strings.append(text_just_more_than_max_width[:(just_more_than_index - 1)])
            _divide_string_to_array(text[(just_more_than_index - 1):], font, number_of_lines, max_width)
        else:  # 倒数第二个字符不能放在句尾，向前遍历直到找到可以放到句尾的
            valid_end_line_index = -1
            for n in range(2, len(text_just_more_than_max_width) - 1):
                if _is_allow_at_end_of_line(text_just_more_than_max_width[-n]):
                    valid_end_line_index = just_more_than_index - n + 1
                    break
            if valid_end_line_index == -1:  # 整句都找不到可以放在句尾的，直接打断
                divided_strings.append(text[:(just_more_than_index - 2)])
                _divide_string_to_array(text[(just_more_than_index - 2):], font, number_of_lines, max_width)
            else:
                divided_strings.append(text[:valid_end_line_index])
                _divide_string_to_array(text[valid_end_line_index:], font, number_of_lines, max_width)
    else:  # 最后一个字符不可以放在句首，向前遍历找到可以放到句首的
        valid_beginning_line_index = -1
        for n in range(2, len(text_just_more_than_max_width) - 1):
            if _is_allow_at_beginning_of_line(text_just_more_than_max_width[-n]):
                valid_beginning_line_index = just_more_than_index - n + 1
                break
        if valid_beginning_line_index == -1:  # 整句都找不到可以放在句首的，直接打断
            divided_strings.append(text[:(just_more_than_index - 2)])
            _divide_string_to_array(text[(just_more_than_index - 2):], font, number_of_lines, max_width)
        else:
            divided_strings.append(text[:valid_beginning_line_index])
            _divide_string_to_array(text[valid_beginning_line_index:], font, number_of_lines, max_width)

    if 1 < number_of_lines < len(divided_strings):
        print('文字在{}行内显示不完'.format(number_of_lines))
        return


def _is_allow_at_beginning_of_line(text):
    return chinese_punctuations_cannot_at_beginning_of_line.find(text) == -1


def _is_allow_at_end_of_line(text):
    return chinese_punctuations_cannot_at_end_of_line.find(text) == -1



draw(test_text, test_font, 3, 300)


# 我和你的额："哈哈"
# 0 1 2 34 567 8 9
