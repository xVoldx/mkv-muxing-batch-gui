# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from PySide2.QtGui import QFont, QFontDatabase
from PySide2.QtWidgets import QApplication
from packages.Startup import GlobalFiles
from packages.Startup.MainApplication import MainApplication
import ctypes

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
# noinspection PyAttributeOutsideInit
from packages.MainWindow import MainWindow
from packages.Widgets.WarningDialog import WarningDialog

window: MainWindow
app: QApplication


def setup_application_font():
    try:
        id = QFontDatabase.addApplicationFont(GlobalFiles.MyFontPath)
        _fontstr = QFontDatabase.applicationFontFamilies(id)[0]
        _font = QFont(_fontstr, 10)
        app.setFont(_font)
    except Exception as e:
        warning_dialog = WarningDialog(window_title="Missing Fonts", info_message="Can't find 'OpenSans' font at "
                                                                                  "../Resources/Fonts/OpenSans.ttf\n" +
                                                                                  "application will use default font")
        warning_dialog.execute()


def create_application():
    global app
    app = MainApplication
    app.setWindowIcon(GlobalFiles.AppIcon)


def create_window():
    global window
    window = MainWindow(sys.argv)


def run_application():
    sys.exit(app.exec_())


def logger_exception(exception_type, exception_value, exception_trace_back):
    with open(GlobalFiles.AppLogFilePath, 'a+', encoding="UTF-8") as log_file:
        log_file.write(str(datetime.utcnow()) + ' ' + str(exception_type) + "\n" + str(exception_value) + "\n" + str(
            exception_trace_back) + '\n')


def setup_logger():
    sys.excepthook = logger_exception


if __name__ == "__main__":
    setup_logger()
    create_application()
    setup_application_font()
    create_window()
    run_application()
