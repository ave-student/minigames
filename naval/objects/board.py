#! /usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys

if __name__ == '__main__':
    from cell import Cell
    from ship import Ship
else:
    from . cell import Cell
    from . ship import Ship

class Board:
    """
    Класс реализует абстракцию игрового поля.
    """
    def __init__(self, size):
        self.__size = size
        self.__cells = []
        self.__ships = []
        self.__visible = False
        self.create()

    def create(self):
        """
        Метод создания объекта Board.
        """
        rows = []
        for row in range(self.__size):
            cols = []
            for col in range(self.__size):
                cols.append(Cell(col, row))
            self.__cells.append(cols)

    def set_visible(self, vis):
        """
        Метод служит для задания атрибута видимости содержимого ячеек
        данного поля.
        """
        self.__visible = vis

    def get_visible(self):
        """
        Получить значение атрибута видимости.
        """
        return self.__visible

    def get_ships(self):
        """
        Получить список кораблей размещенных на поле.
        """
        return self.__ships

    def get_cell(self, x, y):
        """
        Возвращает ячейку с координатами x, y.
        """
        return self.__cells[y][x]

    def get_cell_neighbours(self, x, y):
        """
        Возвращает список ячеек соседних ячейке заданной координатами.
        """
        cells = set()
        for row in [x - 1, x, x + 1]:
            if not 0 <= row < self.__size:
                continue
            for column in [y -1, y, y + 1]:
                if not 0 <= column < self.__size:
                    continue
                cells.add(self.get_cell(row, column))
        return cells.difference(set((self.get_cell(x, y), )))

    def get_ship_neighbours(self, ship):
        """
        Возвращает список ячеек соседних для данного корабля.
        """
        neighbours = set()
        for cell in ship.get_cells():
            neighbours.add(self.get_cell_neighbours(cell.get_x(), cell.get_y()))
        return neighbours.difference(set(ship.get_cells()))
    
    def mark_cells(self, cells, mark):
        """
        Пометить ячейку.
        """
        for cell in cells:
            cell.set_mark(mark)

    def add_ship(self, x, y, direction, count):
        """
        Метод добавления корабля.
        """
        if not 0 <= x <= (self.__size - 1) or not 0 <= y <= (self.__size - 1):
            raise Exception('Not in range!')
        if self.get_cell(x, y).get_mark() == 'ship':
            raise Exception('There is already a ship!')
        cells = []
        if direction == 'horizontal':
            x = self.shift_ship(x, count)
            for i in range(count):
                cells.append(self.get_cell(x + i, y))
        if direction == 'vertical':
            y = self.shift_ship(y, count)
            for i in range(count):
                cells.append(self.get_cell(x, y + i))
        for cell in cells:
            if cell.get_mark() == 'ship':
                raise Exception('There is already a ship!!')
            for item in self.get_cell_neighbours(cell.get_x(), cell.get_y()):
                if item.get_mark() == 'ship':
                    raise Exception('There is already a ship!!!')
        self.__ships.append(Ship(cells))
        self.mark_cells(cells, 'ship')

    def shift_ship(self, coord, count):
        if coord + count > self.__size:
            return self.__size - coord
        return coord

    def cell_in_ship(self, x, y):
        """
        Возвращает объект корабля, которому принадлежит ячейка с заданными координатами.
        """
        for ship in self.__ships:
            for cell in ship.get_cells():
                if cell.get_x() == x and cell.get_y() == y:
                    return ship
        return None

    def clear(self):
        """
        Очистка игрового поля.
        """
        for cell in self.__cells:
            cell.init_state()

    def __str__(self):
        rows = ''
        for i in range(self.__size):
            column = ''
            for j in range(self.__size):
                if not self.__visible and not self.__cells[i][j].is_opened():
                    column += '` '
                    continue
                if self.__cells[i][j].get_mark() == 'empty':
                    if self.__cells[i][j].is_opened():
                        column += '~ '
                    else:
                        column += '` '
                    continue
                if self.__cells[i][j].get_mark() == 'ship':
                    column += 'o '
                    continue
                if self.__cells[i][j].get_mark() == 'bang':
                    column += '* '
                    continue
                if self.__cells[i][j].get_mark() == 'sunk':
                    column += 'x '
                    continue
                column += '? '
            rows += column + '\n'
        return rows

def test(argv=sys.argv):
    bd = Board(10)
    bd.create()
    bd.add_ship(3, 3, 'horizontal', 4)
    bd.add_ship(3, 5, 'vertical', 2)
    bd.add_ship(1, 1, 'horizontal', 1)
    print(bd)
    bd.set_visible(True)
    print(bd)
 
if __name__ == '__main__':
    sys.exit(test())
