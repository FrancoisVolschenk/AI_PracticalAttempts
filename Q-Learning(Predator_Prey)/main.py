from math import sqrt # for distance calculations
import random         # for miscellaneous purposes ;)
import turtle         # for the visualization

class QTable:
    '''This class represents the mechanism by which the agent learns.
    It keeps track of each possible state (8 directions that the food can be reletive to the agent)
        and each action in that state (it stores a score for how good that action is at that state)'''
    def __init__(self, lstActions):
        self.actions = lstActions
        self.space = []
        for food_dir in range(0, 9):
            dictQ = dict()
            for a in lstActions:
                # all actions are available in all states, and start off equally undesirable
                dictQ[a] = 0.0
            self.space.append(dictQ)


    def getBestQ(self, tplState):
        # given a state, get the action that is most desirable based on the score it has
        qVals = self.space[tplState]
        qbest = list(qVals.values())[0]
        abest = list(qVals.keys())[0]

        for a, q in qVals.items():
            if q > qbest:
                qbest = q
                abest = a

        return (abest, qbest)
    
class Agent:
    '''The agent learns how to navigate its environment via the Q-Learning method'''
    def __init__(self, epsilon, gamma, alpha, env):
        self.epsilon = epsilon # The randomness factor to balance exploration vs exploitation
        self.gamma = gamma     # the discount rate used for updating Q-Values 
        self.alpha = alpha     # The learning rate used for updating Q-Values
        self.env = env         # The agent's own internal representation of the environment
        self.location = random.choice(env.openLocations())
        self.actions = ['u','l','d','r']
        self.qtable = QTable(self.actions)
        self.energy = 100
        self.reward = 0
        self.heading = 0 # Direction used for visualization
        self.consecutive = 0

        # These two attributes are used to calculate reward
        self.current_dist_food = 0
        self.prev_dist_food = 0
        

    def calcDist(self, locaction):
        # Euclidean distance using the grid coordinates
        return sqrt((self.location[0] - locaction[0]) ** 2 + (self.location[1] - locaction[1]) ** 2)
    
    def getDir(self, location):
        # Get a numerical value for the direction of the food
        # TODO: think up a more mathematial way to get this
        if self.location[0] > location[0] and self.location[1] == location[1]:
            return 0
        elif self.location[0] > location[0] and self.location[1] < location[1]:
            return 1
        elif self.location[0] == location[0] and self.location[1] < location[1]:
            return 2
        elif self.location[0] < location[0] and self.location[1] < location[1]:
            return 3
        elif self.location[0] < location[0] and self.location[1] == location[1]:
            return 4
        elif self.location[0] < location[0] and self.location[1] > location[1]:
            return 5
        elif self.location[0] == location[0] and self.location[1] > location[1]:
            return 6
        elif self.location[0] > location[0] and self.location[1] > location[1]:
            return 7
        elif self.location[0] == location[0] and self.location[1] == location[1]:
            return 8
        
    def getState(self):
        # get the state of the world
        # This method can be expanded to give the agent more info about the env
        f = self.getDir(self.env.food.pos)
        return f
    
    def sense(self):
        # This method allows the agent to "consider all options at the current state"
        return self.qtable.space[self.getState()]
    
    def choose(self):
        # This method allows the agent to select an action
        qVals = self.sense()
        action = None
        # Use epsilon greedy to introduce random actions that may lead to better tradeoffs
        if random.random() < self.epsilon: 
            abest, _ = self.qtable.getBestQ(self.getState())
            action = abest
        else:
            action = random.choice(list(qVals.keys()))
        # Fade out epsilon to reduce the randomness as the agent gains more experience
        if self.epsilon != 1.0:
            self.epsilon += 0.001
        return action
        
    def inference(self):
        # Run this once the agent has been trained to see what it has learned
        ep = self.epsilon
        self.epsilon = 1.0 # ensure that no random actions are chosen
        self.energy = 50
        self.consecutive = 0
        while not self.env.isTerminal():
            a = self.qtable.getBestQ(self.getState())[0]
            self.act(a)
            if self.location == self.env.food.pos:
                self.env.food.respawn()
                self.energy= 50
                self.consecutive += 1
            self.env.update(0)

        self.epsilon = ep

    def act(self, a):
        # Actually perform the selected action
        tr, tc = self.location
        if a == 'u':
            tr -= 1
            self.heading = 90
        elif a == 'l':
            tc -= 1
            self.heading = 180
        elif a == 'd':
            tr += 1
            self.heading = 270
        elif a == 'r':
            tc += 1
            self.heading = 0

        self.location = (tr, tc)
        self.energy -= 1

    def train(self):
        # this method runs simulations of the environment, allowing the agent to learn about the actions and consequences
        locOriginal = self.location
        for ep in range(self.env.episodes):
            # spawn in a random open location
            self.location = random.choice(self.env.openLocations())
            self.consecutive = 0 # keep track of how many food items the agent has eaten

            # run until the agent dies
            while not self.env.isTerminal():
                a = self.choose()
                f = self.getState()

                # use the bellman equation to update Q-Values based on the actions performed
                qStart = self.qtable.space[f][a] # look at the current policy
                self.prev_dist_food = self.current_dist_food # save my current distance from the food
                self.act(a) # perform the selected action
                self.current_dist_food = self.calcDist(self.env.food.pos) # see how far away the food is now
                self.reward = 0 
                self.env.calcReward() # calculate the reward
                _, qBest = self.qtable.getBestQ(self.getState()) # calculate the best reward that can be obtained from this new state
                td = self.reward + (self.gamma * qBest) - qStart 
                qNew = self.reward + td * self.alpha # calculate the new Q-Value for the chosen action at the previous state
                self.qtable.space[f][a] = qNew # Update the policy

                # self.env.food.move() # this was just a fun idea to see if the agent could learn to chase a moving target. But the movement of the food is a bit buggy
                self.env.update(ep) # This is a visualization step. If you do not wish to visualize the training, comment this out

                # if the agent has achieved the desired threshold, stop training
                if self.consecutive >= env.threshold:
                    break
            # reset the agent to the starting state for next round of training
            self.location = locOriginal
            self.energy = 50

            # if the agent has achieved the desired threshold, stop training
            if self.consecutive >= env.threshold:
                break

