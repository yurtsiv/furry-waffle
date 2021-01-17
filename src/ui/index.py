import os
import sys

from PyQt5.QtCore import QStringListModel, QUrl
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QGuiApplication

from ui.AppMenu import AppMenu
from ui.TorrentsListModel import TorrentsListModel

def run():
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()

    context = engine.rootContext()

    torrents_list_model = TorrentsListModel()
    app_menu = AppMenu(torrents_list_model)

    context.setContextProperty("torrentsListModel", torrents_list_model)
    context.setContextProperty("appMenu", app_menu)

    qml_file = os.path.join(os.path.dirname(__file__), "views/window.qml")
    engine.load(QUrl.fromLocalFile(os.path.abspath(qml_file)))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
