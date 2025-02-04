from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import QGridLayout, QLabel, \
    QDialog, QPushButton, QHBoxLayout

from packages.Startup import GlobalFiles


class ConfirmCheckMakeThisSubtitleDefaultWithUnCheckOption(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.yesButton = QPushButton("OK")
        self.noButton = QPushButton("Cancel")
        self.thirdButton = QPushButton("Uncheck this one")
        self.setWindowTitle("Confirm Check")
        self.setWindowIcon(GlobalFiles.QuestionIcon)
        self.message = QLabel("<nobr>Are you sure?<br>This will <b>uncheck</b> set default and set forced options "
                              "from subtitle tab")
        self.messageIcon = QLabel()

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.thirdButton)
        self.buttons_layout.addWidget(self.yesButton)
        self.buttons_layout.addWidget(self.noButton)

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.messageIcon, 0, 0, 2, 1)
        self.main_layout.addWidget(QLabel(), 0, 1, 1, 1)  # add space
        self.main_layout.addWidget(self.message, 0, 2, 2, 3)
        self.main_layout.addLayout(self.buttons_layout, 2, 4, 1, 1)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.main_layout)

        self.result = "No"
        self.setup_ui()
        self.signal_connect()

    def setup_ui(self):
        self.disable_question_mark_window()
        self.set_message_icon_info()
        # self.increase_message_font_size(1)
        self.set_default_buttons()

    def signal_connect(self):
        self.yesButton.clicked.connect(self.click_yes)
        self.noButton.clicked.connect(self.click_no)
        self.thirdButton.clicked.connect(self.click_third_button)

    def click_yes(self):
        self.result = "Yes"
        self.close()

    def click_no(self):
        self.result = "No"
        self.close()

    def click_third_button(self):
        self.result = "Third"
        self.close()

    def disable_question_mark_window(self):
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, on=False)

    def increase_message_font_size(self, value):
        message_font = self.message.font()
        message_font.setPointSize(self.message.fontInfo().pointSize() + value)
        self.message.setFont(message_font)

    def set_message_icon_info(self):
        self.messageIcon.setPixmap(QtGui.QPixmap(GlobalFiles.InfoBigIconPath))

    def set_default_buttons(self):
        self.yesButton.setDefault(False)
        self.noButton.setDefault(True)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        super().showEvent(a0)
        self.setFixedSize(self.size())

    def execute(self):
        self.exec_()
