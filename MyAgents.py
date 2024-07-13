# My agents for class

from pacman import Directions
from game import Agent
import api_v4 as api
import random
import game
import util

# GoWestAgent
# and other agents
# Always goes West. For testing purposes.

class HungryAgent(Agent):

    def getAction(self, state):
        food = api.food(state)
        pacman = api.whereAmI(state)
        walls = api.walls(state)

        nearest_food = self.nearestFood(pacman, food, walls, api.legalActions(state))
        print "nearest food: ", nearest_food
        
        if nearest_food is None:
            # return api.makeMove(Directions.STOP, api.legalActions(state))
            return api.makeMove(random.choice(api.legalActions(state)), api.legalActions(state))
        
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

        return None

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
            print "random HUNGRY"
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
            print "random SURVIVOR"
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

class HungrySurvivorAgent(Agent):
    
    def __init__(self):
        self.hungry = HungryAgent()
        self.survivor = SurvivalAgent()
        self.hungry_mode = True
        self.survivor_mode = False

    def getAction(self, state):
        pacman = api.whereAmI(state)
        ghosts = api.ghosts(state)

        if self.ghost_nearby(pacman, ghosts):
            self.hungry_mode = False
            self.survivor_mode = True
        else:
            self.hungry_mode = True
            self.survivor_mode = False

        mode = 'hungry' if self.hungry_mode else 'survivor'
        print "mode: ", mode

        if self.hungry_mode:
            action = self.hungry.getAction(state)
            if action == Directions.STOP:
                self.hungry_mode = False
                self.survivor_mode = True
                return self.survivor.getAction(state)
            else:
                return action
        elif self.survivor_mode:
            action = self.survivor.getAction(state)
            if action == Directions.STOP:
                self.survivor_mode = False
                self.hungry_mode = True
                return self.hungry.getAction(state)
            else:
                return action
        else:
            print "stopping dont know what to do"
            return api.makeMove(Directions.STOP, api.legalActions(state))
           
    def ghost_nearby(self, pacman, ghosts):
        for ghost in ghosts:
            if util.manhattanDistance(pacman, ghost) < 3:
                return True
        return False


class Grid:
         
    # Constructor
    #
    # Note that it creates variables:
    #
    # grid:   an array that has one position for each element in the grid.
    # width:  the width of the grid
    # height: the height of the grid
    #
    # Grid elements are not restricted, so you can place whatever you
    # like at each location. You just have to be careful how you
    # handle the elements when you use them.
    def __init__(self, width, height):
        self.width = width
        self.height = height
        subgrid = []
        for i in range(self.height):
            row=[]
            for j in range(self.width):
                row.append(0)
            subgrid.append(row)

        self.grid = subgrid

    # Print the grid out.
    def display(self):       
        for i in range(self.height):
            for j in range(self.width):
                # print grid elements with no newline
                print self.grid[i][j],
            # A new line after each line of the grid
            print 
        # A line after the grid
        print

    # The display function prints the grid out upside down. This
    # prints the grid out so that it matches the view we see when we
    # look at Pacman.
    def prettyDisplay(self):       
        for i in range(self.height):
            for j in range(self.width):
                # print grid elements with no newline
                print self.grid[self.height - (i + 1)][j],
            # A new line after each line of the grid
            print 
        # A line after the grid
        print
        
    # Set and get the values of specific elements in the grid.
    # Here x and y are indices.
    def setValue(self, x, y, value):
        self.grid[y][x] = value

    def getValue(self, x, y):
        return self.grid[y][x]

    # Return width and height to support functions that manipulate the
    # values stored in the grid.
    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

