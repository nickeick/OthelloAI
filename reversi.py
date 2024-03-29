# Reversi

import random
import sys
import matplotlib.pyplot as plt

def drawBoard(board):
     # This function prints out the board that it was passed. Returns None.
     HLINE = '  +---+---+---+---+---+---+---+---+'
     VLINE = '  |   |   |   |   |   |   |   |   |'

     print('    1   2   3   4   5   6   7   8')
     print(HLINE)
     for y in range(8):
         print(VLINE)
         print(y+1, end=' ')
         for x in range(8):
             print('| %s' % (board[x][y]), end=' ')
         print('|')
         print(VLINE)
         print(HLINE)


def resetBoard(board):
     # Blanks out the board it is passed, except for the original starting position.
     for x in range(8):
         for y in range(8):
             board[x][y] = ' '

     # Starting pieces:
     board[3][3] = 'X'
     board[3][4] = 'O'
     board[4][3] = 'O'
     board[4][4] = 'X'


def getNewBoard():
     # Creates a brand new, blank board data structure.
     board = []
     for i in range(8):
         board.append([' '] * 8)

     return board


def isValidMove(board, tile, xstart, ystart):
     # Returns False if the player's move on space xstart, ystart is invalid.
     # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
     if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
         return False

     board[xstart][ystart] = tile # temporarily set the tile on the board.

     if tile == 'X':
         otherTile = 'O'
     else:
         otherTile = 'X'

     tilesToFlip = []
     for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
         x, y = xstart, ystart
         x += xdirection # first step in the direction
         y += ydirection # first step in the direction
         if isOnBoard(x, y) and board[x][y] == otherTile:
             # There is a piece belonging to the other player next to our piece.
             x += xdirection
             y += ydirection
             if not isOnBoard(x, y):
                 continue
             while board[x][y] == otherTile:
                 x += xdirection
                 y += ydirection
                 if not isOnBoard(x, y): # break out of while loop, then continue in for loop
                     break
             if not isOnBoard(x, y):
                 continue
             if board[x][y] == tile:
                 # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                 while True:
                     x -= xdirection
                     y -= ydirection
                     if x == xstart and y == ystart:
                         break
                     tilesToFlip.append([x, y])

     board[xstart][ystart] = ' ' # restore the empty space
     if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
         return False
     return tilesToFlip


def isOnBoard(x, y):
     # Returns True if the coordinates are located on the board.
     return x >= 0 and x <= 7 and y >= 0 and y <=7

def getBoardWithValidMoves(board, tile):
     # Returns a new board with . marking the valid moves the given player can make.
     dupeBoard = getBoardCopy(board)

     for x, y in getValidMoves(dupeBoard, tile):
         dupeBoard[x][y] = '.'
     return dupeBoard


def getValidMoves(board, tile):
     # Returns a list of [x,y] lists of valid moves for the given player on the given board.
     validMoves = []

     for x in range(8):
         for y in range(8):
             if isValidMove(board, tile, x, y) != False:
                 validMoves.append([x, y])
     return validMoves


def getScoreOfBoard(board):
     # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
     xscore = 0
     oscore = 0
     for x in range(8):
         for y in range(8):
             if board[x][y] == 'X':
                 xscore += 1
             if board[x][y] == 'O':
                 oscore += 1
     return {'X':xscore, 'O':oscore}


def enterPlayerTile():
     # Lets the player type which tile they want to be.
     # Returns a list with the player's tile as the first item, and the computer's tile as the second.
     tile = ''
     while not (tile == 'X' or tile == 'O'):
         print('Do you want to be X or O?')
         tile = input().upper()

     # the first element in the list is the player's tile, the second is the computer's tile.
     if tile == 'X':
         return ['X', 'O']
     else:
         return ['O', 'X']


def whoGoesFirst():
     # Randomly choose the player who goes first.
     #if random.randint(0, 1) == 0:
         #return 'computer'
     #else:
         return 'player'


def playAgain():
     # This function returns True if the player wants to play again, otherwise it returns False.
     print('Do you want to play again? (yes or no)')
     return input().lower().startswith('y')


def makeMove(board, tile, xstart, ystart):
     # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
     # Returns False if this is an invalid move, True if it is valid.
     tilesToFlip = isValidMove(board, tile, xstart, ystart)

     if tilesToFlip == False:
         return False

     board[xstart][ystart] = tile
     for x, y in tilesToFlip:
         board[x][y] = tile
     return True


def getBoardCopy(board):
     # Make a duplicate of the board list and return the duplicate.
     dupeBoard = getNewBoard()

     for x in range(8):
         for y in range(8):
             dupeBoard[x][y] = board[x][y]


     return dupeBoard


def isOnCorner(x, y):
     # Returns True if the position is in one of the four corners.
     return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


def getPlayerMove(board, playerTile):
     #------Alph-beta call------
     return getAlphaBetaMove(board, playerTile)
     #------Original player input-------
     # Let the player type in their move.
     # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
