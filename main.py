import sys

from Cython import address
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
import requests

from ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.press_delta = 0.1
        self.theme = 'light'
        self.map_zoom = 5
        self.map_ll = [37.977751, 55.757718]
        self.point = ','.join(list(map(str, [37.977751, 55.757718])))
        self.map_l = 'map'
        self.map_key = ''
        self.theme_button.clicked.connect(self.change_theme)
        self.reset_button.clicked.connect(self.reset_result)
        self.search.clicked.connect(self.searc1)
        self.checkBox.stateChanged.connect(self.searc1)
        self.refresh_map()

    def searc1(self):
        if self.lineEdit.text():
            self.point = self.get_coords_from_geocoder(self.lineEdit.text())
            self.map_ll = list(map(float, self.point.split(',')))
            self.plainTextEdit.setPlainText(self.get_coords_from_geocoder(self.point, address=True,
                                                                          index=self.checkBox.isChecked()))
            self.refresh_map()

    def reset_result(self):
        self.lineEdit.setText('')
        self.plainTextEdit.setPlainText('')
        self.map_ll = [37.977751, 55.757718]
        self.point = ','.join(list(map(str, [37.977751, 55.757718])))
        self.refresh_map()

    def get_coords_from_geocoder(self, toponym_to_find, address=False, index=False):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
            "geocode": toponym_to_find,
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)

        if not response:
            # обработка ошибочной ситуации
            pass

        # Преобразуем ответ в json-объект
        json_response = response.json()
        # Получаем первый топоним из ответа геокодера.
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        # Координаты центра топонима:
        toponym_coodrinates = toponym["Point"]["pos"]
        if address:
            if index:
                return (toponym['metaDataProperty']['GeocoderMetaData']['Address']['formatted'] + ', ' +
                        toponym['metaDataProperty']['GeocoderMetaData']['Address']["postal_code"])
            return toponym['metaDataProperty']['GeocoderMetaData']['Address']['formatted']

        # Долгота и широта:
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        self_point = f'{toponym_longitude},{toponym_lattitude}'
        return self_point


    def change_theme(self):
        self.theme = 'light' if self.theme != 'light' else 'dark'
        self.refresh_map()

    def refresh_map(self):
        map_params = {
            "ll": ','.join(map(str, self.map_ll)),
            "l": self.map_l,
            'z': self.map_zoom,
            'pt': self.point,
            'theme': self.theme,
            'apikey': '92bf06ed-e9bb-4a7b-8b91-23cf32fb910d',

        }



        response = requests.get('https://static-maps.yandex.ru/v1', params=map_params)
        print(response.url)
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


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


app = QApplication(sys.argv)
main_window = MainWindow()
sys.excepthook = except_hook
main_window.show()
sys.exit(app.exec())
