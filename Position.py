class Pos:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  
  def __getX__(self):
    return self.x

  def __getY__(self):
    return self.y

  def __equals__(self, other):
    return self.x == other.x and self.y == other.y

  def __str__(self):
    return "(" + self.x + " " + self.y + ")"