##     DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
##     while True:
##         print('Enter your move, or type quit to end the game, or hints to turn off/on hints.')
##         move = input().lower()
##         if move == 'quit':
##             return 'quit'
##         if move == 'hints':
##             return 'hints'
##
##         if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
##             x = int(move[0]) - 1
##             y = int(move[1]) - 1
##             if isValidMove(board, playerTile, x, y) == False:
##                 continue
##             else:
##                 break
##         else:
##             print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
##             print('For example, 81 will be the top-right corner.')


# ------------- Alpha-Beta Pruning -----------
minvalue = -1
maxvalue = 101 #max board score + 1
infinity = float('inf')
def getAlphaBetaMove(board, computerTile):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    possibleMoves = getValidMoves(board, computerTile)
    # randomize the order of the possible moves
    random.shuffle(possibleMoves)
    # always go for a corner if available.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]
    # Body of alphabeta_search:
    bestScore = -infinity
    beta = infinity
    alpha = -infinity
    bestMove = None
    for x,y in possibleMoves:
        dupeBoard = getBoardCopy(board)

        makeMove(dupeBoard, computerTile, x, y)
        score = Minimax(dupeBoard, 3, True, computerTile, alpha, beta)
        if score > bestScore:
            bestScore = score
            bestMove = [x,y]
    return bestMove

def Minimax(board, depth, maxim, computerTile, alpha, beta):
    possibleMoves = getValidMoves(board, computerTile)
    if possibleMoves == [] or depth==0:
        return getScoreOfBoard(board)[computerTile]
    if maxim:
        bestValue = minvalue
        for x , y in possibleMoves:
            newBoard = getBoardCopy(board)
            makeMove(newBoard,computerTile,x,y)
            v = Minimax(newBoard, depth - 1, False,computerTile, alpha, beta)
            bestValue = max(bestValue, v)
            alpha = max(alpha, bestValue)
            if beta<=alpha:
                break
    else:
        bestValue = maxvalue
        for x,y in possibleMoves:
            newBoard = getBoardCopy(board)
            makeMove(newBoard,computerTile,x,y)
            v = Minimax(newBoard, depth - 1, True,computerTile, alpha, beta)
            bestValue = min(bestValue, v)
            beta = min(bestValue, beta)
            if alpha >=beta:
                break
    return bestValue
          


def getComputerMove(board, computerTile):
     # ------------ Weighted Map Agent --------------
     bestMove = "empty"
     bestScore = 0
     priorities = {
          "11":100, "18":100, "81":100, "88":100,
          "13":90, "31":90, "16":90, "61":90, "38":90, "83":90, "68":90, "86":90,
          "67":85, "76":85, "26":85, "62":85, "23":85, "32":85, "37":85, "73":85,
          "41":80, "14":80, "51":80, "15":80, "48":80, "84":80, "58":80, "85":80,
          "33":75, "36":75, "63":75, "66":75,
          "34":70, "43":70, "35":70, "53":70, "46":70, "64":70, "56":70, "65":70,
          "24":50, "42":50, "25":50, "52":50, "47":50, "74":50, "57":50, "75":50,
          "12":20, "21":20, "17":20, "71":20, "28":20, "82":20, "78":20, "87":20,
          "22":10, "27":10, "72":10, "77":10
          }
     possibleMoves = getValidMoves(board, computerTile)
     for x, y in possibleMoves:
          move = str(x + 1) + str(y + 1)
          if priorities[move] > bestScore:
               bestMove = move
          bestScore = max(priorities[move], bestScore)
     return [int(bestMove[0]) - 1, int(bestMove[1]) - 1]
     # ------------ Random Agent --------------
##     possibleMoves = getValidMoves(board, computerTile)
##     #print(possibleMoves)
##     random.shuffle(possibleMoves)
##     for x, y in possibleMoves:
##          return [x, y]
# ------------ Local Maximization Agent --------------
##     # Given a board and the computer's tile, determine where to
##     # move and return that move as a [x, y] list.
##     possibleMoves = getValidMoves(board, computerTile)
##
##     # randomize the order of the possible moves
##     random.shuffle(possibleMoves)
##
##     # always go for a corner if available.
##     for x, y in possibleMoves:
##         if isOnCorner(x, y):
##             return [x, y]
##
##     # Go through all the possible moves and remember the best scoring move
##     bestScore = -1
##     for x, y in possibleMoves:
##         dupeBoard = getBoardCopy(board)
##         makeMove(dupeBoard, computerTile, x, y)
##         score = getScoreOfBoard(dupeBoard)[computerTile]
##         if score > bestScore:
##             bestMove = [x, y]
##             bestScore = score
##     return bestMove

def getRandomMove(board, tile):
    possibleMoves = getValidMoves(board, tile)
    #print(possibleMoves)
    random.shuffle(possibleMoves)
    for x, y in possibleMoves:
        return [x, y]