class MyGreedyAgent(Agent):

    def registerInitialState(self, state):
        self.makeMap(state)
        self.addWallsToMap(state)
        self.updateFoodInMap(state)
        self.map.prettyDisplay()
    
    def makeMap(self, state):
        self.action_map = {
            'North': (0, 1),
            'South': (0, -1),
            'East': (1, 0),
            'West': (-1, 0),
            'Stop': (0, 0)
        }
        corners = api.corners(state)
        print corners
        height = self.getLayoutHeight(corners)
        width  = self.getLayoutWidth(corners)
        self.map = Grid(width, height)
    
    def getLayoutHeight(self, corners):
        height = -1
        for i in range(len(corners)):
            if corners[i][1] > height:
                height = corners[i][1]
        return height + 1
    
    def getLayoutWidth(self, corners):
        width = -1
        for i in range(len(corners)):
            if corners[i][0] > width:
                width = corners[i][0]
        return width + 1

    def addWallsToMap(self, state):
        walls = api.walls(state)
        for i in range(len(walls)):
            self.map.setValue(walls[i][0], walls[i][1], 1)
    
    def updateFoodInMap(self, state):
        for i in range(self.map.getWidth()):
            for j in range(self.map.getHeight()):
                if self.map.getValue(i, j) != 1:
                    self.map.setValue(i, j, 0)
        
        food = api.food(state)
        for i in range(len(food)):
            self.map.setValue(food[i][0], food[i][1], 2)
    
    # def getAction(self, state):
    #     self.updateFoodInMap(state)
    #     self.map.prettyDisplay()
    #     legal = api.legalActions(state)
    #     pacman = api.whereAmI(state)

    #     expected_values = []
    #     for action in legal:
    #         action_coords = self.action_map[action]
    #         outcome = self.calculate_outcomes(action_coords, state, pacman)
    #         expected_value = self.calculate_expected_value(outcome)
    #         expected_values.append(expected_value)
        
    #     max_expected_value_index = expected_values.index(max(expected_values))
    #     selected_action = legal[max_expected_value_index]
    #     print "selected action: ", selected_action

    #     return  api.makeMove(selected_action, legal)
    
    # def calculate_outcomes(self, action, state, pacman):
    #     legal = api.legalActions(state)

    #     new_state = []
    #     probability = 1.0 / len(legal)
    #     value_at_position = self.map.getValue(pacman[0] + action[0], pacman[1] + action[1])
        
    #     return (new_state, probability, value_at_position)
    
    # def calculate_expected_value(self, outcome):
    #     expected_value = 0
    #     expected_value = outcome[1] * outcome[2]
        
    #     return expected_value
    def getAction(self, state):
        self.updateFoodInMap(state)
        self.map.prettyDisplay()
        legal = api.legalActions(state)
        pacman = api.whereAmI(state)

        # Check for adjacent food
        adjacent_food_action = self.get_adjacent_food_action(state, pacman)
        if adjacent_food_action:
            print("Eating adjacent food!")
            return api.makeMove(adjacent_food_action, legal)

        expected_values = []
        for action in legal:
            action_coords = self.action_map[action]
            outcome = self.calculate_outcomes(action_coords, state, pacman)
            expected_value = self.calculate_expected_value(outcome)
            expected_values.append(expected_value)
        
        max_expected_value_index = expected_values.index(max(expected_values))
        selected_action = legal[max_expected_value_index]
        print("Selected action:", selected_action)

        return api.makeMove(selected_action, legal)

    def get_adjacent_food_action(self, state, pacman):
        # for action in api.legalActions(state):
        #     action_coords = self.action_map[action]
        #     successor = state.generateSuccessor(pacman, [action_coords[0], action_coords[1]])
        #     successor_pacman = api.whereAmI(successor)

        #     if successor_pacman in api.food(successor):
        #         return action  # Return the action leading to adjacent food

        # return None  # No adjacent food found
        for action in api.legalActions(state):
            action_coords = self.action_map[action]
            if self.map.getValue(pacman[0] + action_coords[0], pacman[1] + action_coords[1]) == 2:
                return action
        
        return random.choice(api.legalActions(state))

    def calculate_outcomes(self, action, state, pacman):
        legal = api.legalActions(state)

        new_pacman_position = (pacman[0] + action[0], pacman[1] + action[1])

        # if not self.map.is_valid_position(new_pacman_position):
        #     return None

        probability = 1.0 / len(legal)
        value_at_position = self.map.getValue(new_pacman_position[0], new_pacman_position[1])

        # Include the new state in the outcome
        new_state = state.generateSuccessor(pacman, [action[0], action[1]])

        return (new_state, probability, value_at_position)

    def calculate_expected_value(self, outcome):
        if outcome is None:
            return 0

        expected_value = outcome[1] * outcome[2]
        return expected_value