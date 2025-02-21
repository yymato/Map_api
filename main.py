import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
import requests

from ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.press_delta = 0.00001

        self.map_zoom = 5
        self.map_ll = [37.977751, 55.757718]
        self.map_l = 'map'
        self.map_key = ''

        self.refresh_map()

    def refresh_map(self):
        map_params = {
            "ll": ','.join(map(str, self.map_ll)),
            "l": self.map_l,
            'z': self.map_zoom
        }

        response = requests.get('https://static-maps.yandex.ru/1.x/', params=map_params)
        with open('tmp.png', mode='wb') as tmp:
            tmp.write(response.content)

        pixmap = QPixmap()
        pixmap.load('tmp.png')
        self.map_label.setPixmap(pixmap)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_PageUp and self.map_zoom < 17:
            self.map_zoom += 1
        if key == Qt.Key.Key_PageDown and self.map_zoom > 0:
            self.map_zoom -= 1
        if key == Qt.Key.Key_Left:
            self.map_ll[0] -= self.press_delta
        if key == Qt.Key.Key_Right:
            self.map_ll[0] += self.press_delta
        if key == Qt.Key.Key_Up:
            self.map_ll[1] += self.press_delta
        if key == Qt.Key.Key_Down:
            self.map_ll[1] -= self.press_delta

        self.refresh_map()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
