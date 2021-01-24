import QtQuick 2.15
import QtQuick.Controls 2.12
import QtQuick.Controls 1.4 as Controls1
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.15
import Qt.labs.platform 1.1 as Lab
import QtQuick.Dialogs 1.2

ApplicationWindow {
  id: appWindow
  title: "Furry waffle"
  visible: true
  width: 800
  height: 600
  minimumWidth: 800
  minimumHeight: 600
  menuBar: MenuBar {
    Menu {
      title: "&File"

      Action {
        text: "&Open"
        onTriggered: openFileDialog.open()
      }

      Action {
        text: "&Exit"
        onTriggered: {
          Qt.quit()
        }
      }
    }

    Menu {
      title: "&Edit"

      Action {
        text: "&Logs"
        onTriggered: {
          app_menu.on_logs_open()
        }
      }
    }
  }


  Lab.FileDialog {
    id: openFileDialog
    title: "Torrent file"
    nameFilters: ["Torrent files (*.torrent)"]

    onAccepted: {
      app_menu.on_file_open(openFileDialog.file)
    }
  }

  Dialog {
    id: logsDialog
    width: 600
    height: 600

    objectName: "logsDialog"
    title: "Logs"
    modality: Qt.NonModal
    standardButtons: StandardButton.Close
    Component {
      id: logItem

      ColumnLayout {
        width: parent.width
        clip: true

        Rectangle {
          height: 1
          Layout.fillWidth: true
          color: "#ededed"
        }

        ColumnLayout {
          Text {
            text: log_text
            font.bold: true
            font.pixelSize: 16
          }

          Text {
            text: torrent_name
          }

          Text {
            text: created_at
          }
        }
      }
    }

    ColumnLayout {
      anchors.fill: parent
      clip: true


      RowLayout {
        TextField {
          id: logSearchField
          selectByMouse: true
          placeholderText: 'Search...'

          onTextChanged: {
            logs_list_model.on_search_change(logSearchField.text)
          }
        }

        Rectangle {
          Layout.fillWidth: true
        }

        Button {
          text: "Clear all"
          onClicked: {
            logs_list_model.on_clear_all()
          }
        }
      }

      ListView {
        Layout.fillWidth: true
        Layout.fillHeight: true

        clip: true
        model: logs_list_model
        delegate: logItem
        spacing: 10
      }
    }
  }

  Dialog {
    width: 500
    height: 220
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

  Component {
    id: torrentItem

    ColumnLayout {
      width: parent.width

      Rectangle {
        height: 1
        Layout.fillWidth: true
        color: "#ededed"
      }

      RowLayout {
        Layout.fillWidth: true

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

  ColumnLayout {
    anchors.fill: parent
    clip: true

    Rectangle {
      height: 2
    }

    ComboBox {
      width: 200
      model: ["Filter...", "Downloading", "Seeding", "Paused"]
      onActivated: {
        torrents_list_model.on_filter(currentIndex)
      }
    }

    Rectangle {
      height: 2
    }

    ListView {
      Layout.fillWidth: true
      Layout.fillHeight: true
      clip: true
      model: torrents_list_model
      delegate: torrentItem
      spacing: 10
    }
  }
}
