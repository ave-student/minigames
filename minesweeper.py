#! /usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
Сапер (Minesweeper) - логическая игра.
Приложение построено на базе паттерна MVC.
"""

import sys
from tkinter import *
import tkinter.messagebox
import random

MIN_ROW_COUNT = 5
MAX_ROW_COUNT = 30

MIN_COLUMN_COUNT = 5
MAX_COLUMN_COUNT = 30

#MIN_MINE_COUNT = 1
#MAX_MINE_COUNT = 800

class MinesweeperCell:
    """
    Класс ячейки минного поля.
    Используется в модели MVC.
    """
    # Состояния игровой клетки:
    #   closed - закрыта
    #   opened - открыта
    #   flagged - помечена флажком
    #   questioned - помечена вопросительным знаком

    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.state = 'closed'
        self.mined = False
        self.counter = 0
        self.markSequence = ['closed', 'flagged', 'questioned']

    def nextMark(self):
        """
        Метод циклически изменяет состояние игровой клетки.
        """
        if self.state in self.markSequence:
            stateIndex = self.markSequence.index(self.state)
            self.state = self.markSequence[(stateIndex + 1) % len(self.markSequence)]

    def open(self):
        """
        Метод позволяет открыть ячейку, если она не помечена флажком
        (состояние 'flagged').
        """
        if self.state != 'flagged':
            self.state = 'opened'


class MinesweeperModel:
    """
    Класс модели игры.
    Определяет основную логику игры.
    """
    def __init__(self):
        self.startGame()

    def startGame(self, rowCount = 15, columnCount = 15, mineCount = 28):
        """
        Игра начинается с этого метода, в котором определяются размеры поля,
        количество мин, инициализируются ячейки.
        """
        if rowCount in range(MIN_ROW_COUNT, MAX_ROW_COUNT + 1):
            self.rowCount = rowCount
        # Для случаев, когда число строк выходит за допустимые пределы.
        # Для столбцов аналогично.
        elif rowCount < MIN_ROW_COUNT:
            self.rowCount = MIN_ROW_COUNT
        else:
            self.rowCount = MAX_ROW_COUNT

        if columnCount in range(MIN_COLUMN_COUNT, MAX_COLUMN_COUNT + 1):
            self.columnCount = columnCount
        elif columnCount < MIN_COLUMN_COUNT:
            self.columnCount = MIN_COLUMN_COUNT
        else:
            self.columnCount = MAX_COLUMN_COUNT

        self.min_mine = round(self.rowCount * self.columnCount * 1 / 8)       
        self.max_mine = round(self.rowCount * self.columnCount * 6 / 8)
        
        if mineCount in range(self.min_mine, self.max_mine):
            self.mineCount = mineCount
        elif mineCount < self.min_mine:
            self.mineCount = self.min_mine
        else:
            self.mineCount = self.max_mine
        
        self.firstStep = True
        self.gameOver = False
        self.cellsTable = []
        
        for row in range(self.rowCount):
            cellsRow = []
            for column in range(self.columnCount):
                cellsRow.append(MinesweeperCell(row, column))
            self.cellsTable.append(cellsRow)

    def getCell(self, row, column):
        """
        Возвращает объект ячейки по адресу row : column.
        """
        if row < 0 or column < 0 or row >= self.rowCount or column >= self.columnCount:
            return None
        return self.cellsTable[row][column]

    def isWin(self):
        """
        Метод возвращает True, если каждая ячейка соответствует одному из условий
        Победы, а именно:
            - Ячейка заминирована.
            - Ячейка открыта.
            - Ячейка помечена флагом.
        """
        for row in range(self.rowCount):
            for column in range(self.columnCount):
                cell = self.cellsTable[row][column]
                if not cell.mined and cell.state != 'opened' and cell.state != 'flagged':
                    return False
        return True

    def isGameOver(self):
        """
        Возращает значение self.gameOver, которое устанавливается в истину,
        в случае поражения.
        """
        return self.gameOver

    def openCell(self, row,column):
        """
        Метод открытия ячеек.
        Во время первого хода происходит генерация заминированных полей.
        Если открываемая ячейка заминирована - игра окончена.
        Если вокруг ячейки нет мин, то выполняется открытие соседних ячеек.
        """
        cell = self.getCell(row, column)
        if not cell:
            return

        cell.open()

        if cell.mined:
            self.gameOver = True
            return

        if self.firstStep:
            self.firstStep = False
            self.generateMines()

        cell.counter = self.countMinesAroundCell(row, column)
        if cell.counter == 0:
            self.openNeighbours(row, column)

    def countFlaggedNeighbours(self, row, column):
        """
        Метод возращает количество соседних полей помеченных флажком.
        """
        neighbours = self.getCellNeighbours(row, column)
        count = 0
        for n in neighbours:
            if n.state == 'flagged':
                count +=1
        return count

    def openNeighbours(self, row, column):
        """
        Метод окрытия соседних полей.
        Поля вокруг ячейки с адресом (row;column) открываются, и если
        среди них есть заминированное поле не помеченное флажком - игра окончена.
        """
        neighbours = self.getCellNeighbours(row, column)
        for n in neighbours:
            if n.state == 'closed':
                self.openCell(n.row, n.column)
            if n.mined and not n.state == 'flagged':
                self.gameOver = True
                return

    def openClearNeighbours(self, row, column):
        """
        Метод открывает ячейки вокруг поля (row;column), если
        числомин вокруг данного поля равно числу полей помеченных флажком.
        """
        count_mines = self.countMinesAroundCell(row,column)
        count_flags = self.countFlaggedNeighbours(row, column)

        if count_mines == count_flags:
            self.openNeighbours(row, column)

    def nextCellMark(self, row, column):
        """
        Циклически меняет метку поля.
        """
        cell = self.getCell(row, column)
        if cell:
            cell.nextMark()

    def generateMines(self):
        """
        Метод генерации мин на поле.
        Метод выполняется после первого хода. Открытая в первом
        ходе ячейка не может быть заминирована.
        """
        for i in range(self.mineCount):
            while True:
                row = random.randint(0, self.rowCount - 1)
                column = random.randint(0, self.columnCount -1)
                cell = self.getCell(row, column)
                if not cell.state == 'opened' and not cell.mined:
                    cell.mined = True
                    break

    def countMinesAroundCell(self, row, column):
        """
        Метод подсчета заминированных ячеек вокруг данной.
        """
        neighbours = self.getCellNeighbours(row, column)
        return sum(1 for n in neighbours if n.mined)

    def getCellNeighbours(self, row, column):
        """
        Возвращает список соседних ячеек.
        """
        neighbours = []
        for r in range(row - 1, row + 2):
            neighbours.append(self.getCell(r, column - 1))
            if r != row:
                neighbours.append(self.getCell(r, column))
            neighbours.append(self.getCell(r, column + 1))

        return filter(lambda n: n is not None, neighbours)

class MinesweeperView(Frame):
    """
    Класс представления.
    Определяет графический пользовательский интерфейс.
    """
    def __init__(self, model, controller, parent = None):
        Frame.__init__(self, parent)
        self.model = model
        self.controller = controller
        self.controller.setView(self)
        self.createBoard()

        panel = Frame(self)
        panel.pack(side = BOTTOM, fill = X)

        Button(panel, text = 'New Game', command = self.controller.startNewGame).pack(side = RIGHT)
        
        self.mineCount = StringVar(panel)
        self.mineCount.set(self.model.mineCount)
        Spinbox(
                panel,
                from_ = model.min_mine,
                to = model.max_mine,
                textvariable = self.mineCount,
                width = 5
        ).pack(side = RIGHT)
        
        self.rowCount = StringVar(panel)
        self.rowCount.set(self.model.rowCount)
        Spinbox(
                panel,
                from_ = MIN_ROW_COUNT,
                to = MAX_ROW_COUNT,
                textvariable = self.rowCount,
                width = 5
        ).pack(side = RIGHT)

        Label(panel, text = ' x ').pack(side = RIGHT)

        self.columnCount = StringVar(panel)
        self.columnCount.set(self.model.columnCount)

        Spinbox(
                panel,
                from_ = MIN_COLUMN_COUNT,
                to = MAX_COLUMN_COUNT,
                textvariable = self.columnCount,
                width = 5
        ).pack(side = RIGHT)
        Label(panel, text = 'Board size: ').pack(side = RIGHT)

    def syncWithModel(self):
        """
        Метод синхронизации представления с модлью.
        """
        for row in range(self.model.rowCount):
            for column in range(self.model.columnCount):
                cell = self.model.getCell(row, column)
                if cell:
                    btn = self.buttonsTable[row][column]

                    if cell.state == 'closed':
                        btn.config(bg = 'lightblue', text = '')
                    elif cell.state == 'opened':
                        btn.config(relief = SUNKEN, bg='white', text='')
                        if cell.counter > 0:
                            btn.config(text = cell.counter)
                    elif cell.state == 'flagged':
                        btn.config(bg = 'orange', text = 'P')
                    elif cell.state == 'questioned':
                        btn.config(text = '?')
                    
                    if self.model.isGameOver() and cell.mined:
                        if cell.state == 'opened':
                            btn.config(bg = 'red', text = ':x')
                        else:
                            btn.config(bg = 'purple', text = 'x')

    def blockCell(self, row, column, block = True):
        """
        Метод блокирует заданную ячейку для ЛКМ.
        """
        btn = self.buttonsTable[row][column]
        if not btn:
            return

        if block:
            btn.bind('<Button-1>', 'break')
        else:
            btn.unbind('<Button-1>')

    def getGameSettings(self):
        """
        Возвращает параметры игры.
        """
        return self.rowCount.get(), self.columnCount.get(), self.mineCount.get()

    def createBoard(self):
        """
        Метод создает графическое представление игрового поля.
        """
        try:
            self.board.pack_forget()
            self.board.destroy()

            self.rowCount.set(self.model.rowCount)
            self.columnCount.set(self.model.columnCount)
            self.mineCount.set(self.model.mineCount)
        except:
            pass

        self.board = Frame(self)
        self.board.pack()
        self.buttonsTable = []
        for row in range(self.model.rowCount):
            line = Frame(self.board)
            line.pack(side = TOP)
            self.buttonsRow = []
            for column in range(self.model.columnCount):
                btn = Button(
                        line,
                        width = 2,
                        height = 1,
                        command = lambda row = row, column = column: self.controller.onLeftClick(row, column),
                        padx = 0,
                        pady = 0
                )
                btn.config(bg = 'lightblue')
                btn.pack(side = LEFT)
                btn.bind(
                        '<Button-3>',
                        lambda e, row = row, column = column: self.controller.onRightClick(row, column)
                )
                btn.bind(
                        '<Button-2>',
                        lambda e, row = row, column = column: self.controller.onMiddleClick(row, column)
                )
                self.buttonsRow.append(btn)

            self.buttonsTable.append(self.buttonsRow)

    def showWinMessage(self):
        tkinter.messagebox.showinfo('Congratulations!', 'You win! 8)')

    def showGameOverMessage(self):
        tkinter.messagebox.showinfo('Game Over!', 'You lose! 8x')

class MinesweeperController:
    """
    Класс контроллера.
    Обеспечивает взаимодействи модели и представления.
    """
    def __init__(self, model):
        self.model = model

    def setView(self, view):
        self.view = view

    def startNewGame(self):
        gameSettings = self.view.getGameSettings()
        try:
            self.model.startGame(*map(int, gameSettings))
        except:
            self.model.startGame(self.model.rowCount, self.model.columnCount, self.model.mineCount)

        self.view.createBoard()

    def onLeftClick(self, row, column):
        """
        Обработчик нажатия левой кнопки мыши.
        """
        self.model.openCell(row, column)
        self.checkStateGame()

    def onRightClick(self, row, column):
        """
        Обработчик нажатия правой кнопки мыши.
        """
        self.model.nextCellMark(row, column)
        self.view.blockCell(row, column, self.model.getCell(row, column).state == 'flagged')
        self.view.syncWithModel()

    def onMiddleClick(self, row, column):
        """
        Клик СКМ по открытой клетке открывает соседние ячейки, если число помеченных флагом
        мин соответствует числу в ячейке.
        """
        self.model.openClearNeighbours(row, column)
        self.checkStateGame()
    
    def checkStateGame(self):
        """
        Выполняет проверку состояния игры, и если игрок выиграл или проиграл
        выводится соответствующее собщение, после чего начинается новая игра.
        """
        if self.model.isWin():
            self.view.syncWithModel()
            self.view.showWinMessage()
            self.startNewGame()
        elif self.model.isGameOver():
            self.view.syncWithModel()
            self.view.showGameOverMessage()
            self.startNewGame()
        else:
            self.view.syncWithModel()


def main(argv=sys.argv):
    model = MinesweeperModel()
    controller = MinesweeperController(model)
    view = MinesweeperView(model, controller)
    view.pack()
    view.mainloop()

if __name__ == "__main__":
    sys.exit(main())
