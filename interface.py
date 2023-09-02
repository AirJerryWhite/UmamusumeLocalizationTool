import sys

from PySide6.QtCore import Qt, QLocale, QTranslator
from PySide6.QtWidgets import QApplication

from libs.window import Window

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)

    translator = QTranslator()
    app.installTranslator(translator)

    w = Window()
    w.show()
    app.exec_()
