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
        text: "&Default download directory"
        onTriggered: {
          app_menu.on_default_download_dir()
        }
      }

      Action {
        text: "&Pause all"
        onTriggered: {
          app_menu.on_pause_all()
        }
      }

      Action {
        text: "&Resume all"
        onTriggered: {
          app_menu.on_resume_all()
        }
      }

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
    width: 180
    height: 100

    objectName: "peerLimitDialog"
    title: "Peer limit"
    standardButtons: StandardButton.Close | StandardButton.Save

    onAccepted: {
      peer_limit_dialog.on_save()
    }

    Rectangle {
      width: parent.width
      height: 25
      border.width: 1
      border.color: '#ededed'

      TextInput {
        id: peerLimitInput
        objectName: "peerLimitInput"

        width: parent.width
        text: "1234"
        inputMethodHints: Qt.ImhDigitsOnly
        validator: IntValidator {bottom: 1; top: 1000000}
        font.pixelSize: 15

        onTextChanged: {
          peer_limit_dialog.on_input_change(peerLimitInput.text)
        }
      }
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
        width: logsListView.width
        clip: true

        Rectangle {
          height: 1
          Layout.fillWidth: true
          color: "#ededed"
        }

        ColumnLayout {
          Text {
            text: title
            font.bold: true
            font.pixelSize: 16
          }

          Text {
            text: description
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
          objectName: "logSearchField"
          selectByMouse: true
          placeholderText: 'Search...'

          onTextChanged: {
            const text = logSearchField.text;
            clearFilteredLogsBtn.enabled = !!text
            logs_list_model.on_search_change(text);
          }
        }

        Rectangle {
          Layout.fillWidth: true
        }

        Button {
          id: clearFilteredLogsBtn
          text: "Clear filtered"
          enabled: false
          onClicked: {
            logs_list_model.on_clear_filtered(logSearchField.text)
          }
        }

        Button {
          text: "Clear all"
          onClicked: {
            logs_list_model.on_clear_all()
          }
        }
      }

      ListView {
        id: logsListView
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
    height: 120
    objectName: "defaultDownloadDirDialog"
    title: "Default download directory"
    standardButtons: StandardButton.Save | StandardButton.Cancel

    onAccepted: {
      default_download_dir_dialog.on_accept()
    }

    FileDialog {
      id: changeDefaultDownloadDirDialog
      title: "Download directory"
      selectFolder: true

      onAccepted: {
        default_download_dir_dialog.on_change_dir(changeDefaultDownloadDirDialog.folder)
      }
    }

    RowLayout {
      width: parent.width

      TextField {
        id: defaultDownloadDir
        objectName: "defaultDownloadDir"
        text: "filepath"
        readOnly: true
        selectByMouse: true
        Layout.fillWidth: true
      }

      Button {
        text: "Change"
        onClicked: {
          changeDefaultDownloadDirDialog.open()
        }
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

    Rectangle {
      width: torrentsListView.width
      height: 100

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
            text: "Peer limit"
            onTriggered: torrents_list_model.on_peer_limit(id)
          }

          Action {
            text: "Remove"
            onTriggered: torrents_list_model.on_remove(id)
          }

          Action {
            text: "Remove and clean data"
            onTriggered: torrents_list_model.on_remove_with_data(id)
          }
        }
      }

      ColumnLayout {
        width: parent.width

        Rectangle {
          height: 1
          Layout.fillWidth: true
          color: "#ededed"
        }

        RowLayout {
          Layout.fillWidth: true

          // TODO: fix this hack
          Rectangle {
            width: 3
          }

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

          // TODO: fix this hack
          Rectangle {
            width: 20
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
      id: torrentsListView
      Layout.fillWidth: true
      Layout.fillHeight: true
      clip: true
      model: torrents_list_model
      delegate: torrentItem
      spacing: 10
    }

    Rectangle {
      height: 1
      Layout.fillWidth: true
      color: "#ededed"
    }

    Text {
      objectName: "footerText"
      horizontalAlignment: Text.AlignRight
      rightPadding: 10
      bottomPadding: 5
      Layout.fillWidth: true
      text: "Uploaded: 55Gb     Downloaded: 33Gb"
    }
  }
}
