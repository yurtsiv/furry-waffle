import os
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine

from ui.ContextManager import ContextManager

def run(torrent_client):
    """
    Start the UI
    """
    app = QApplication(sys.argv)

    app.setOrganizationName("example")
    app.setOrganizationDomain("example.com")

    engine = QQmlApplicationEngine()

    context = engine.rootContext()

    ctx_manager = ContextManager(torrent_client)

    ctx_props = ctx_manager.context_props
    for prop_name in ctx_props:
        context.setContextProperty(prop_name, ctx_props[prop_name])

    qml_file = os.path.join(os.path.dirname(__file__), "views/window.qml")
    engine.load(QUrl.fromLocalFile(os.path.abspath(qml_file)))

    if not engine.rootObjects():
        sys.exit(-1)

    window = engine.rootObjects()[0]
    ctx_manager.set_window(window)

    ret = app.exec_()

    ctx_manager.clean_up()
    sys.exit(ret)
