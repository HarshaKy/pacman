from game import Directions
from game import Agent
from game import Actions
import game
import util, time, search

class CornerSeekingAgent(Agent):

    def __init__(self, fn='dfs'):
        
        searchFn = getattr(search, fn)
        self.searchFn = searchFn
    
    def registerInitialState(self, state):

        self.starttime = time.time()
        problem = CornersProblem(state, self.starttime)
        self.actions = self.searchFn(problem)
        print len(self.actions)
        totalCost = problem.getCostOfActions(self.actions)
    
    def getAction(self, state):
            
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions): return self.actions[i]
        else:
            print '%.1f seconds' % (time.time() - self.starttime)
            return Directions.STOP

class CornersProblem():
     
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
    
    def isGoalState(self, state):
        cur = state[0]
        visited = state[1]
        
        if cur in self.corners and cur not in visited:
            visited.append(cur)
        
        
        return len(visited) == 4
    
    def getSuccessors(self, state):

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
    
    def getCostOfActions(self, actions):

        if actions == None: return 999999
        x, y = self.startPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)
    