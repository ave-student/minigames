#! /usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui

class NavalView(QtGui.QWidget):
    def __init__(self, model=None, parent=None):
        self.model = model
        QtGui.QWidget.__init__(self, parent)
        self.ng_button = QtGui.QPushButton('&New game')
        self.hbox = QtGui.QHBoxLayout()
        self.create_board()
        self.vbox = QtGui.QVBoxLayout()
        self.hbox.addWidget(self.ng_button)
        self.vbox.addLayout(self.grid)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

    def create_board(self):
        self.grid = QtGui.QGridLayout()
        for n in range(10):
            for m in range(10):
                button = QtGui.QPushButton('')
                button.setText('%d x %d'%(m, n))
                self.grid.addWidget(button, m, n)
                self.connect(button, QtCore.SIGNAL("clicked()"), lambda row = m, col = n: print(row, col))

def test(argv=sys.argv):
    app = QtGui.QApplication(sys.argv)
    window = NavalView()
    window.setWindowTitle("Naval Battle")
    window.resize(300, 70)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    sys.exit(test())

