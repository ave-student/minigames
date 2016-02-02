#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Naval Clash - игра "морской бой".
"""

import sys

class Cell:
    """
    Класс ячейки игрового поля.
    Имеет 2 состояния: 'closed' (по умолчанию), 'opened'.
    """
    def __init__(self, x, y, content = 'empty'):
        self.__x = x
        self.__y = y
        self.__state = 'closed'
        self.__content = content

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_coords(self):
        return (self.__x, self.__y)

    def open(self):
        """
        Открыть ячейку.
        """
        self.__state = 'opened'
        return self.__content

    def set_content(self, content):
        self.__content = content

    def is_opened(self):
        """
        True, если ячейка отрыта.
        """
        return self.__state == 'opened'

    def is_empty(self):
        """
        True, если ячейка пустая.
        """
        return self.__content == 'empty'

    def is_bang(self):
        """
        True, если корабль ранен.
        """
        return self.__content == 'bang'

    def is_ship(self):
        """
        True, если в ячейке расположена палуба коробля.
        """
        return self.__content == 'ship'

    def is_sunk(self):
        """
        True, если корабль утоплен.
        """
        return self.__content == 'sunk'

    def __str__(self):
        return 'Cell(%d, %d){state = %s, content = %s}'%(self.__x, self.__y, self.__state, self.__content)

class Ship:
    """
    Класс представляет абстракцию корабля.
    """
    def __init__(self, cells):
        self.__cells = cells
        self.mark_cells('ship')

    def get_cells(self):
        return self.__cells

    def mark_cells(self, mark):
        for cell in self.__cells:
            cell.set_content(mark)

    def get_count(self):
        return len(self.__cells)

    def is_bang(self):
        """
        True, если корабль ранен.
        """
        for cell in self.__cells:
            if cell.is_bang():
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
            if cell.is_sunk():
                return True
        self.mark_cells('sunk')
        return True

    def __str__(self):
        return 'Ship(%d)' % self.get_count()

class Board:
    """
    Класс реализует абстракцию игрового поля.
    """
    def __init__(self, size):
        self.__size = size
        self.__cells = []
        self.__ships = []

    def create(self):
        rows = []
        for row in range(self.__size):
            cols = []
            for col in range(self.__size):
                cols.append(Cell(row, col))
            self.__cells.append(cols)

    def get_cell(self, x, y):
        return self.__cells[x][y]

    def get_cell_neighbours(self, x, y):
        cells = set()
        for row in [x - 1, x, x + 1]:
            for column in [y -1, y, y + 1]:
                cells.add(self.get_cell(row, column))
        return cells.difference(set((self.get_cell(x, y), )))

    def get_ship_neighbours(self, ship):
        neighbours = set()
        for cell in ship.get_cells():
            neighbours.add(self.get_cell_neighbours(cell.get_x(), cell.get_y()))
        return neighbours.difference(set(ship.get_cells()))

    def place_ship(self, x, y, direction, count):
        if not 0 <= x <= (self.__size - 1) or not 0 <= y <= (self.__size - 1):
            raise Exception('Not in range!')
        if self.get_cell(x, y).is_ship():
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
            if cell.is_ship():
                raise Exception('There is already a ship!!')
            for item in self.get_cell_neighbours(cell.get_x(), cell.get_y()):
                if item.is_ship():
                    raise Exception('There is already a ship!!!')
        self.__ships.append(Ship(cells))


    def shift_ship(self, coord, count):
        if coord + count > self.__size:
            return self.__size - coord
        return coord

class NavalModel:
    """
    Класс реализующий модель.
    """
    def __init__(self):
        self.ships = []
        self.new_game()

    def new_game(self):
        self.board_size = 10
        self.human_step = False
        self.game_started = False
        self.__board = [self.create_board(), self.create_board()]

    def create_boards(self):
        pass

def main(argv=sys.argv):
    board = Board(10)
    board.create()
    for cell in (board.get_cell_neighbours(3, 3)):
        print(cell)
    board.place_ship(3, 3, 'horizontal', 4)

if __name__ == "__main__":
    sys.exit(main())

