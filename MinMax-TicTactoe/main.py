from time import sleep
import turtle

def clk_hnd(x, y):
    """This method is the click handler for each of the tiles
    It is to be used in GUI mode. For some reason it only works if I check that the mouse is on the tile
    even though the event handler gets tied to a specific tile"""
    global game # Make use of the global game object
    for t in game.lstTiles: # For some reason I still need to do boundary checking (shrugs)
        if t.token.distance(x, y) <= 50 and not t.taken:
            game.act(t) # Place the current player's tile in the selected spot
            break # don't search through all tiles

class Tile:
    """This class is used to visualise the game. There is a tile on each playable space
    When it is selected, it changes to the current player's symbol"""
    def __init__(self, index, coords):
        self.index = index
        self.token = turtle.Turtle()
        self.token.speed(0)
        self.token.penup()
        self.token.shape("circle")
        self.token.color("grey") # blend in with the background until needed
        self.token.shapesize(stretch_wid=5, stretch_len=5)
        self.token.seth(90)
        x, y = coords
        self.token.goto(x, y)
        self.taken = False
        self.token.onclick(clk_hnd)

class Game:
    """This class is the game controller. It handles the state, current player and turns. It is also used to
    check when the game ends, calculate the expected score of a state and handles visualization"""
    def __init__(self):
        self.CurrentPlayer = 0
        self.state = [['.','.','.'], 
                      ['.','.','.'],
                      ['.','.','.']]
        self.lstTiles = []
        self.dCoords = {0: (-100, 100), 1: (0, 100), 2: (100, 100), 3: (-100, 0), 4: (0, 0), 5: (100, 0), 6: (-100, -100), 7: (0, -100), 8: (100, -100), }
        self.symbols = ["O", "X", "."]
        self.setup()

    def setup(self):
        """This method starts the GUI and draws the board"""
        self.screen = turtle.setup(310, 310)
        turtle.Screen().bgcolor("grey")
        turtle.register_shape("X.gif")
        turtle.register_shape("O.gif")
        pen = turtle.Turtle()
        pen.penup()
        pen.speed(0)
        pen.color("white")
        pen.hideturtle()
        pen.seth(270)
        for l in range(2):
            pen.goto(-50 + (l* 100), 150)
            pen.pendown()
            pen.fd(300)
            pen.penup()
        
        pen.seth(0)
        for l in range(2):
            pen.goto(-150, 50 - (l * 100))
            pen.pendown()
            pen.fd(300)
            pen.penup()

        for tile in range(9):
            self.lstTiles.append(Tile(tile, self.dCoords[tile]))
    
    def turn(self):
        """Alternate between players. I could have gone with a boolean option, but this way, I can expand number of players someday"""
        self.CurrentPlayer = (self.CurrentPlayer + 1) % 2

    def act(self, tile):
        tile.taken = True
        r = tile.index // 3
        c = tile.index - (3 * r)
        if self.CurrentPlayer == 0:
            tile.token.shape("O.gif")
        else:
            tile.token.shape("X.gif")
        self.state[r][c] = self.symbols[self.CurrentPlayer]
        self.turn()
        if self.IS_TERMINAL(self.state):
            print("GAME OVER!!!")
            turtle.Screen().bye()
        elif self.CurrentPlayer == 0:
            a = self.MINIMAX(self.state, self.CurrentPlayer)[1]
            self.act(self.lstTiles[a])

    def ACTIONS(self, state):
        """This method returns all of the possible actions available in a given state. 
        An Action is represented by the index of the tile's placement in the grid"""
        lstActions = []
        index = 0
        for row in state:
            for col in row:
                if col == self.symbols[2]:
                    lstActions.append(index)
                index += 1
        return lstActions

    def RESULT(self, state, action, player):
        """This method returns the hypothetical state that would result in a certain action being taken by a certain player"""

        # Use the Action (tile index) to calculate row and column position
        r = action // 3
        c = action - (3 * r)

        # Create a copy of the current state
        nextState = []
        for row in range(len(state)):
            nextState.append([])
            for col in range(len(state[0])):
                nextState[row].append(state[row][col])

        # Place the current player's symbol in the indicated spot
        nextState[r][c] = self.symbols[player]     
        return nextState

    def IS_TERMINAL(self, state):
        """This method is used to determine whether or not a given state is terminal"""

        # Check for 3 in a row
        for row in range(3):
            if state[row][0] != self.symbols[2]:
                if state[row][0] == state[row][1] and state[row][0] == state[row][2]:
                    return True
        for col in range(3):
            if state[0][col] != self.symbols[2]:
                if state[0][col] == state[1][col] and state[0][col] == state[2][col]:
                    return True

        # Check for diagonals
        if state[0][0] != self.symbols[2]:   
            if state[0][0] == state[1][1] and state[0][0] == state[2][2]:
                return True
        if state[0][2] != self.symbols[2]:
            if state[0][2] == state[1][1] and state[0][2] == state[2][0]:
                return True
        
        # If it made it here, there are no winners. Lastly we check if there are any open slots left
        return len(self.ACTIONS(state)) == 0

    def UTILITY(self, state):
        """This method calculates the score of a given state.
        If player one (MAX) wins in that state, the score is +1
        If player two (MIN) wins in that state, the score is -1
        If no one wins, the score is 0"""

        # There is probably a better way to check this, but my main focus here was the AI algorithm
        player = self.symbols[0]
        opposing = self.symbols[1]
        for row in range(3):
            if state[row][0] == player and state[row][1] == player and state[row][2] == player:
                return 1
        for col in range(3):
            if state[0][col] == player and state[1][col] == player and state[2][col] == player:
                return 1
        if state[0][0] == player and state[1][1] == player and state[2][2] == player:
            return 1
        if state[0][2] == player and state[1][1] == player and state[2][0] == player:
            return 1
        
        for row in range(3):
            if state[row][0] == opposing and state[row][1] == opposing and state[row][2] == opposing:
                return -1
        for col in range(3):
            if state[0][col] == opposing and state[1][col] == opposing and state[2][col] == opposing:
                return -1
        if state[0][0] == opposing and state[1][1] == opposing and state[2][2] == opposing:
            return -1
        if state[0][2] == opposing and state[1][1] == opposing and state[2][0] == opposing:
            return -1
        
        return 0


    def MINIMAX(self, state, player):
        """This is the 'AI' algorithm that is used to determine the next move. 
        If the AI is player 1, the goal is to reach a state where the UTILITY is highest (+1 for a win, 0 for a tie, but prefereably never a -1)
        If the AI is player 2, the goal is to reach a state where the UTILITY is lowest (-1 for a win, 0 for a tie, but preferably never a +1)"""
        
        # base case. When terminal node is reached
        if self.IS_TERMINAL(state) or len(self.ACTIONS(state)) == 0:
            return (self.UTILITY(state), None)
        
        nextPlayer = (player + 1) % 2 # Used to think of oponent's potential moves
        if player == 0: # Maximise the outcome
            maxUtil = -2 # Since the lowest Utility score it can get is -1, -2 is a suitable starting value
            maxAct = None # We don't know which action got the highest score yet
            for a in self.ACTIONS(state): # Try all possible actions at this state (and recursively beyond this state)
                util = self.MINIMAX(self.RESULT(state, a, player), nextPlayer)[0] # Determine what moves the opponent can take and what the eventual outcome will be
                if util > maxUtil: # Look for the move that led to the best outcome
                    maxUtil = util
                    maxAct = a
            return (maxUtil, maxAct) # return the best move and its score
        else: # Minimise the outcome
            minUtil = 2 # Since 1 is the highest Utility a state can have, 2 is a suitable starting value
            minAct = None
            for a in self.ACTIONS(state): # Try all possible actions at this state
                util = self.MINIMAX(self.RESULT(state, a, player), nextPlayer)[0] # Determine what moves the opponent can make and their eventual outcome
                if util < minUtil: # Keep track of the lowest value and the action that led there
                    minUtil = util
                    minAct = a
            return (minUtil, minAct) # Return the move that yielded the lowest value as well as its score

#=========================START GAME===================================================================================================================================================================================================================================================
game = Game()
a = game.MINIMAX(game.state, game.CurrentPlayer)[1]
game.act(game.lstTiles[a])
turtle.mainloop()