from PyQt5.QtWidgets import QApplication, QLabel


def main():
    app = QApplication([])
    label = QLabel('Hello World!')
    label.show()
    app.exec_()
