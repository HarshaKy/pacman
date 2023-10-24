# My agents for class

from pacman import Directions
from game import Agent
import api_v2 as api
import random
import game
import util

# GoWestAgent
#
# Always goes West. For testing purposes.

class HungryAgent(Agent):

    def getAction(self, state):
        food = api.food(state)
        pacman = api.whereAmI(state)
        walls = api.walls(state)

        nearest_food = self.nearestFood(pacman, food, walls, api.legalActions(state))
        return self.direction(pacman, nearest_food, api.legalActions(state))

    def nearestFood(self, pacman, food, walls, legal_actions):
        def heuristic(node):
            return abs(node[0] - pacman[0]) + abs(node[1] - pacman[1])

        open_set = [(pacman, 0)]
        came_from = {}

        while open_set:
            current, _ = min(open_set, key=lambda node: heuristic(node[0]))
            open_set.remove((current, _))

            if current in food:
                return current

            for neighbor in [(current[0] + 1, current[1]), (current[0] - 1, current[1]),
                             (current[0], current[1] + 1), (current[0], current[1] - 1)]:
                if neighbor not in walls and neighbor not in came_from:
                    open_set.append((neighbor, heuristic(neighbor)))
                    came_from[neighbor] = current

        return pacman

    def direction(self, current, next_food, legal_actions):
        dx = next_food[0] - current[0]
        dy = next_food[1] - current[1]

        if dx > 0 and Directions.EAST in legal_actions:
            return Directions.EAST
        elif dx < 0 and Directions.WEST in legal_actions:
            return Directions.WEST
        elif dy > 0 and Directions.NORTH in legal_actions:
            return Directions.NORTH
        elif dy < 0 and Directions.SOUTH in legal_actions:
            return Directions.SOUTH
        else:
            return random.choice(legal_actions)

class SurvivalAgent(Agent):

    def getAction(self, state):
        legal = api.legalActions(state)
        food = api.food(state)
        pacman = api.whereAmI(state)
        ghosts = api.ghosts(state)
        walls = api.walls(state)

        if self.ghost_nearby(pacman, ghosts):
            return self.runAway(pacman, ghosts, walls, legal)
        else:
            return api.makeMove(random.choice(legal), legal)
        
    def ghost_nearby(self, pacman, ghosts):
        for ghost in ghosts:
            if util.manhattanDistance(pacman, ghost) < 3:
                return True
        return False
    
    def runAway(self, pacman, ghosts, walls, legal):
        ghostDistance = {}
        nearestGhost = None
        for i in range(len(ghosts)):
            ghostDistance[ghosts[i]] = util.manhattanDistance(pacman, ghosts[i])
        
        nearestGhost = min(ghostDistance, key=ghostDistance.get)

        return self.direction(pacman, nearestGhost, walls, legal)
    
    def direction(self, pacman, nearestGhost, walls, legal):
        if pacman[0] < nearestGhost[0] and Directions.WEST in legal:
            return api.makeMove(Directions.WEST, legal)
        elif pacman[0] > nearestGhost[0] and Directions.EAST in legal:
            return api.makeMove(Directions.EAST, legal)
        elif pacman[1] < nearestGhost[1] and Directions.SOUTH in legal:
            return api.makeMove(Directions.SOUTH, legal)
        elif pacman[1] > nearestGhost[1] and Directions.NORTH in legal:
            return api.makeMove(Directions.NORTH, legal)
        else:
            print "random"
            return api.makeMove(random.choice(legal), legal)

class GoWestAgent(Agent):

    def getAction(self, state):
        legal = api.legalActions(state)
        if Directions.WEST in legal:
            return api.makeMove(Directions.WEST, legal)
        else:
            return self.goUpOrDown(legal)
    
    def goUpOrDown(self, legal):
        if Directions.NORTH in legal:
            return api.makeMove(Directions.NORTH, legal)
        elif Directions.SOUTH in legal:
            return api.makeMove(Directions.SOUTH, legal)
        else:
            return api.makeMove(Directions.STOP, legal)

