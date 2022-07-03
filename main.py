import sys
from OthelloGame import Cell, Othello
from Position import Pos

game = Othello(8)


def possibleMove(row, col):
  posMoves = game.__possibleMoves__(game.curPlayer)
  for k in range(len(posMoves)):
    if (posMoves[k] != None):
      pos = posMoves[k].get("pos")
      if (pos.__equals__(Pos(row, col))):
        return True
  return False
  

# Helper method to render the board in a text view.
def renderBoard():
  s = "White: " + str(game.__getScore__(Cell.white)) + "\t\tBlack: " + str(game.__getScore__(Cell.black)) + "\n"

  posMoves = game.__possibleMoves__(game.curPlayer)
  
 

  # for i in range(len(posMoves)):
  #   if (posMoves[i] != None):
  #     pos = posMoves[i]
  #     game.board[pos.__getX__()][pos.__getY__()] = Cell.possible
  #     print(str(pos.__getX__()) + " " + str(pos.__getY__()))

  for i in range(game.boardSize):
    s += '\t'
    for j in range(game.boardSize):
      cell = game.board[i][j]
      if (cell == Cell.empty):
        if (possibleMove(i, j)):
          s += "+ "
        else:
          s += '- '
      elif (cell == Cell.white):
        s += 'O '
      elif (cell == Cell.black):
        s += 'X '

    s += '\n'

  return s


while(not game.__isGameEnd__()):
  print(renderBoard())

  row = input("Enter the row")
  col = input("Enter the column")

  if (row == "q" or col == "q"):
    print("Thanks for playing!")
    break

  game.__placePiece__(int(row) - 1, int(col) - 1)

