import random

# this is the lowercase alphabet and the space character
lstChars = list(range(97, 123))
lstChars.append(32)

# this list will hold each generation's population
lstPopulation = []

# this is the target phrase
targetPhrase = "to be or not to be that is the question"

# mess around with this value to try and speed up or slow down the evolution
mutationRate = 0.03

# this method creates the initial population with completely random strings
def setup(popSize, phraseLength):
    global lstPopulation
    for p in range(popSize):
        strPhrase = ""
        for l in range(phraseLength):
            strPhrase += chr(random.choice(lstChars))
        lstPopulation.append(strPhrase)

# This function evaluates the fittness by seeing how many letters of a member mathces the target phrase
def calcFitness(strPhrase):
    global targetPhrase
    score = 0
    for c in range(len(targetPhrase)):
        if strPhrase[c] == targetPhrase[c]:
            score += 1
    return score

# Breed two members of the previous generation to create a better and stromger child
def crossover(p1, p2):
    newMember = ""
    # basically 50/50 chance to take a particular gene from either parent
    for i in range(len(p1)):
        if random.randint(0, 100) % 2 == 0:
            newMember += p1[i]
        else:
            newMember += p2[i]
    return newMember

# Introduce genetic mutations to increase variation in the gene pool
def mutate(member):
    global mutationRate
    global lstChars
    strRet = ""
    # based on the mutation rate, there is a chance that one of the member's genes will mutate to introduce new possibilities
    for i in range(len(member)):
        if random.random() < mutationRate:
            strRet += chr(random.choice(lstChars))
        else:
            strRet += member[i]
    return strRet
    

def run():
    global lstPopulation
    global targetPhrase
    popSize = 1000
    setup(popSize, len(targetPhrase))
    generation = 0

    # loop until we find a perfect candidate
    while targetPhrase not in lstPopulation:
        lstScores = []

        # determine the fitness of each member of the population
        for member in lstPopulation:
            lstScores.append((calcFitness(member), member))

        # order the population by fitness
        lstScores.sort(key= lambda p: p[0])
        lstScores.reverse()

        print(f"Generation {generation} Best member: {lstScores[0][1]}    Score: {lstScores[0][0]}")

        # generate the new population
        lstPopulation = []
        member = 0

        # keep the best performer in the previous population to prevent mutation from screwing up our chances of finding a solution if it came about from one member
        lstPopulation.append(lstScores[0][1])
        while len(lstPopulation) < popSize - 1:
            lstPopulation.append(mutate(crossover(lstScores[member][1], lstScores[member + 1][1])))
            member += 1

        generation += 1
    if targetPhrase in lstPopulation:
        print(f"Generation {generation}: {lstPopulation[lstPopulation.index(targetPhrase)]}")

if __name__ == "__main__":
    run()