class food:
    '''This class represents the food.
    Technically it could have just been a tuple in the Environment class, but I wanted to make it move to see what happens'''
    def __init__(self, env):
        self.env = env
        self.pos = (random.randint(1, env.rows - 2), random.randint(1, env.cols - 2))

    def respawn(self):
        self.pos = (random.randint(1, self.env.rows - 2), random.randint(1, self.env.cols - 2))

    def move(self):
        direction = random.choice(['u','d','l','r'])
        tr, tc = self.pos

        if direction == 'u':
            tr -= 1
        elif direction == 'd':
            tr += 1
        elif direction == 'l':
            tc -= 1
        elif direction == 'r':
            tc += 1

        if self.env.isInWorld((tr, tc)):
            self.pos = (tr, tc)

class Environment:
    """This class represents the environment of the agent"""
    def __init__(self, intRows, intCols, intEpisodes, threshold):
        self.episodes = intEpisodes # number of training rounds
        self.threshold = threshold # how many eats indicates that the agent has learned enough?

        # Size of world
        self.rows = intRows
        self.cols = intCols

        self.food = food(self)
        self.agent = Agent(0.9, 0.9, 0.5, self) # These values can be tweaked to fine tune the learning
        self.maxConsecutive = 0 # Highest number of consecutive eats

        # tools for visualization
        self.agent_token = None
        self.food_token = None
        self.score_token = None
        self.base_x = ((self.cols * 20) // -2) + 10
        self.base_y = ((self.rows * 20) // 2) - 20 
        

    def update(self, episode):
        """This method is for visualization"""
        if self.agent_token is None:
            self.agent_token = turtle.Turtle()
            self.agent_token.penup()
            self.agent_token.speed(0)
            self.agent_token.shape("turtle")
            self.agent_token.color("green")
        self.agent_token.seth(self.agent.heading)
        self.agent_token.goto(self.base_x + (self.agent.location[1] * 20), self.base_y - (self.agent.location[0] * 20))
        
        # I change the color of every second agent, so that you can visually see when a new agent is training
        if episode % 2 == 0:
            self.agent_token.color("green")
        else:
            self.agent_token.color("red")

        if self.food_token is None:
            self.food_token = turtle.Turtle()
            self.food_token.shape("circle")
            self.food_token.color("blue")
            self.food_token.penup()
            self.food_token.speed(0)
        self.food_token.goto(self.base_x + (self.food.pos[1] * 20), self.base_y - (self.food.pos[0] * 20))\
        
        if self.score_token is None:
            self.score_token = turtle.Turtle()
            self.score_token.hideturtle()
            self.score_token.penup()
            self.score_token.speed(0)
            self.score_token.color("blue")
            self.score_token.goto(self.base_x + 10, self.base_y - 5)
        self.score_token.clear()
        self.score_token.write(f"Training Episode: {episode} | Consecutive eats: {self.agent.consecutive}")

        
    def isInWorld(self, pos):
        return not (pos[0] < 0 or pos[0] >= self.rows) or (pos[1] < 0 or pos[1] >= self.cols)

    def isTerminal(self):
        """Has the agent run off the world, or run out of energy?
        Or has the agent achieved the threshold?"""
        bTerminal = False
        if self.agent.location[0] <= 0 or self.agent.location[0] >= self.rows - 1:
            bTerminal = True
        if self.agent.location[1] <= 0 or self.agent.location[1] >= self.cols - 1:
            bTerminal = True
        if self.agent.energy <= 0:
            bTerminal = True

        if bTerminal:
            if self.agent.consecutive > self.maxConsecutive:
                self.maxConsecutive = self.agent.consecutive
        return bTerminal
        
    def openLocations(self):
        lstOpen = []
        for r in range(1, self.rows):
            for c in range(1, self.cols):
                if (r, c) != self.food.pos:
                    lstOpen.append((r, c))
        return lstOpen
    
    def calcReward(self):
        """Very important. This is what makes the agent learn what is wrong and what is right"""
        self.agent.reward = -1 - (50 - self.agent.energy) # Calculate an initial score based on how much energy the agent has left (this discourages the girating behaviour)

        # If the agent has fallen off the world, punish it
        if self.agent.location[0] == 0 or self.agent.location[0] >= self.rows - 1 or self.agent.location[1] == 0 or self.agent.location[1] >= self.cols - 1:
            self.agent.reward = -100
        if self.agent.location == self.food.pos: # If the agent has found food, reward it
            self.agent.energy = 50
            self.food.respawn()
            self.agent.reward = 100
            self.agent.consecutive += 1
    
    def run(self):
        """Start training and then ask the uer f they want to run the policy"""

        # Setup the screen 
        self.screen = turtle.setup((self.cols * 20) + 10, (self.rows * 20) + 30)
        turtle.Screen().bgcolor("black")

        # Draw the bounds of the world
        pen = turtle.Turtle()
        pen.shape("square")
        pen.penup()
        pen.speed(0)
        pen.hideturtle()
        pen.color("red")
        pen.goto(self.base_x, self.base_y)
        pen.seth(0)
        for border in range(4):
            n_cells = self.cols - 1 if border % 2 == 0 else self.rows - 1
            for i in range(n_cells):
                pen.stamp()
                pen.fd(20)
            pen.right(90)
        self.update(0)
        self.agent.train()    

if __name__ == "__main__":
    width = int(input("Enter the width of the world (num cols): "))
    height = int(input("Enter the height of the world (num rows): "))
    eps = int(input("Enter the number of training episodes: "))
    threshold = int(input("Enter the threshold for training completeness: "))
    env = Environment(height, width, eps, threshold)
    env.run()
    print(f"The best agent achieved {env.maxConsecutive} eats")
    choice = input("The training has completed. Would you like to run inference? (y/n):\n")
    if choice == "y":
        env.agent.inference()

        # Enter an infinite loop to prevent the screen from closing immediately
        # This could be done in many different ways that are vastly superiour, but I chose the suboptimal solution because epsilon made me do it
        turtle.mainloop()