class Tree:
    def __init__(self):
        self.nodes = []
        self.position = []
        self.visits = 0
        self.reward = 0
    
    def is_leaf(self):
        if self.nodes == []:
            return True
        else:
            return False

    def set_position(self, x, y):
        self.position = [x, y]

    def add_nodes(self, positions):
        for x, y in positions:
            new_node = Tree()
            new_node.set_position(x, y)
            self.nodes.append(new_node)
    
    def add_visit(self):
        self.visits += 1

    def add_reward(self):
        self.reward += 1

    def get_strongest_node(self):
        strength = 0
        strongest = None
        for node in self.nodes:
            if not node.is_leaf():
                node_strength = node.reward / node.visits
                if node_strength > strength:
                    strongest = node
                    strength = node_strength
        return strongest

    def get_random_node(self):
        possibleNodes = self.nodes
        random.shuffle(possibleNodes)
        return possibleNodes[0]


def getMCTSMove(board, tile, tree):
    if tree.is_leaf():
            possibleMoves = getValidMoves(board, tile)
            tree.add_nodes(possibleMoves)
            return 'rollout'

    if random.randint(0, 9) > 0:
        #exploit
        strongest = tree.get_strongest_node()
        if strongest == None:
            node = tree.get_random_node()
        else:
            node = strongest

    else:
        #explore
        node = tree.get_random_node()
    node.add_visit()
    return node
        

def MCTS_train():
    MCTS_tree = Tree()
    mainBoard = getNewBoard()
    playerTile = 'X'
    computerTile = 'O'
    game_wins = 0
    success_rate = []
    for game in range(10001):
        if game % 100 == 0:
            #Every 100 games, reset game wins to recalculate success rate
            success_rate.append(game_wins / 100)
            game_wins = 0
        resetBoard(mainBoard)
        turn = 'player'
        rollout = False
        node = MCTS_tree
        played_nodes = []
        while True:
            if turn == 'player':
                if rollout == False:
                    node = getMCTSMove(mainBoard, playerTile, node)
                    if node == 'rollout':
                        rollout = True
                        move = getRandomMove(mainBoard, playerTile)
                    else:
                        move = node.position
                        played_nodes.append(node)
                else:
                    move = getRandomMove(mainBoard, playerTile)
                #move = getPlayerMove(mainBoard, 'X')
                makeMove(mainBoard, playerTile, move[0], move[1])
                if getValidMoves(mainBoard, computerTile) == []:
                    #break
                    if getValidMoves(mainBoard, playerTile) == []:
                        break
                    else:
                        turn = 'player'
                else:
                    turn = 'computer'
            else:
                x, y = getComputerMove(mainBoard, computerTile)
                makeMove(mainBoard, computerTile, x, y)

                if getValidMoves(mainBoard, playerTile) == []:
                    #break
                    if getValidMoves(mainBoard, computerTile) == []:
                        break
                    else:
                        turn = 'computer'
                else:
                    turn = 'player'
        scores = getScoreOfBoard(mainBoard)
        if scores[playerTile] > scores[computerTile]:
            # Win
            for node in played_nodes:
                node.add_reward()
            game_wins += 1
    plt.plot(range(1, len(success_rate)+1), success_rate)
    plt.show()




def showPoints(playerTile, computerTile):
     # Prints out the current score.
     scores = getScoreOfBoard(mainBoard)
     print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))



print('Welcome to Reversi!')
'''
while True:
     # Reset the board and game.
     mainBoard = getNewBoard()
     resetBoard(mainBoard)
     playerTile, computerTile = enterPlayerTile()
     showHints = False
     turn = whoGoesFirst()
     print('The ' + turn + ' will go first.')

     while True:
         if turn == 'player':
             # Player's turn.
             if showHints:
                 validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
                 drawBoard(validMovesBoard)
             #else:
                 #drawBoard(mainBoard)
             #showPoints(playerTile, computerTile)
             move = getPlayerMove(mainBoard, playerTile)
             if move == 'quit':
                 print('Thanks for playing!')
                 sys.exit() # terminate the program
             elif move == 'hints':
                 showHints = not showHints
                 continue
             else:
                 makeMove(mainBoard, playerTile, move[0], move[1])

             if getValidMoves(mainBoard, computerTile) == []:
                 #break
                 if getValidMoves(mainBoard, playerTile) == []:
                      break
                 else:
                      turn = 'player'
             else:
                 turn = 'computer'

         else:
             # Computer's turn.
             #drawBoard(mainBoard)
             #showPoints(playerTile, computerTile)
             #input('Press Enter to see the computer\'s move.')
             x, y = getComputerMove(mainBoard, computerTile)
             makeMove(mainBoard, computerTile, x, y)

             if getValidMoves(mainBoard, playerTile) == []:
                 #break
                 if getValidMoves(mainBoard, computerTile) == []:
                      break
                 else:
                      turn = 'computer'
             else:
                 turn = 'player'

     # Display the final score.
     drawBoard(mainBoard)
     scores = getScoreOfBoard(mainBoard)
     print('X scored %s points. O scored %s points.' % (scores['X'], scores['O']))
     if scores[playerTile] > scores[computerTile]:
         print('You beat the computer by %s points! Congratulations!' % (scores[playerTile] - scores[computerTile]))
     elif scores[playerTile] < scores[computerTile]:
         print('You lost. The computer beat you by %s points.' % (scores[computerTile] - scores[playerTile]))
     else:
         print('The game was a tie!')

     if not playAgain():
         break
'''
MCTS_train()