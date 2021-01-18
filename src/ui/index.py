import os
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QGuiApplication

from ui.AppMenu import AppMenu
from ui.TorrentsListModel import TorrentsListModel

def run(torrent_client):
    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()

    context = engine.rootContext()

    torrents_list_model = TorrentsListModel(torrent_client)
    app_menu = AppMenu(torrents_list_model, torrent_client)

    context.setContextProperty("torrentsListModel", torrents_list_model)
    context.setContextProperty("appMenu", app_menu)

    qml_file = os.path.join(os.path.dirname(__file__), "views/window.qml")
    engine.load(QUrl.fromLocalFile(os.path.abspath(qml_file)))

    if not engine.rootObjects():
        sys.exit(-1)
    app.exec_()

    torrents_list_model.clean_up()
    sys.exit(0)
