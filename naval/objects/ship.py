#! /usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys

class Ship:
    """
    Класс представляет абстракцию корабля.
    """
    def __init__(self, cells):
        self.__cells = cells

    def get_cells(self):
        """
        Возвращает список ячеек коробля.
        """
        return self.__cells

    def get_count(self):
        """
        Возвращает размер корабля.
        """
        return len(self.__cells)

    def is_bang(self):
        """
        True, если корабль ранен.
        """
        for cell in self.__cells:
            if cell.get_mark() == 'bang':
                return True
        return False

    def is_sunk(self):
        """
        True, если корабль потоплен.
        Если все палубы корабля открыты и ни одна
        не помечена как потопленная (т.е. все ячейки помечены
        как 'bang'), то пометить палубы как потопленные.
        """
        for cell in self.cells:
            if not cell.is_opened():
                return False
            if cell.get_mark() == 'sunk':
                return True
        # self.mark_cells('sunk')
        return True

    def __str__(self):
        string = 'Ship(%d): ' % self.get_count()
        for cell in self.__cells:
            string += str(cell) + ', '
        return string

def test(argv=sys.argv):
    cells = [Cell(3, 2), Cell(1, 1), Cell(1, 2)]
    ship = Ship(cells)
    for cell in cells:
        cell.set_mark('ship')
    print(ship)

if __name__ == "__main__":
    from cell import Cell

    sys.exit(test())
