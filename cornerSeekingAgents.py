from game import Directions
from game import Agent
from game import Actions
import game
import util, time, search
import csv
import sys

# CornerSeekingAgent is a class that inherits from Agent
# It is used to find the shortest path to all four corners of the maze
class CornerSeekingAgent(Agent):

    # Constructor
    # fn: the search function to be used
    # dfs is the default search function
    def __init__(self, fn='dfs'):
        
        searchFn = getattr(search, fn)
        self.searchFn = searchFn
        self.allCorners = False
        self.totaltime = 0
    
    # registerInitialState is called when the agent is initialized
    # state: the initial state of the game
    def registerInitialState(self, state):

        # starttime is used to keep track of the time taken to find the path
        # problem: instance of CornersProblem
        self.starttime = time.time()
        problem = CornersProblem(state, self.starttime)
        self.actions = self.searchFn(problem)
        self.turns = self.calculateTurns(self.actions)
        totalCost = problem.getCostOfActions(self.actions)
    
    # getAction is called every time the agent is asked to make a move
    # state: the current state of the game
    def getAction(self, state):
        
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions): return self.actions[i]
        else:
            if not self.allCorners:
                self.totaltime = time.time() - self.starttime
                self.saveData(state)
                self.allCorners = True
            return Directions.STOP

    def final(self, state):
        self.saveData(state)
        
    def saveData(self, state):
        filename = 'corners.csv'
        args = sys.argv
        human = False
        for a in args:
            if 'human' in a:
                human = True
        map = 'human' if human else 'generated'     
        walls = state.getWalls()
        with open(filename, 'a') as file:
            writer = csv.writer(file)
            writer.writerow([time.time() - self.starttime, len(self.actions), self.turns, map, float(self.turns)/float(walls.width)])

    def calculateTurns(self, actions):
        turns = 0
        for i in range(1, len(actions)):
            if actions[i] != actions[i-1]:
                turns += 1
        return turns

# The CornersProblem class is used to 
# set the initial state of the game
# check if the goal state has been reached
# get the successors of a state
# get the cost of the actions taken
class CornersProblem():
     
    # Constructor
    # gameState: the initial state of the game
    # starttime: the time at which the game was started
    def __init__(self, gameState, starttime):
        
        self.walls = gameState.getWalls()
        self.startPosition = gameState.getPacmanPosition()
        top, right = self.walls.height-2, self.walls.width-2
        self.corners = ((1,1), (1,top), (right, 1), (right, top))
        self.starttime = starttime
        
        self._expanded = 0
        self.gameState = gameState
    
    def getStartState(self):
        return (self.startPosition, [])
    
    # isGoalState checks if the goal state has been reached
    # state: the current state of the game
    # return value: True if all 4 corners have been visited, False otherwise
    def isGoalState(self, state):
        cur = state[0]
        visited = state[1]
        
        if cur in self.corners and cur not in visited:
            visited.append(cur)
        
        
        return len(visited) == 4
    
    # getSuccessors returns the successors of a state
    # state: the current state of the game
    # return value: a list of successors
    def getSuccessors(self, state):

        # successors is a list of tuples
        # each tuple contains the next state, the action taken to reach that state and the cost of the action
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state[0]
            visited = state[1]
            dx, dy = Actions.directionToVector(action)
            nx, ny = int(x + dx), int(y + dy)
            isWall = self.walls[nx][ny]
            if not isWall:
                nextState = (nx, ny)
                cost = 1
                nextVisited = visited[:]
                if nextState in self.corners and nextState not in visited:
                    nextVisited.append(nextState)
                successors.append(((nextState, nextVisited), action, cost))
        
        self._expanded += 1
        
        return successors
    
    # getCostOfActions returns the cost of the actions taken
    # actions: the actions taken
    # return value: the cost of the actions taken
    def getCostOfActions(self, actions):

        # if there are no actions, return 999999
        if actions == None: return 999999
        x, y = self.startPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)
    