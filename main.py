import sys
import os
from argparse import ArgumentParser, RawTextHelpFormatter
from BFMainWindow import BFMainWindow
from PyQt5.QtWidgets import QApplication
from raven import Client
import CommandLineHelper


def handle_exception(exctype, value, traceback):
    client.captureException((exctype, value, traceback))


def run_command_line():
    parser = ArgumentParser(description='Generate Jianshu common banners for both web and app easily.',
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('-i', '--input', dest='input', required=True, help='path for input image')
    parser.add_argument('--tag', dest='tag', required=True, help='tag string for banner')
    parser.add_argument('--type', dest='type', help='tag type for banner:\n'
                                                    '   0 - Collection\n'
                                                    '   1 - Activity\n'
                                                    '   2 - Signing writer\n'
                                                    '   3 - Hot')
    parser.add_argument('--title', dest='title', required=True, help='title for banner')
    parser.add_argument('--desc', dest='desc', required=True, help='desc for banner')
    parser.add_argument('-o', '--output', dest='output', required=True,
                        help='directory for banner images(default is ~/Desktop)')

    args = parser.parse_args()
    if not os.path.isfile(args.input):
        print('{} is not a file'.format(args.input))
        return
    if not os.path.exists(args.input):
        print('{} is not exist'.format(args.input))
        return
    if not os.path.isdir(args.output):
        print('{} is not a dir'.format(args.output))
        return
    CommandLineHelper.generate(os.path.expanduser(args.input), args.tag, args.title, args.desc,
                               os.path.expanduser(args.output), args.type)


if __name__ == '__main__':
    # release时，1、填入sentry url（防止开源下私钥泄露），2、取消sys.excepthook行的注释
    client = Client()
    # sys.excepthook = handle_exception

    if len(sys.argv) == 1:
        app = QApplication(sys.argv)
        window = BFMainWindow()
        sys.exit(app.exec_())
    else:
        run_command_line()
