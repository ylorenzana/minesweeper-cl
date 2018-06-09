import copy, random

class Cell:
    def __init__(self, value, row, column):
        self.neighbors = []
        self.value = value
        self.row = row
        self.column = column
        self.wasRevealed = False
        self.isMine = False

class Minesweeper:
    def __init__(self, n):
        self.board = []
        row = 0
        column = 0
        for row in range(n):
            self.board.append([])
            for column in range(n):
                cell = Cell("H", row, column)
                self.board[row].append(cell)
        self.userBoard = copy.deepcopy(self.board)
        self.minePlacement()
        self.neighbors()
        self.countMines()

    def minePlacement(self, m = 5):
        maxRange = len(self.board) - 1
        for i in range(m):
            mineRow = random.randint(0, maxRange)
            mineColumn = random.randint(0, maxRange)
            self.board[mineRow][mineColumn].value = "M"
            self.board[mineRow][mineColumn].isMine = True
            self.userBoard[mineRow][mineColumn].isMine = True  

    def neighbors(self):
        rowCounter = 0
        columnCounter = 0
        for row in self.board:
            columnCounter = 0
            for cell in row:
                for rowOffset in range(-1, 2, 1):
                    neighborsRow = rowCounter + rowOffset
                    if (neighborsRow < 0 or neighborsRow >= len(self.board)):
                        continue
                    for colOffset in range(-1, 2, 1):
                        neighborsCol = columnCounter + colOffset
                        if (neighborsRow == rowCounter and neighborsCol == columnCounter):
                            continue
                        if (neighborsCol < 0 or neighborsCol >= len(self.board)):
                            continue
                        cell.neighbors.append(self.board[neighborsRow][neighborsCol])      
                columnCounter += 1
            rowCounter += 1

    def countMines(self):
        for row in self.board:
            for cell in row:
                mineCount = 0
                if cell.isMine == False:
                    for neighbor in cell.neighbors:
                        if neighbor.value == "M":
                            mineCount += 1
                    cell.value = mineCount
                        
    def displayUserBoard(self):
        for row in self.userBoard:
            for cell in row:
                print(cell.value, " ", end="")
            print("")

    def displayBoard(self):
        for row in self.board:
            for cell in row:
                print(cell.value, " ", end="")
            print("")
    

    def revealCell(self, row, column):
        if self.board[row][column].value != 0 and self.board[row][column].wasRevealed == False:
            self.board[row][column].wasRevealed = True
            self.userBoard[row][column] = self.board[row][column]
        elif self.board[row][column].value == 0 and self.board[row][column].wasRevealed == False:
            self.userBoard[row][column] = self.board[row][column]
            self.board[row][column].wasRevealed = True
            for neighbor in self.board[row][column].neighbors:
                self.revealCell(neighbor.row, neighbor.column)

    def gameWon(self):
        gameIsWon = False
        for row in self.userBoard:
            for cell in row:
                if not cell.isMine:
                    if cell.wasRevealed:
                        gameIsWon = True
                    else:
                        gameIsWon = False
                        return gameIsWon
        return gameIsWon


def main():
    game = Minesweeper(5)
    game.displayUserBoard()
    print("")
    game.displayBoard()
    while True:
        try:
            row, column = eval(input("Select a cell (row, column): ")) 
            if game.board[row][column].isMine:
                game.displayBoard()
                print("You hit a mine! Game over.")
                break
            game.revealCell(row, column)
            print("")
            game.displayUserBoard()
            print("")
            if game.gameWon():
                print("You win!")
                game.displayBoard()
                print("")
                break
        except (TypeError, NameError, IndexError):
            print("Please enter two numbers separated by a comma.")
            
        
main()
