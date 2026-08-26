"""
Graphical user interface in utility
"""
from PyQt6 import QtWidgets
from PyQt6.QtCore import QSize, QRect, QCoreApplication, QMetaObject
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QInputDialog, QLabel, QDialog, QHBoxLayout, QTextEdit


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Learn help")
        Form.resize(800, 700)
        Form.title(u'Learn help')
        Form.setMinimumSize(QSize(800, 700))
        Form.setMaximumSize(QSize(800, 700))
        self.horizontalLayoutWidget = QWidget(Form)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 570, 801, 131))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.No_answer = QPushButton(self.horizontalLayoutWidget)
        self.No_answer.setObjectName(u"No_answer")

        self.horizontalLayout_2.addWidget(self.No_answer)

        self.Pass_question = QPushButton(self.horizontalLayoutWidget)
        self.Pass_question.setObjectName(u"Pass_question")

        self.horizontalLayout_2.addWidget(self.Pass_question)

        self.Save_question = QPushButton(self.horizontalLayoutWidget)
        self.Save_question.setObjectName(u"Save_question")

        self.horizontalLayout_2.addWidget(self.Save_question)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)

        self.Question_field = QTextEdit(Form)
        self.Question_field.setObjectName(u"Question_field")
        self.Question_field.setGeometry(QRect(0, 10, 791, 551))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.No_answer.setText(QCoreApplication.translate("Form", u"No answer", None))
        self.Pass_question.setText(QCoreApplication.translate("Form", u"Pass question", None))
        self.Save_question.setText(QCoreApplication.translate("Form", u"Save question", None))

    def setup_slots(self):
        self.Pass_question.clicked.connect(QtWidgets.QApplication.instance().quit)
        self.No_answer.clicked.connect(QtWidgets.QApplication.instance().quit)
        self.Save_question.clicked.connect(QtWidgets.QApplication.instance().quit)


class Choose_suit_dialog(QDialog):
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
