#! /usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore

class FWindow(QtGui.QWidget):
    def __init__(self, parent = None):
        super(FWindow, self).__init__()
    
    def window_set(self, title = 'programm by ave', icon = QtGui.QIcon()):
        self.setWindowTitle = title
        self.setWindowIcon = icon

def test(argv=sys.argv):
    pass

if __name__ == "__main__":
    sys.exit(test())

