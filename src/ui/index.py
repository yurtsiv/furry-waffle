import os
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine

from ui.ContextManager import ContextManager

def run(torrent_client):
    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()

    context = engine.rootContext()

    ctx_manager = ContextManager(torrent_client)

    context.setContextProperty("app_menu", ctx_manager.app_menu)
    context.setContextProperty("torrents_list_model", ctx_manager.torrents_list_model)
    context.setContextProperty("torrent_details_dialog", ctx_manager.torrent_details_dialog)
    context.setContextProperty("logs_list_model", ctx_manager.logs_list_model)

    qml_file = os.path.join(os.path.dirname(__file__), "views/window.qml")
    engine.load(QUrl.fromLocalFile(os.path.abspath(qml_file)))

    if not engine.rootObjects():
        sys.exit(-1)

    window = engine.rootObjects()[0]
    ctx_manager.set_window(window)

    app.exec_()

    ctx_manager.clean_up()
    sys.exit(0)
