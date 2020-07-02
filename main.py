# import the main window object (mw) from aqt
from aqt import mw
# import all of the Qt GUI library
from aqt.qt import *
from PyQt5 import QtCore
import logging

def launch_menu():
    pass

def setup_menus():
    launch_action = QAction("Chinese Prestudy", mw)
    launch_action.triggered.connect(launch_menu)
    mw.form.menuTools.addAction(launch_action)
