#! /usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys
import random
from objects.board import Board

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
        self.h_board.set_visible(True)
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
        ships_list = self.get_ships_list()
        for count in ships_list:
            while True:
                try:
                    board.add_ship(random.randint(0, self.__board_size - 1),
                            random.randint(0, self.__board_size -1),
                            random.choice(['horizontal', 'vertical']),
                            count)
                except Exception:
                    continue
                break
        self.mark_ships(board)

    def c_fire(self):
        """
        Простейшая реализация компьютерной логики -
        это ее отсутствие :)
        """
        success = True
        while success:
            x = random.randint(0, self.__baord_size - 1)
            y = random.randint(0, self.__board_size - 1)
            try:
                success = fire(x, y, self.h_board)
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

def test(argv=sys.argv):
    mod = NavalModel()
    mod.new_game(10, 4)
    print(mod.c_board)
    print(mod.h_board)

if __name__ == "__main__":
    sys.exit(test())

