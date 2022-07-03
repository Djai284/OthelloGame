import enum

from Position import Pos

'''
This class represents the Othello game. This class will define all the 
game operations possible in a two player game of Othello (aka Reversee).

Fields:
  - BoardSize : The size of the square board. A game of Othello can only be played on 
                a square board of even dimensions greater than 4.
  - Grid of Cells : Represents the game board
    - A Cell is an enumeration of the states of specific cells 
      (black, white, empty)
  - Current Move : Represents how many moves have been played

These include the following:
  - placePiece() : Places a game piece onto the board
'''

class Cell(enum.Enum):
  '''
    There are finite states of a cell. It can either be black, white, or empty.
    There is no other possibility, and therefore we are using the enumeration type.
  '''
  empty = 0
  white = 1
  black = 2

class Othello:

  def __init__(self, boardSize):
    # Board size is invalid if odd or less than 4  
    if (boardSize % 2 == 1 or boardSize < 4):
      raise Exception("Board size must be even and greater than or equal to 4.")

    self.boardSize = boardSize

    rows, cols = (boardSize, boardSize)
    self.board = [[Cell.empty for i in range(cols)] for j in range(rows)]

    # Sets the 4 middle pieces
    cell = int(boardSize/2)
    
    # Sets the 4 middle pieces
    self.board[cell][cell] = Cell.white
    self.board[cell - 1][cell - 1] = Cell.white
    self.board[cell][cell - 1] = Cell.black
    self.board[cell - 1][cell] = Cell.black

    self.curPlayer = Cell.black

  # Small Helper Method to see if a row and column is out of bounds
  def __outOfBounds__(self, row, col):
    return row >= self.boardSize or col >= self.boardSize or row < 0 or col < 0

  '''
  Places the piece on the board. Will be mainly used in the main game loop when we take in 
  user inputs for moves. This method will check for any invalid inputs and return associated 
  exceptions.
  '''
  def __placePiece__(self, row, col):
    if (self.__outOfBounds__(row, col)):
      raise Exception("Row and Column must be within the range of the board.") 
    else:
      moves = self.__possibleMoves__(self.curPlayer)
      pos = Pos(row, col)
      
      playerTurn = False

      for i in range(len(moves)):
        if(moves[i] != None):
          if (moves[i].get("pos").__equals__(pos)):
            self.board[row][col] = self.curPlayer
            self.__flipPieces__(moves[i].get("pieces"), self.curPlayer)
            playerTurn = True
      

      if(playerTurn):
        # Changes the current player
        if (self.curPlayer == Cell.black):
          self.curPlayer = Cell.white
        else:
          self.curPlayer = Cell.black
            


  '''
  Flips the pieces that are given to the given color (usually, it will be the current player)
  '''
  def __flipPieces__(self, pieces, color):
    for piece in pieces:
      self.board[piece.__getX__()][piece.__getY__()] = color
    
 
  '''
  Checks the board for all possible moves given a Cell color. Does this by searching through
  all 8 directions around the given cell. Returns a list of moves with their associated points possible
  and pieces to flip.
  '''
  def __possibleMoves__(self, Cell):
    moves = []

    for i in range(self.boardSize):
      for j in range(self.boardSize):
        if (self.board[i][j] == Cell):
          # Search Up
          moves.append(self.__search__("up", i - 1, j, 0, [], Cell))

          # Search Down
          moves.append(self.__search__("down", i + 1, j, 0, [], Cell))

          # Search Left
          moves.append(self.__search__("left", i, j - 1, 0, [], Cell))

          # Search Right
          moves.append(self.__search__("right", i, j + 1, 0, [], Cell))

          # Search UpLeft
          moves.append(self.__search__("upLeft", i - 1, j - 1, 0, [], Cell))

          # Search UpRight
          moves.append(self.__search__("upRight", i - 1, j + 1, 0, [], Cell))

          # Search DownLeft
          moves.append(self.__search__("downLeft", i + 1, j - 1, 0, [], Cell))

          # Search DownRight
          moves.append(self.__search__("downRight", i + 1, j + 1, 0, [], Cell))

    return moves

  '''
  This search method searhces through any direction and returns whether there is a valid move
  at the end. It uses a starting position and recursively searches up the board to see if there is a 
  '''
  def __search__(self, direction, row, col, points, pieces, Cell):
    if (self.__outOfBounds__(row, col)):
      return None
    elif (self.board[row][col] == Cell.empty):
      # Returns this as a dictionary
      if (points == 0):
        return None
      else:
        return {
          "pos" : Pos(row, col), 
          "dir" : direction,
          "points" : points, 
          "pieces" : pieces
          }

    elif(self.board[row][col] == Cell):
      return None
  
    else:
      pieces.append(Pos(row, col))

      if (direction == "up"):
        return self.__search__(direction, row - 1, col, points + 1, pieces, Cell)
      elif (direction == "down"):
        return self.__search__(direction, row + 1, col, points + 1, pieces, Cell)
      elif (direction == "right"):
        return self.__search__(direction, row, col + 1, points + 1, pieces, Cell)
      elif (direction == "left"):
        return self.__search__(direction, row, col - 1, points + 1, pieces, Cell)
      elif (direction == "upLeft"):
        return self.__search__(direction, row - 1, col - 1, points + 1, pieces, Cell)
      elif (direction == "upRight"):
        return self.__search__(direction, row - 1, col + 1, points + 1, pieces, Cell)
      elif (direction == "downLeft"):
        return self.__search__(direction, row + 1, col - 1, points + 1, pieces, Cell)
      elif (direction == "downRight"):
        return  self.__search__(direction, row + 1, col + 1, points + 1, pieces, Cell)

  ''' 
  Returns the current player based on the move. Because this is 
  a two player game, we can assume that an even current move means that
  the current player is using the black pieces, and white pieces if the 
  current move is odd.
  '''
  def __getCurPlayer__(self):
    if (self.curMove % 2 == 0):
      return Cell.black
    else:
      return Cell.white

  '''
  Checks if the game has ended if there are no longer any possible moves.
  NEEDS TO BE FIXED
  '''
  def __isGameEnd__(self):
    return len(self.__possibleMoves__(Cell.white)) == 0 and len(self.__possibleMoves__(Cell.black)) == 0

  '''
  Gets the score of a given cell state (color).
  '''
  def __getScore__(self, Cell):
    score = 0

    for i in range(self.boardSize):
      for j in range(self.boardSize):
        if (self.board[i][j] == Cell):
          score += 1
    
    return score
