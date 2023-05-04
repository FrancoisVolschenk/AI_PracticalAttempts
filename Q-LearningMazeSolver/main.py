import random
import turtle

rows = 20
cols = 40
base_x = ((cols * 20) / -2) + 10
base_y = ((rows * 20) / 2) - 10

class Table:
    def __init__(self, tplDimensions, tplRange = (64,64)):
        self.rows, self.cols = tplDimensions
        self.space = [[] for _ in range(self.rows)]

class RewardTable(Table):
    def __init__(self, tplDimensions, tplUpperRange = (64,64)):
        super().__init__(tplDimensions)
        for r in range(self.rows):
            for c in range(self.cols):
                if r == 0 or c == 0 or r == self.rows - 1 or c == self.rows - 1:
                    self.space[r].append(-50)
                else:
                    self.space[r].append(-1.0)

class QTable(Table):
    def __init__(self, tplDimensions, tplUpperRange, lstActions):
        super().__init__(tplDimensions)
        self.actions = lstActions
        for r in range(self.rows):
            for _ in range(self.cols):
                dictQ = {}
                for a in self.actions:
                    dictQ[a] = 0.0
                self.space[r].append(dictQ)

    def getBestQ(self, tplCoord):
        qs = self.space[tplCoord[0]][tplCoord[1]]
        qbest = list(qs.values())[0]
        abest = list(qs.keys())[0]

        for a, q in qs.items():
            if q > qbest:
                qbest = q
                abest = a
        return (abest, qbest)

class Agent:
    def __init__(self, epsilon, gamma, alpha, env):
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.env = env
        self.location = env.startLoc
        self.actions = ['up','down','left','right']
        self.qtable = QTable((env.rewards.rows, env.rewards.cols), (128, 128), self.actions)
        self.path = []
        self.token = turtle.Turtle()
        self.token.penup()
        self.token.speed("slow")
        self.token.shape("turtle")
        self.token.color("green")
        self.token.goto(base_x + (self.location[1] * 20), base_y - (self.location[0] * 20))

    def sense(self):
        return self.qtable.space[self.location[0]][self.location[1]]
    
    def choose(self):
        qs = self.sense()
        if random.random() < self.epsilon:
            abest, _ = self.qtable.getBestQ(self.location)
            return abest
        else:
            return random.choice(list(qs.keys()))
        
    def inference(self):
        self.epsilon = 1.0
        self.path = []

        while not self.env.isTerminal(self.location):
            a = self.qtable.getBestQ(self.location)[0]
            self.act(a)
            self.token.goto(base_x + (self.location[1] * 20), base_y - (self.location[0] * 20))
            self.path.append(self.location)

        self.epsilon = 0.9

    def act(self, action):
        tr, tc = self.location
        if action == "up":
            tr -= 1
            # self.token.seth(90)
        elif action == "down":
            tr += 1
            # self.token.seth(270)
        elif action == 'left':
            tc -= 1
            # self.token.seth(180)
        elif action == "right":
            tc += 1
            # self.token.seth(0)
        if self.env.isInWorld((tr, tc)):
            self.location = (tr, tc)
        

    def train(self):
        locOriginal = self.location

        for e in range(self.env.episodes):
            self.location = random.choice(self.env.openLocations())
            while not self.env.isTerminal(self.location):
                locStart = self.location
                a = self.choose()
                qStart = self.qtable.space[locStart[0]][locStart[1]][a]
                self.act(a)
                reward = self.env.rewards.space[self.location[0]][self.location[1]]
                _, qBest = self.qtable.getBestQ(self.location)
                td = reward + (self.gamma * qBest) - qStart
                qNew = qStart + td * self.alpha
                self.qtable.space[locStart[0]][locStart[1]][a] = qNew
            self.location = locOriginal
            # self.token.goto(base_x + (self.location[1] * 20), base_y - (self.location[0] * 20))


class Environment:
    def __init__(self, intRows, intCols, intEpisodes):
        self.episodes = intEpisodes
        self.rewards = RewardTable((intRows, intCols))
        self.startLoc = (1,1)
        self.agent = Agent(0.9, 0.9, 0.9, self)
        self.map = [["X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
                    ["X", "S", "X", "X", "X", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
                    ["X", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "X", "X"],
                    ["X", "O", "X", "X", "X", "O", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
                    ["X", "O", "X", "X", "X", "O", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
                    ["X", "O", "X", "X", "X", "O", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
                    ["X", "O", "X", "X", "X", "O", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
                    ["X", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "X", "X"],
                    ["X", "O", "X", "X", "X", "X", "X", "X", "O", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
                    ["X", "O", "X", "X", "X", "X", "X", "X", "O", "O", "O", "O", "O", "O", "O", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
                    ["X", "O", "X", "X", "X", "X", "X", "X", "O", "X", "X", "X", "X", "X", "O", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
                    ["X", "O", "X", "X", "X", "X", "X", "X", "O", "X", "X", "X", "X", "X", "O", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
                    ["X", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "X", "X"],
                    ["X", "O", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "O", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
                    ["X", "O", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "O", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
                    ["X", "O", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "O", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
                    ["X", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "X", "X"],
                    ["X", "O", "X", "X", "X", "O", "X", "X", "X", "X", "X", "X", "X", "X", "O", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],
                    ["X", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "O", "#", "X"],
                    ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"],]
        
    def isInWorld(self, tplTargetLoc):
        if tplTargetLoc[0] < 0 or tplTargetLoc[0] >= self.rewards.rows:
            return False
        if tplTargetLoc[1] < 0 or tplTargetLoc[1] >= self.rewards.cols:
            return False
        return True

    def isTerminal(self, tplCoord):
        return self.rewards.space[tplCoord[0]][tplCoord[1]] != -1
    
    def run(self):
        screen = turtle.setup((cols * 20) + 20, (rows * 20) + 20)
        turtle.Screen().bgcolor("black")

        pen = turtle.Turtle()
        pen.penup()
        pen.speed(0)
        pen.shape("square")
        pen.seth(0)
        pen.hideturtle()
        pen.goto(base_x, base_y)
        for r in range(self.rewards.rows - 1):
            pen.setx(base_x)
            for c in range(self.rewards.cols -1):
                if self.map[r][c] == "X":
                    pen.color("red")
                    self.rewards.space[r][c] = -50
                elif self.map[r][c] == "O":
                    pen.color("white")
                    self.rewards.space[r][c] = -1.0
                elif self.map[r][c] == "S":
                    pen.color("green")
                    self.rewards.space[r][c] = -1.0
                elif self.map[r][c] == "#":
                    pen.color("grey")
                    self.rewards.space[r][c] = 100
                pen.stamp()
                pen.fd(20)
            pen.sety(pen.ycor() - 20)

        self.agent.train()

    def clearGoal(self):
        for r in range(self.rewards.rows):
            for c in range(self.rewards.cols):
                if self.rewards.space[r][c] == 100:
                    self.rewards.space[r][c] = -1.0

    def openLocations(self):
        lstOpen = []
        for r in range(self.rewards.rows):
            for c in range(self.rewards.cols):
                if self.rewards.space[r][c] == -1:
                    lstOpen.append((r, c))
        return lstOpen


env = Environment(rows, cols, 100000)
env.run()
runInfer = input("Training complete, Would you like to run the inference? (y/n):\n")
if runInfer == "y":
    env.agent.inference()

turtle.mainloop()

        
