from PyQt5.QtWidgets import QMessageBox

def show_error(err_msg, title='Error'):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(err_msg)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.exec_()