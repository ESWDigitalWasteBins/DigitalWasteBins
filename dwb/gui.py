import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QWidget, \
    QPushButton, QHBoxLayout, QVBoxLayout, QAction, qApp
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon


def center_window(window) -> None:
    window_geometry = window.frameGeometry()
    center = QDesktopWidget().availableGeometry().center()
    window_geometry.moveCenter(center)
    window.move(window_geometry.topLeft())


class DWBSetup(QMainWindow):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width, self.screen_height = screen_width, screen_height
        self.init_UI()

    def init_UI(self):
        quit_act = QAction(QIcon('exit24.png'), '&Exit', self)
        quit_act.setShortcut('Ctrl+Q')
        quit_act.setStatusTip('Quit application')
        quit_act.triggered.connect(qApp.quit)

        self.statusBar()

        file_menu = self.menuBar().addMenu('&File')
        file_menu.addAction(quit_act)

        # OK Button
        # ok_btn = QPushButton('OK')
        # ok_btn.resize(ok_btn.sizeHint())
        # Quit Button
        # quit_btn = QPushButton('Quit')
        # quit_btn.clicked.connect(QCoreApplication.instance().quit)
        # quit_btn.resize(quit_btn.sizeHint())

        # hbox = QHBoxLayout()
        # hbox.addStretch(1)
        # hbox.addWidget(ok_btn)
        # hbox.addWidget(quit_btn)
        #
        # vbox = QVBoxLayout()
        # vbox.addStretch(1)
        # vbox.addLayout(hbox)
        #
        # self.setLayout(vbox)

        self.resize(2/3 * self.screen_width, 2/3 * self.screen_height)
        self.center()
        self.setWindowTitle('Digital Waste Bins Setup')
        self.show()

    def center(self):
        window_geometry = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        window_geometry.moveCenter(center)
        self.move(window_geometry.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dims = app.primaryScreen().size()
    ex = DWBSetup(dims.width(), dims.height())
    sys.exit(app.exec_())
