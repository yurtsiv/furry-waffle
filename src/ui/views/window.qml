import QtQuick 2.12
import QtQuick.Controls 2.12
import Qt.labs.platform 1.1 as Lab

ApplicationWindow {
  title: "Furry waffle"
  visible: true
  width: 800
  height: 600
  minimumWidth: 800
  minimumHeight: 600

  Lab.FileDialog {
    id: openFileDialog
    nameFilters: ["Torrent files (*.torrent)"]

    onAccepted: {
      appMenu.onFilesOpen(openFileDialog.files)
    }
  }

  menuBar: MenuBar {
    Menu {
      title: "&File"
  
      Action {
        text: "&Open"
        onTriggered: openFileDialog.open()
      }

      Action {
        text: "&Quit"
        onTriggered: {
          Qt.quit()
        }
      }
    }
  }

  ListView {
    id: listView
    anchors.fill: parent
    clip: true
    model: torrentsListModel
    delegate: Text {
      text: name
    }
  }
}
