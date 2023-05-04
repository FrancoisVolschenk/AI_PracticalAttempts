import math
import random
import turtle

# These are just some pre set colours that can be used for displaying a cluster
lstCOLORS = ["red", "green", "blue", "brown", "yellow", "orange", "pink"]

class Point:
    """This class represents a single point, 
        along with functionality to link it to a centroid
          and have it take on the colour of that cluster"""
    def __init__(self, pos):
        self.pos = pos
        self.token = turtle.Turtle()
        self.token.shapesize(stretch_len=0.2, stretch_wid=0.2)
        self.token.penup()
        self.token.speed(0)
        self.token.color("grey")
        self.token.shape("circle")
        self.token.goto(pos[0], pos[1])
        self.kPoint = None

    def showKPoint(self):
        """This method makes the current point take on the properties of the centroid of its current cluster"""
        col = self.kPoint.token.color()[0]
        self.token.color(col)

class K_Cluster:
    """This class represents the functionality of the K-Means clustering method"""
    def __init__(self, nPoints, kVal, numCorrections):
        self.kVal = kVal
        self.lstDataPoints = []
        self.kLists = []
        self.groups = []
        self.WIDTH = 800
        self.HEIGHT = 500
        self.lowerX = self.WIDTH / -2
        self.upperX = self.WIDTH / 2
        self.lowerY = self.HEIGHT / -2
        self.upperY = self.HEIGHT / 2
        self.screen = turtle.setup(self.WIDTH, self.HEIGHT)
        turtle.Screen().bgcolor("black")
        turtle.Screen().title("K-Means Clustering vizualization")
        self.drawAxis()
        self.fillRandom(nPoints)
        self.plotKPoints()

        # Run a few iterations of the correction algorithm
        for c in range(numCorrections):
            self.checkNearestNeighbors()
            self.findCentroids()
        turtle.mainloop()

    def drawAxis(self):
        """This method simply draws the axis of a Cartesian plane"""
        pen = turtle.Turtle()
        pen.penup()
        pen.speed(0)
        pen.hideturtle()
        pen.color("white")
        pen.goto(0, self.HEIGHT / 2)
        pen.seth(270)
        pen.pendown()
        pen.fd(self.HEIGHT)
        pen.penup()
        pen.goto(self.WIDTH / - 2, 0)
        pen.seth(0)
        pen.pendown()
        pen.fd(self.WIDTH)

    def fillRandom(self, nPoints):
        """This method fills the list of datapoints with randomly generated points"""
        for p in range(nPoints):
            pos = [random.randint(self.lowerX, self.upperX), random.randint(self.lowerY, self.upperY)]
            self.lstDataPoints.append(Point(pos))

    def plotKPoints(self):
        """This method plots the original K centroids"""
        self.kLists = []
        for k in range(self.kVal):
            pos = [random.randint(self.lowerX, self.upperX), random.randint(self.lowerY, self.upperY)]

            kp = Point(pos)
            kp.token.color(lstCOLORS[len(self.kLists)])
            kp.token.shape("triangle")
            kp.token.speed('slow')
            self.kLists.append(kp)

    def clearGroups(self):
        """Empty the list of cluster groupings"""
        self.groups = []
        for k in range(self.kVal):
            self.groups.append([])

    def checkNearestNeighbors(self):
        """For every data point, find the closest centroid"""
        self.clearGroups()
        for point in self.lstDataPoints:
            nearest = self.calcDist(point.pos, self.kLists[0].pos)
            kpoint = self.kLists[0]
            lst = 0
            for k in range(self.kVal):
                dist = self.calcDist(point.pos, self.kLists[k].pos)
                if dist < nearest:
                    nearest = dist
                    kpoint = self.kLists[k]
                    lst = k
            self.groups[lst].append(point)
            point.kPoint = kpoint
            point.showKPoint()

    def findCentroids(self):
        """Readjust the placement of the centroids to be more central to the clusters"""
        for group in range(len(self.groups)):
            pos = [0, 0]
            for point in self.groups[group]:
                pos[0] += point.pos[0]
                pos[1] += point.pos[1]
            pos = [pos[0]/ len(self.groups[group]) , pos[1]/ len(self.groups[group])]
            self.kLists[group].pos = pos
            self.kLists[group].token.goto(pos[0], pos[1])

    def calcDist(self, p1, p2):
        """Simple Euclidean distance formula"""
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

if __name__ == "__main__":
    K_Cluster(300, 5, 3)