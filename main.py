import os, sys, urllib.request, json
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickView
from PySide6.QtCore import QStringListModel, Qt, QUrl
from PySide6.QtGui import QGuiApplication

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()

    #Load the QML file
    qml_file = os.path.join(os.path.dirname(__file__),"view.qml")
    engine.load(QUrl.fromLocalFile(os.path.abspath(qml_file)))

    #Show the window
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())

# c = Client(host='localhost', port=9091, username='transmission', password='password')
# with open("/home/stepy/Downloads/elizer_yudkovski._garri_potter_i_metody_ratsionalnosti.pdf_148.torrent", "rb") as f:
#   c.add_torrent(f)