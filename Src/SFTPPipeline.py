# ***********************************************************************************************************************
# *                                                                                                                     *
# *   SFTPPipeline.py                                                                                                   *
# *   Authors: Robert B. Wilson, Alex Baker, Jordan Phillips, Gabriel Snider, Steven Dorsey, Yoshinori Agari            *
# *   The purpose of this file is to serve as the entry point of the SFTPPipeline application                           *
# *                                                                                                                     *
# ***********************************************************************************************************************

import PyQt5
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import sys

from views.MainWindow import MainWindow



# check for command line arguments
if len(sys.argv) > 1:
    print("Command line arguments!!!")
    pass
else:
    # display MainWindow
    app = QApplication(sys.argv)
    UI = MainWindow()
    app.exec_()