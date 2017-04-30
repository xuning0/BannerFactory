import sys
from BFMainWindow import BFMainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BFMainWindow()
    sys.exit(app.exec_())
