import QtQuick 2.15
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.15
import Qt.labs.platform 1.1 as Lab
import QtQuick.Dialogs 1.2

ApplicationWindow {
  title: "Furry waffle"
  visible: true
  width: 800
  height: 600
  minimumWidth: 800
  minimumHeight: 600

  Lab.FileDialog {
    id: openFileDialog
    title: "Torrent file"
    nameFilters: ["Torrent files (*.torrent)"]

    onAccepted: {
      app_menu.on_file_open(openFileDialog.file)
    }
  }

  Dialog {
    width: 500
    height: 200
    objectName: "torrentDetailsDialog"
    title: "Torrent details"
    modality: Qt.NonModal
    standardButtons: StandardButton.Open | StandardButton.Cancel

    onAccepted: {
      torrent_details_dialog.on_accept()
    }

    Lab.FileDialog {
      id: changeFileDialog
      title: "Torrent file"
      nameFilters: ["Torrent files (*.torrent)"]

      onAccepted: {
        torrent_details_dialog.on_change_file(changeFileDialog.file)
      }
    }

    FileDialog {
      id: changeDownloadDirDialog
      title: "Download directory"
      selectFolder: true

      onAccepted: {
        torrent_details_dialog.on_change_download_dir(changeDownloadDirDialog.folder)
      }
    }

    ColumnLayout {
      width: parent.width
      spacing: 10

      Label {
        text: "Torrent file"
      }

      RowLayout {
        width: parent.width

        TextField {
          objectName: "torrentFilePath"
          text: "hello"
          readOnly: true
          selectByMouse: true
          Layout.fillWidth: true
        }

        Button {
          text: "Change"
          onClicked: {
            changeFileDialog.open()
          }
        }  
      }

      Label {
        text: "Download directory"
      }

      RowLayout {
        width: parent.width

        TextField {
          objectName: "downloadDir"
          text: "filepath"
          readOnly: true
          selectByMouse: true
          Layout.fillWidth: true
        }

        Button {
          text: "Change"
          onClicked: {
            changeDownloadDirDialog.open()
          }
        }  
      }
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
            text: stats_formatted
            color: stats_color
          }

          Text {
            text: progress_formatted
          }
        }

        Rectangle {
          Layout.fillWidth: true
        }

        Button {
          text: control_btn_text
          visible: control_btn_visible
          onClicked: {
            torrents_list_model.on_control_btn_click(id)
          }
        }  
      }

      Controls1.ProgressBar {
        value: progress_percent

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
            color: progress_bar_color
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
            onTriggered: torrents_list_model.on_remove(id)
          }

          Action {
            text: "&Remove and clean data"
            onTriggered: torrents_list_model.on_remove_with_data(id)
          }
        }
      }
    }
  }

  ListView {
    id: listView
    anchors.fill: parent
    clip: true
    model: torrents_list_model
    delegate: torrentItem
    spacing: 10
  }
}
