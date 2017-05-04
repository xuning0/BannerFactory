import sys
from BFMainWindow import BFMainWindow
from PyQt5.QtWidgets import QApplication
from raven import Client


def handle_exception(exctype, value, traceback):
    client.captureException((exctype, value, traceback))

if __name__ == '__main__':
    client = Client('https://9cdee7750e2a4b18b83138bd841c03bc:ba0ab74060fa47d29efc99fc18eb18d7@sentry.io/164738')
    sys.excepthook = handle_exception

    app = QApplication(sys.argv)
    window = BFMainWindow()
    sys.exit(app.exec_())
