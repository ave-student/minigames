#! /usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys

class Cell:
    """
    Класс ячейки игрового поля.
    Имеет 2 состояния: 'closed' (по умолчанию), 'opened'.
    """
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.init_state()

    def init_state(self):
        """
        Привести ячейку к исходному состоянию:
            - ячейка закрыта;
            - ячейка пустая.
        """
        self.__state = 'closed'
        self.__mark = 'empty'

    def get_x(self):
        """
        Возвращает координату x ячейки.
        """
        return self.__x

    def get_y(self):
        """
        Возвращает координату y ячейки.
        """
        return self.__y

    def open(self):
        """
        Открыть ячейку.
        """
        self.__state = 'opened'
        return self.__mark

    def get_mark(self):
        """
        Вернуть значение метки ячейки.
        """
        return self.__mark

    def set_mark(self, mark):
        """
        Пометить ячейку.
        """
        self.__mark = mark 

    def is_opened(self):
        """
        True, если ячейка отрыта.
        """
        return self.__state == 'opened'

    def __str__(self):
        return 'Cell(%d, %d){state = %s, mark = %s}'%(self.__x, self.__y, self.__state, self.__mark)

def test(argv=sys.argv):
    cells = [Cell(3, 2), Cell(1, 1,), Cell(1, 2,)]
    cells[1].set_mark('ship')
    for cell in cells:
        print(cell)
        if cell.get_mark() == 'ship':
            cell.open()
            cell.set_mark('bang')
        print(cell)
        cell.init_state()
        print(cell)
        print()

if __name__ == "__main__":
    sys.exit(test())

