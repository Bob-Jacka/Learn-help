"""
Graphical user interface in utility
"""
from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QInputDialog, QLabel, QDialog


class UI(QtWidgets.QWidget):
    """
    Pyqt based ui
    """

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        uic.loadUi("MainWindow.ui", self)

    def take_question(self, question: str):
        self.Question_field.setText(question)

    def setup_slots(self):
        self.Pass_question.clicked.connect(QtWidgets.QApplication.instance().quit)
        self.No_answer.clicked.connect(QtWidgets.QApplication.instance().quit)
        self.Save_question.clicked.connect(QtWidgets.QApplication.instance().quit)


class Choose_suit_dialog(QDialog):  # 1. Наследуем от QDialog
    def __init__(self, options, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modal choose")
        self.options = options
        self.result = ""

        layout = QVBoxLayout()
        self.label = QLabel("Push button to choose suit")
        btn = QPushButton("Choose variant")

        btn.clicked.connect(self.on_button_click)

        layout.addWidget(self.label)
        layout.addWidget(btn)
        self.setLayout(layout)
        self.setModal(True)

    def on_button_click(self):
        item, ok = QInputDialog.getItem(
            self,
            "Choose suit to run",
            "Suit:",
            self.options,
            current=0,
            editable=False
        )
        if ok and item:
            self.result = item
            self.accept()
        else:
            self.reject()
