#CREDITS
# modified https://www.askpython.com/python/examples/tic-tac-toe-using-python for the outline of the tictactoe game itself, mainly the way the wins were displayed early on
# code still included by no display any more some logic for how to store the players move is still included
# Used Visual Studio editor to help clean up certain sytax errors
######
#general notes
#   what makes a genetic algorithm
#       -reproduction
#       -mutation
#       -selection
#
#GAME PLAN(PsuedoCode):
#   Populate initial Generation
#   Have every member of the generation play 2 games with each other
#   rate them with a fitness score as they play
#   Take the top 50% of members with the highest scores and make them the parents of the next gen
#   Create Offspring
#   Mutate some of the offspring
#   Have the new generation play games together(back to step 2)
#   Repeat for specifed number off generations
import random


class TicTacToe:
    def __init__(self):
        self.values = [' ' for _ in range(9)]
        self.playerPos = {'X': [], 'O': []}
        self.currentPlayer = 'X'


    def printGameBoard(self):
        values = self.values
        print("\n")
        print("\t     |     |")
        print("\t  {}  |  {}  |  {}".format(values[0], values[1], values[2]))
        print('\t_____|_____|_____')
        print("\t     |     |")
        print("\t  {}  |  {}  |  {}".format(values[3], values[4], values[5]))
        print('\t_____|_____|_____')
        print("\t     |     |")
        print("\t  {}  |  {}  |  {}".format(values[6], values[7], values[8]))
        print("\t     |     |")
        print("\n")


    def checkForWin(self):
        solutions = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
        for solution in solutions:
            if all(pos in self.playerPos[self.currentPlayer] for pos in solution):
                return True
        return False


    def checkForDraw(self):
        return len(self.playerPos['X']) + len(self.playerPos['O']) == 9


    def reset(self):
        self.values = [' ' for _ in range(9)]
        self.playerPos = {'X': [], 'O': []}
        self.currentPlayer = 'X'


    def validMove(self, move):
        if self.values[move - 1] != ' ':
            return False
        self.values[move - 1] = self.currentPlayer
        self.playerPos[self.currentPlayer].append(move)
        return True


    def swapPlayer(self):
        self.currentPlayer = 'O' if self.currentPlayer == 'X' else 'X'


    def findSpecialMove(self, moveType):
        solutions = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
        opponent = 'O' if self.currentPlayer == 'X' else 'X'
        for solution in solutions:
            if moveType == 'blockWin':
                if sum(1 for pos in solution if pos in self.playerPos[opponent]) == 2:


                    for pos in solution:
                        if pos not in self.playerPos['X'] and pos not in self.playerPos['O']:
                            return pos
            elif moveType == 'winMove':
                if sum(1 for pos in solution if pos in self.playerPos[self.currentPlayer]) == 2:
                    for pos in solution:
                        if pos not in self.playerPos['X'] and pos not in self.playerPos['O']:
                            return pos
        return None


    def oneGame(self, chromosome1, chromosome2, playerX, playerO):
        self.reset()
        moveIndices = {'X': 0, 'O': 0}
        movePriority = {'X': chromosome1, 'O': chromosome2}
       
        #moves tracker for point given for draw
        movesMade = 0  
       
        while True:
            #stalemate/ Draw logic
            if moveIndices[self.currentPlayer] >= len(movePriority[self.currentPlayer]):
                print("Ran out of moves for player,",{self.currentPlayer})
                return 'D', movesMade  
           
            move = movePriority[self.currentPlayer][moveIndices[self.currentPlayer]]
           
            if move in ['blockWin', 'winMove']:
                move = self.findSpecialMove(move)
                if move is None:
                    moveIndices[self.currentPlayer] += 1
                    continue
            else:
                moveIndices[self.currentPlayer] += 1


            if not self.validMove(move):
                continue


            movesMade += 1


            if self.checkForWin():
                # self.printGameBoard()  # see game boards
                winner = playerX if self.currentPlayer == 'X' else playerO
                # print(f"{winner} has won the game!!")  #  see win messages
                return winner, movesMade


            if self.checkForDraw():
                # self.printGameBoard()  # see game boards
                # print("Draw")  #  see draw messages
                return 'D', movesMade


            self.swapPlayer()


def makeChromo():
    chromoLength = 10


    newArr = []
    shufArr = []
    i = 1
    j = 1
    while i < chromoLength:
        newArr.append(i)
        i += 1
   
    while j < chromoLength:
        randomInt = random.randint(0, len(newArr) - 1)
        shufArr.append(newArr[randomInt])
        newArr.pop(randomInt)
        j += 1
   
    return shufArr


