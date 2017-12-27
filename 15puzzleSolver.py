#! usr/bin/env python3
'''
 Author : Dhaval R Niphade
 Description : Solves the 15 puzzle problem with a difference that a single move
                comprises of 3 tiles being slided
 Technique : A-star search
 Heuristic : Manhattan Distance

'''

from collections import defaultdict
from copy import deepcopy
import operator
class Solver:

    # Class variables
    goalState = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
    posMapper = defaultdict(int)
    movesList = [(1,0),(0,1),(-1,0),(0,-1)]

    # Constructor
    def __init__(self,initialState):
        self.initialState = initialState
        for i in range(16):
            Solver.posMapper[i]=initialState[int(i/4)][int(i%4)]

    @classmethod
    def isGoal(cls,state):
        return state == cls.goalState

    # Print the board
    def printBoard(self,currState):
        print("\n".join(str(row) for row in currState))

    # Generate next moves
    def successors(self,currState):
        '''Returns a list of board configurations that are successors to the
        given state'''

        # Stores all the next moves for a given board configuration
        allMoves=[]

        # Find the index of zero so that we can start swapping
        pivot = [(i,j) for i in range(4) for j in range(4) if currState[i][j]==0][0]

        # Build moves
        for moves in Solver.movesList:
            newCoord = tuple(map(operator.add,moves,pivot))
            if newCoord[0] in [0,1,2,3] and newCoord[1] in [0,1,2,3]:
                # Swap 0 and newCoord to create a new board
                newBoard = deepcopy(currState)
                newBoard[pivot[0]][pivot[1]] = newBoard[newCoord[0]][newCoord[1]]
                newBoard[newCoord[0]][newCoord[1]] = 0
                allMoves.append(newBoard)

        return allMoves

    # Calculate the estimated cost to goal
    def heuristic(self,state):
        '''Calculates Manhattan distance of tiles from their correct positions.
        Returns  heuristic value for the entire board'''

        fs=0    # Can be initialized to the current board heuristic
        for row in range(4):
            for col in range(4):
                if state[row][col]==Solver.goalState[row][col]:
                    continue
                for i in range(4):
                    for j in range (4):
                        if Solver.goalState[i][j]==state[row][col]:
                            break
                fs = fs + abs(i-row) + abs(j-col)

        return fs

    def astar(self,initialState):
        if self.isGoal(self.initialState):
            print("You are already at the goal state")
            return True

        priorityQueue = []
        visited = []

        # Tuple of currentState,heuristic evaluation,path so far
        priorityQueue.append((self.initialState,self.heuristic(self.initialState),[self.initialState]))

        while(priorityQueue):

            # Sort the priority queue based on the heuristic
            priorityQueue = sorted(priorityQueue, key = lambda x : x[1])
            nextBoard = priorityQueue.pop(0)
            state,path = nextBoard[0],nextBoard[2]

            # If we haven't seen this state previously
            if(state not in visited):

                # Check if this is the goal State
                if self.isGoal(state):
                    print("Goal found")

                    for boards in path:
                        self.printBoard(boards)
                        print("\n")

                    print("Number of moves = ",len(path)-1)
                    return True

                # Get all successors of the current State and add them to the -
                # queue. Remove from the queue if we already have such a state
                children = self.successors(state)
                for child in children:
                    if child in priorityQueue:
                        priorityQueue.remove(child)
                    if child not in visited:
                        newPath = list(path)
                        newPath.append(child)
                        priorityQueue.append((child,self.heuristic(child),newPath))
                visited.append(state)

        return False

    def solvePuzzle(self):
        print(self.astar(self.initialState))


def main():
    initialState = [[1,2,3,4],[5,6,7,8],[9,10,11,0],[13,14,15,12]]
    s = Solver(initialState)
    s.solvePuzzle()
    # print(s.isGoal(initialState))
    # print(s.heuristic(initialState))


    print("Finished solving puzzle")
    return

if __name__ == '__main__':
    main()
