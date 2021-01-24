from PyQt5.QtWidgets import QMessageBox

def show_error(text, title='Error'):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setDefaultButton(QMessageBox.Ok)
    msg.exec_()

def confirm_action(text, title='Confirm'):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
    msg.setDefaultButton(QMessageBox.Cancel)

    return msg.exec_() == QMessageBox.Yes
