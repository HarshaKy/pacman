# My agents for class

from pacman import Directions
from game import Agent
import api
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

# class HungryAgent(Agent):
    
#     def getAction(self, state):
#         food = api.food(state)
#         pacman = api.whereAmI(state)
#         walls = api.walls(state)

#         # print "food: ", food
#         # print "pacman: ", pacman
#         # print "walls: ", walls

#         nearestFood = self.nearestFood(food, pacman, walls, state)
#         return api.makeMove(nearestFood, api.legalActions(state))
    
#     def nearestFood(self, food, pacman, walls, state):
#         foodDistance = {}
#         nearestFood = None
#         for i in range(len(food)):
#             foodDistance[food[i]] = util.manhattanDistance(pacman, food[i])
        
#         nearestFood = min(foodDistance, key=foodDistance.get)

#         return self.direction(pacman, nearestFood, walls, state)
    
#     def direction(self, pacman, nearestFood, walls, state):
#         legal = api.legalActions(state)
#         if pacman[0] < nearestFood[0] and Directions.EAST in legal:
#             return api.makeMove(Directions.EAST, legal)
#         elif pacman[0] > nearestFood[0] and Directions.WEST in legal:
#             return api.makeMove(Directions.WEST, legal)
#         elif pacman[1] < nearestFood[1] and Directions.NORTH in legal:
#             return api.makeMove(Directions.NORTH, legal)
#         elif pacman[1] > nearestFood[1] and Directions.SOUTH in legal:
#             return api.makeMove(Directions.SOUTH, legal)
#         else:
#             return api.makeMove(random.choice(legal), legal)
