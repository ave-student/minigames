#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Naval Clash - игра "морской бой".
"""

import sys
import random

class Cell:
    """
    Класс ячейки игрового поля.
    Имеет 2 состояния: 'closed' (по умолчанию), 'opened'.
    """
    def __init__(self, x, y, content):
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
        return self.__mark

    def get_mark(self):
        return self.__mark

    def set_mark(self, mark):
        self.__mark = mark 

    def is_opened(self):
        """
        True, если ячейка отрыта.
        """
        return self.__state == 'opened'

    def __str__(self):
        return 'Cell(%d, %d){state = %s, content = %s}'%(self.__x, self.__y, self.__state, self.__mark)

class Ship:
    """
    Класс представляет абстракцию корабля.
    """
    def __init__(self, cells):
        self.__cells = cells

    def get_cells(self):
        return self.__cells

    def get_count(self):
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
        return 'Ship(%d)' % self.get_count()

class Board:
    """
    Класс реализует абстракцию игрового поля.
    """
    def __init__(self, size):
        self.__size = size
        self.__cells = []
        self.__ships = []
        self.create()

    def create(self):
        rows = []
        for row in range(self.__size):
            cols = []
            for col in range(self.__size):
                cols.append(Cell(row, col, 'empty'))
            self.__cells.append(cols)

    def get_ships(self):
        return self.__ships

    def get_cell(self, x, y):
        return self.__cells[x][y]

    def get_cell_neighbours(self, x, y):
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
        neighbours = set()
        for cell in ship.get_cells():
            neighbours.add(self.get_cell_neighbours(cell.get_x(), cell.get_y()))
        return neighbours.difference(set(ship.get_cells()))
    
    def mark_cells(self, cells, mark):
        for cell in cells:
            cell.set_mark(mark)

    def add_ship(self, x, y, direction, count):
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
                if self.__cells[i][j].get_mark() == 'empty':
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

class NavalModel:
    """
    Класс реализующий модель.
    """
    def __init__(self):
        self.c_board, self.h_board = None, None

    def new_game(self, board_size, ship_size):
        """
        Метод инициализации новой сессии игры.
        """
        self.__board_size = board_size
        self.__max_size_ship = ship_size
        self.human_step = False
        self.game_started = False
        if self.c_board and self.h_board:
            self.c_board.clear()
            slef.h_board.clear()
        else:
            self.c_board = Board(self.__board_size)
            self.h_board = Board(self.__board_size)
        self.random_place_ships(self.c_board)
        self.random_place_ships(self.h_board)
        self.game_started = True
        self.human_step = True

    def get_ships_list(self):
        """
        Генерирует список доступных в игре кораблей.
        """
        ships_list = []
        for i in range(self.__max_size_ship):
            for j in range(i + 1):
                ships_list.append(self.__max_size_ship - i)
        return ships_list

    def random_place_ships(self, board):
        for count in self.get_ships_list():
            success = False
            while not success:
                try:
                    board.add_ship(random.randint(0, self.__board_size - 1),
                            random.randint(0, self.__board_size -1),
                            random.choice(['horizontal', 'vertical']),
                            count)
                except Exception: 
                    success = False
                    continue
                success = True
        self.mark_ships(board)

    def c_fire(self):
        """
        Простейшая реализация компьютерной логики -
        это ее отсутствие :)
        Random решает судьбу игрока.
        """
        success = True
        while success:
            x = random.randint(0, self.__baord_size - 1)
            y = random.randint(0, self.__board_size - 1)
            try:
                next_step = fire(x, y, self.h_board)
                success = next_step
            except Exception:
                success = True

    def fire(self, x, y, board):
        if not 0 <= x < self.__board_size or not 0 <= y < self.__board_size:
            raise Exception('Not in range.')
        cell = board.get_cell(x, y)
        if cell.is_opened():
            raise Exception('Cell is already opened!.')
        cell.open()
        ship = board.cell_in_ship(x, y)
        if ship:
            cell.set_mark('bang')
            if ship.is_sunk():
                board.mark_cells(ship.get_cells(), 'sunk')
            return True
        return False

    def mark_ships(self, board):
        for ship in board.get_ships():
            board.mark_cells(ship.get_cells(), 'ship')

class NavalGame:
    def __init__(self, model):
        self.model = model
    
    def start_game(self):
        self.model.new_game(10, 4)


def main(argv=sys.argv):
    model = NavalModel()
    model.new_game(10, 4)
    model.random_place_ships(model.c_board)
    print(model.c_board)

if __name__ == "__main__":
    sys.exit(main())
