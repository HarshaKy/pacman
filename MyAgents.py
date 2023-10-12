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

class HungryAgent(Agent):
    
    def getAction(self, state):
        food = api.food(state)
        pacman = api.whereAmI(state)
        walls = api.walls(state)

        print "food: ", food
        print "pacman: ", pacman
        print "walls: ", walls

        return api.makeMove(Directions.STOP, api.legalActions(state))