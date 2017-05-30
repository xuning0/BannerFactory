import sys
import os


def resource_abs_path():
    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        bundle_dir = sys._MEIPASS
    else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(bundle_dir, 'Resource')

# Qt的输入框用displayText取到的是已经转成\\n的。这里恢复到\n
# 终端取到的string也是这样
def restoreNewlineCharacter(text):
    return text.replace('\\n', '\n')