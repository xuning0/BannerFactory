from PIL import ImageFont
from TextLabel import TextLabel, _is_allow_at_end_of_line, _is_allow_at_beginning_of_line
import unittest
from Error import IrregularError


class TestLabel(unittest.TestCase):
    def test_break_line1(self):
        label = TextLabel('编程，众所周知被定义为知识工作。所有的知识工作，从业者和门外汉都喜欢把它神秘化……',
                          ImageFont.truetype('../Resource/SourceHanSansCN-Regular.otf', 38),
                          2,
                          874)
        label.size_to_fit()
        self.assertTrue(_is_allow_at_end_of_line((label._TextLabel__mutiline_divided_strings[0])[-1]))
        self.assertTrue(_is_allow_at_beginning_of_line((label._TextLabel__mutiline_divided_strings[1])[0]))

    def test_break_line2(self):
        label = TextLabel('一二三四五六七八九十十一十二十三十四十五说：“《麻烦》哈哈哈哈”',
                          ImageFont.truetype('../Resource/SourceHanSansCN-Regular.otf', 38),
                          2,
                          874)
        label.size_to_fit()
        self.assertEqual(label._TextLabel__mutiline_divided_strings[0], '一二三四五六七八九十十一十二十三十四十五说：')
        self.assertEqual(label._TextLabel__mutiline_divided_strings[1], '“《麻烦》哈哈哈哈”')

    def test_LF1(self):
        label = TextLabel('给大家讲一个真实的故事。\n上初中时，班里有一个长得极美的小太妹。',
                          ImageFont.truetype('../Resource/SourceHanSansCN-Regular.otf', 38),
                          2,
                          874)
        label.size_to_fit()
        self.assertEqual(label._TextLabel__mutiline_divided_strings[0], '给大家讲一个真实的故事。')
        self.assertEqual(label._TextLabel__mutiline_divided_strings[1], '上初中时，班里有一个长得极美的小太妹。')

    def test_LF2(self):
        label = TextLabel('给大家讲一个真实的故事。一二三四五六七八九十十一十二十三十四十五\n上初中时，班里有一个长得极美的小太妹。',
                          ImageFont.truetype('../Resource/SourceHanSansCN-Regular.otf', 38),
                          2,
                          874)
        with self.assertRaises(IrregularError):
            label.size_to_fit()
        self.assertEqual(label._TextLabel__mutiline_divided_strings[0], '给大家讲一个真实的故事。一二三四五六七八九十十')
        self.assertEqual(label._TextLabel__mutiline_divided_strings[1], '一十二十三十四十五')
        self.assertEqual(label._TextLabel__mutiline_divided_strings[2], '上初中时，班里有一个长得极美的小太妹。')
