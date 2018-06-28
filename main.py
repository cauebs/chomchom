import sys
import PyQt5.QtWidgets as qtw
from chomchom import Control


def main():
    app = qtw.QApplication(sys.argv)
    Control()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