class CornerSeekingAgent(Agent):

    def __init__(self):
        self.NW = False
        self.NE = False
        self.SW = False
        self.SE = False

    def getAction(self, state):
        corners = api.corners(state)
        pacman = api.whereAmI(state)
        legal = api.legalActions(state)
        coords = {
            'SW': (corners[0][0] + 1, corners[0][1] + 1),
            'SE': (corners[1][0] - 1, corners[1][1] + 1),
            'NW': (corners[2][0] + 1, corners[2][1] - 1),
            'NE': (corners[3][0] - 1, corners[3][1] - 1)
        }

        self.updateCorners(pacman, coords)

        if not self.NW:
            if Directions.WEST in legal:
                return api.makeMove(Directions.WEST, legal)
            elif Directions.NORTH in legal:
                return api.makeMove(Directions.NORTH, legal)
            else:
                return api.makeMove(random.choice(legal), legal)
        
        if not self.SW:
            if Directions.WEST in legal:
                return api.makeMove(Directions.WEST, legal)
            elif Directions.SOUTH in legal:
                return api.makeMove(Directions.SOUTH, legal)
            else:
                return api.makeMove(random.choice(legal), legal)

        if not self.NE:
            if Directions.EAST in legal:
                return api.makeMove(Directions.EAST, legal)
            elif Directions.NORTH in legal:
                return api.makeMove(Directions.NORTH, legal)
            else:
                return api.makeMove(random.choice(legal), legal)  
            
        if not self.SE:
            if Directions.EAST in legal:
                return api.makeMove(Directions.EAST, legal)
            elif Directions.SOUTH in legal:
                return api.makeMove(Directions.SOUTH, legal)
            else:
                return api.makeMove(random.choice(legal), legal)

        return api.makeMove(Directions.STOP, api.legalActions(state))
    
    def updateCorners(self, pacman, coords):
        if pacman == coords['NW']:
            self.NW = True
        elif pacman == coords['NE']:
            self.NE = True
        elif pacman == coords['SW']:
            self.SW = True
        elif pacman == coords['SE']:
            self.SE = True

    # def __init__(self):
    #     self.visited_corners = []
    #     self.corners = []
    #     self.last = None

    # def getAction(self, state):
    #     legal = api.legalActions(state)

    #     if len(self.visited_corners) == 4:
    #         return api.makeMove(Directions.STOP, legal)
        
    #     if not self.corners:
    #         self.corners = api.corners(state)
        
    #     next_corner = self.corners[-1]
    #     pacman = api.whereAmI(state)
    #     walls = api.walls(state)

    #     if self.pacman_in_corner(pacman, next_corner):
    #         print "pacman in corner"
    #         print "pacman: ", pacman
    #         print "current corner: ", next_corner
    #         self.visited_corners.append(next_corner)
    #         self.corners.pop()
    #         self.next_corner = self.corners[-1]
    #         print "next corner: ", self.next_corner

    #     return self.direction(pacman, next_corner, walls, legal)

    # def pacman_in_corner(self, pacman, corner):
    #     for c in [(corner[0] + 1, corner[1]), (corner[0] - 1, corner[1]),
    #               (corner[0], corner[1] + 1), (corner[0], corner[1] - 1), (corner[0] + 1, corner[1] + 1), (corner[0] - 1, corner[1] - 1)]:
    #         if c == pacman:
    #             return True
        
    #     return False

    # def direction(self, pacman, next_corner, walls, legal):
    #     if pacman[0] < next_corner[0] and Directions.EAST in legal:
    #         pick = Directions.EAST
    #     elif pacman[0] > next_corner[0] and Directions.WEST in legal:
    #         pick = Directions.WEST
    #     elif pacman[1] < next_corner[1] and Directions.NORTH in legal:
    #         pick = Directions.NORTH
    #     elif pacman[1] > next_corner[1] and Directions.SOUTH in legal:
    #         pick = Directions.SOUTH
    #     else:
    #         pick = self.goUpOrDown(pacman, next_corner, walls, legal)
    #         print "pick: ", pick
 
    #     return api.makeMove(pick, legal)
    
    # def goUpOrDown(self, pacman, next_corner, walls, legal):
    #     if Directions.NORTH in legal:
    #         return Directions.NORTH
    #     elif Directions.SOUTH in legal:
    #         return Directions.SOUTH
    #     else:
    #         return self.goEastOrWest(pacman, next_corner, walls, legal)
        
    # def goEastOrWest(self, pacman, next_corner, walls, legal):
    #     if Directions.EAST in legal:
    #         return Directions.EAST
    #     elif Directions.WEST in legal:
    #         return Directions.WEST
    #     else:
    #         return Directions.STOP