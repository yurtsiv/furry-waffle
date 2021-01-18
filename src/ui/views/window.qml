import QtQuick 2.15
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.15
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
      appMenu.onFileOpen(openFileDialog.file)
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

  Component {
    id: torrentItem

    ColumnLayout {
      width: parent.width

      RowLayout {
        width: parent.width

        ColumnLayout {
          Text {
            text: name
            font.bold: true
            font.pixelSize: 16
          }

          Text {
            text: statsFormatted
          }

          Text {
            text: progressFormatted
          }
        }

        Rectangle {
          Layout.fillWidth: true
        }

        Button {
          text: controlBtnText
          visible: controlBtnVisible
          onClicked: {
            torrentsListModel.on_control_btn_click(id)
          }
        }  
      }

      Controls1.ProgressBar {
        value: progressPercent

        maximumValue: 100
        implicitWidth: parent.width
        implicitHeight: 20

        style: ProgressBarStyle {
          background: Rectangle {
            radius: 2
            color: "lightgray"
            border.color: "gray"
            border.width: 1
            implicitWidth: parent.width
            implicitHeight: parent.height
          }

          progress: Rectangle {
              color: "lightsteelblue"
              border.color: "steelblue"
          }
        }
      }

      MouseArea {
        anchors.fill: parent

        acceptedButtons: Qt.RightButton
        onClicked: {
            if (mouse.button === Qt.RightButton)
                contextMenu.popup()
        }
  
        Menu {
          id: contextMenu

          Action {
            text: "&Remove"
            onTriggered: torrentsListModel.on_remove(id)
          }

          Action {
            text: "&Remove and clean data"
            onTriggered: torrentsListModel.on_remove_with_data(id)
          }
        }
      }
    }
  }

  ListView {
    id: listView
    anchors.fill: parent
    clip: true
    model: torrentsListModel
    delegate: torrentItem
    spacing: 10
  }
}
