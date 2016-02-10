#! /usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
from gui.window import FWindow

class NavalView:
    def __init__(self, model=None):
        self.model = model
        self.create_gui()

    def create_gui(self):
        self.app = QtGui.QApplication(sys.argv)
        self.window = FWindow()
        self.window.window_set(title = 'Naval Battle')

        self.vbox = QtGui.QVBoxLayout()
        self.board_hbox = QtGui.QHBoxLayout()
        self.control_hbox = QtGui.QHBoxLayout()
        self.c_grid = QtGui.QGridLayout()
        self.h_grid = QtGui.QGridLayout()
        
        self.c_grid.setMargin(10)
        self.h_grid.setMargin(10)
        self.create_board(self.c_grid)
        self.create_board(self.h_grid)
        self.board_hbox.addLayout(self.h_grid)
        self.board_hbox.addLayout(self.c_grid)

        self.ng_button = QtGui.QPushButton('&New game')
        self.control_hbox.addWidget(self.ng_button)
        
        self.vbox.addLayout(self.board_hbox)
        self.vbox.addLayout(self.control_hbox)
       
        self.window.setLayout(self.vbox)

        self.window.show()

        sys.exit(self.app.exec_())

    def create_board(self, grid):
        for n in range(10):
            for m in range(10):
                button = QtGui.QPushButton('')
                size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
                size_policy.setHorizontalStretch(0)
                size_policy.setVerticalStretch(0)
                button.setSizePolicy(size_policy)
                button.resize(5, 5)
                # button.setText('%d x %d'%(m, n))
                grid.addWidget(button, m, n)
                self.window.connect(button, QtCore.SIGNAL("clicked()"), lambda row = m, col = n: print(row, col))

def test(argv=sys.argv):
    view = NavalView()

if __name__ == "__main__":
    sys.exit(test())

