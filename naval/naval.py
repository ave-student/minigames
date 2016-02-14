#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
Naval Clash - игра "морской бой".
"""

import sys
import random

class NavalGame:
    def __init__(self, model):
        self.model = model
    
    def start_game(self):
        self.model.new_game(10, 4)

def main(argv=sys.argv):
    model = NavalModel()
    game = NavalGame(model)
    game.start_game()
    print('computer')
    print(model.c_board)
    print('human')
    print(model.h_board)

if __name__ == "__main__":
    sys.exit(main())