class ChromosomeManager:
    def __init__(self):
        self.population = []


    def initializePopulation(self, size):
        self.population = [makeChromo() for _ in range(size)]


    # mergesort works, but i wonder if it could be more efficient, look back on notes for quicksort
    # based on class example but pivot is the middle
    def partition(self, array, left, right):
        mid = (left + right) // 2
        pivot = array[mid]
        array[mid], array[right] = array[right], array[mid]  
        pivot_index = right
        right -= 1
       
        while left <= right:
            while left <= right and array[left][1] >= pivot[1]:  
                left += 1
            while left <= right and array[right][1] <= pivot[1]:  
                right -= 1
            if left < right:
                array[left], array[right] = array[right], array[left]


        array[left], array[pivot_index] = array[pivot_index], array[left]
        return left


    def quicksort(self, array, left=0, right=None):
        if right is None:
            right = len(array) - 1
        if left >= right:
            return


        pivot = self.partition(array, left, right)
        self.quicksort(array, left, pivot - 1)
        self.quicksort(array, pivot + 1, right)


    def selectParents(self, fitnessScores):
        #NEED a way to tie pop to fitscore, look into zip
        combined = list(zip(self.population, fitnessScores))


       
        self.quicksort(combined)


        # top half of the sorted population
        selectedParents = [chromo for chromo, score in combined[:len(self.population)//2]]


        return selectedParents
   
    def mutateChromosome(self, chromosome):
        halfChrom = len(chromosome) // 2
       
        # 1% mutation to add 'winMove' or 'blockWin'
        if random.random() < 0.05:
            #print("randomA mutation")
            specialMove = random.choice(['winMove', 'blockWin'])
            if specialMove not in chromosome:
                chromosome.append(specialMove)


        # 15% chance to randomly swap a number of priority items
        if random.random() < 0.15:
            #print("randomB mutation")
            numSwaps = random.randint(1, len(chromosome) // 2)
            for _ in range(numSwaps):
                i, j = random.sample(range(len(chromosome)), 2)
                chromosome[i], chromosome[j] = chromosome[j], chromosome[i]


        # 30% chance to shuffle the back half of the chromosome
        if random.random() < 0.5:
            #print("randomC mutation")
            partToShuffle = chromosome[halfChrom:]
            random.shuffle(partToShuffle)
            chromosome = chromosome[:halfChrom] + partToShuffle


        # 5% chance to shuffle the first half of the chromosome
        if random.random() < 0.2:
            #print("randomD mutation")
            partToShuffle = chromosome[:halfChrom]
            random.shuffle(partToShuffle)
            chromosome = partToShuffle + chromosome[halfChrom:]


        return chromosome


    def createOffspring(self, parent):
        directChild = parent[:]
        mutatedChild = self.mutateChromosome(parent[:])
        return [directChild, mutatedChild]
   
    def evolvePopulation(self, selectedParents):
        nextGeneration = []
        for parent in selectedParents:
            offspring = self.createOffspring(parent)
            nextGeneration.extend(offspring)




        self.population = nextGeneration


def runGames():
    game = TicTacToe()
    manager = ChromosomeManager()
    populationSize = 6
    generations = 4


    manager.initializePopulation(populationSize)


    initialPopulation = manager.population[:]


    # Print initial population
    print("Initial Population:")
    for chromo in initialPopulation:
        print(chromo)


    for generation in range(generations):
        print("\n Generation", generation + 1)


        fitnessScores = [0] * populationSize  


        for i in range(populationSize):
            for j in range(i + 1, populationSize):
                chromosome1 = manager.population[i]
                chromosome2 = manager.population[j]


                for _ in range(2):
                    winner, movesMade = game.oneGame(chromosome1, chromosome2, "player1", "player2")
                    if winner == "player1":
                        fitnessScores[i] += 10  
                        fitnessScores[i] += max(0, 10 - movesMade)  
                    elif winner == "player2":
                        fitnessScores[j] += 10  
                        fitnessScores[j] += max(0, 10 - movesMade)  
                    else:
                        fitnessScores[i] -= 5  
                        fitnessScores[j] -= 5  


                    chromosome1, chromosome2 = chromosome2, chromosome1


                    if winner == "player2" and chromosome1 == manager.population[j]:
                        fitnessScores[j] += 5


        for chromo, score in zip(manager.population, fitnessScores):
            print("Chromosome:", chromo, "Score:", score)


        averageFitness = sum(fitnessScores) / len(fitnessScores)
        print("Average Fitness:", averageFitness)


        selectedParents = manager.selectParents(fitnessScores)


        print("\nSelected Parents:")
        for parent in selectedParents:
            print(parent)


        manager.evolvePopulation(selectedParents)


        print("\nNext Generation:")
        for offspring in manager.population:
            print(offspring)


    # Final Generation vs Initial Generation
    finalPopulation = manager.population[:]
    print("\nFinal Generation vs Initial Generation Matches")
    finalFitnessScores = [0] * len(finalPopulation)


    for i in range(len(finalPopulation)):
        for j in range(len(initialPopulation)):
            chromosome1 = finalPopulation[i]
            chromosome2 = initialPopulation[j]


            for _ in range(2):
                winner, movesMade = game.oneGame(chromosome1, chromosome2, "finalPlayer", "initialPlayer")
                if winner == "finalPlayer":
                    finalFitnessScores[i] += 10
                    finalFitnessScores[i] += max(0, 10 - movesMade)
                elif winner == "initialPlayer":
                    finalFitnessScores[i] -= 5
                else:
                    finalFitnessScores[i] += 1


                chromosome1, chromosome2 = chromosome2, chromosome1


    for chromo, score in zip(finalPopulation, finalFitnessScores):
        print("Chromosome:", chromo)
    averageFinalFitness = sum(finalFitnessScores) / len(finalFitnessScores)
    print("Average Fitness:", averageFinalFitness)


if __name__ == "__main__":
    runGames()