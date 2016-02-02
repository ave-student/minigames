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
    def __init__(self, content = 'empty'):
        self.__state = 'closed'
        self.__content = content

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
        return 'Cell(state = %s, content = %s)'%(self.__state, self.__content)

class Ship:
    """
    Класс представляет абстракцию корабля.
    """
    def __init__(self, cells):
        self.cells = cells
        self.mark_cells('ship')

    def mark_cells(self, mark):
        for cell in self.cells:
            cell.set_content(mark)

    def get_count(self):
        return len(cells)

    def is_bang(self):
        """
        True, если корабль ранен.
        """
        for cell in self.cells:
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

    def get_cell(self, x, y, board):
        if 0 <= x <= self.board_size and 0 <= y <= self.board_size:
            return self.__board[board][x][y]

    def create_board(self):
        rows = []
        for row in range(self.board_size):
            cells = []
            for cell in range(self.board_size):
                cells.append(Cell())
            rows.append(cells)
        return rows

    def create_ships(self, board):
        # self.ships[board]
        pass

    def place_ship(self, x, y, direction, count, board):
        if not 0 <= x <= (self.board_size - 1) or not 0 <= y <= (self.board_size - 1):
            raise Exception('Not in range!')
        cells = []
        if direction == 'horizontal':
            x = self.shift_ship(x, count)
            for i in range(count):
                cells.append(self.get_cell(x + i, y, board))
        if direction == 'vertical':
            y = self.shift_ship(y, count)
            for i in range(count):
                cells.append(self.get_cell(x, y + i, board))

    def shift_ship(self, coord, count):
        if coord + count > self.board_size:
            return self.board_size - coord
        return coord

    def get_cell_neighbours(self, row, column, board):
        cells = set()
        for x in [row - 1, row, row + 1]:
            for y in [column -1, column, column + 1]:
                cells.add(self.get_cell(x, y, board))
        return cells.difference(set((self.get_cell(row, column, board), )))

def main(argv=sys.argv):
    model = NavalModel()
    for cell in (model.get_cell_neighbours(3, 3, 0)):
        print(cell)

if __name__ == "__main__":
    sys.exit(main())

