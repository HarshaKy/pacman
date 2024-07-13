# mdpAgents.py
# parsons/20-nov-2017
#
# Version 1
#
# The starting point for CW2.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

import itertools
from pacman import Directions
from game import Agent
import api_v6 as api
import random
import game
import util

# 
# A class that creates a Grid that can be used as a map
# 
# The grid is a nested list. 
# Access specific elements using grid[x][y]
# 
# Referenced from mapAgents.py by Simon Parsons
#
class Grid:
    
    # Constructor
    # 
    # grid:    An array with one position for each element in the map / grid
    # width:   The width of the map / grid
    # height:  The height of the map / grid
    #
    # Will be using map and grid interchangably
    #
    def __init__(self, width, height):
        self.width, self.height = width, height
        subgrid = []

        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(0)
            subgrid.append(row)
        
        self.grid = subgrid
    
    # Display the grid
    #
    # Flips the grid so that the origin is in the bottom left corner
    # This helps us visualize the grid the way we see the game layout
    #
    # Referenced from mapAgents.py by Simon Parsons
    #
    def prettyDisplay(self):
        for i in range(self.height):
            for j in range(self.width):
                print self.grid[self.height - (i + 1)][j],
            print
        print
    
    # Set the value of a specific element in the grid
    #
    # x:       The x coordinate of the element
    # y:       The y coordinate of the element
    # value:   The value to set the element to
    #
    # Referenced from mapAgents.py by Simon Parsons
    #
    def setValue(self, x, y, value):
        self.grid[y][x] = value
    
    # Get the value of a specific element in the grid
    #
    # x:       The x coordinate of the element
    # y:       The y coordinate of the element
    #
    # Referenced from mapAgents.py by Simon Parsons
    #
    def getValue(self, x, y):
        return self.grid[y][x]
    
    # Get the height of the grid
    #
    # Referenced from mapAgents.py by Simon Parsons
    #
    def getHeight(self):
        return self.height
    
    # Get the width of the grid
    #
    # Referenced from mapAgents.py by Simon Parsons
    #
    def getWidth(self):
        return self.width
    

class MDPAgent(Agent):

    # Constructor: this gets run when we first invoke pacman.py
    #
    # self.walls:        List of wall locations
    # self.grid:         Grid of the map
    # self.rewards_map:  Map of rewards for each state - UPDATE
    # self.states_map:   Map of states and their neighbours - UPDATE
    # self.utilities:    Map of utilities for each state - UPDATE
    #
    def __init__(self):
        print "Starting up MDPAgent!"
        name = "Pacman"

        self.walls, self.grid = set(), set()
        self.rewards_map, self.states_map, self.utilities = {}, {}, {}


    # Gets run after an MDPAgent object is created and once there is
    # game state to access.
    def registerInitialState(self, state):
        print "Running registerInitialState for MDPAgent!"
        
        self.mapStates(state)
        self.makeMap(state)
        self.addWallsToMap(state)
        self.walls = set(api.walls(state))
        corners = api.corners(state)
        height = corners[3][1] - corners[0][1]
        width = corners[1][0] - corners[0][0]
        self.grid = set((x,y) for x in range(0,width) for y in range(0,height))
    
    # Create a map of the game
    #
    # state:   The current game state
    #
    # Referenced from mapAgents.py by Simon Parsons
    #
    def makeMap(self, state):
        corners = api.corners(state)
        height = self.getLayoutHeight(corners)
        width = self.getLayoutWidth(corners)
        self.map = Grid(width, height)
    
    # Get the height of the layout
    #
    # corners: The corners of the layout
    #
    # Referenced from mapAgents.py by Simon Parsons
    #
    def getLayoutHeight(self, corners):
        height = -1
        for i in range(len(corners)):
            if corners[i][1] > height:
                height = corners[i][1]
        
        return height + 1

    # Get the width of the layout
    #
    # corners: The corners of the layout
    #
    # Referenced from mapAgents.py by Simon Parsons
    #
    def getLayoutWidth(self, corners):
        width = -1
        for i in range(len(corners)):
            if corners[i][0] > width:
                width = corners[i][0]
        
        return width + 1
    
    # Add walls to the map
    #
    # state:   The current game state
    #
    # Referenced from mapAgents.py by Simon Parsons
    #
    def addWallsToMap(self, state):
        walls = api.walls(state)
        for i in range(len(walls)):
            self.map.setValue(walls[i][0], walls[i][1], '%')
    
    # Map the states of the game
    # Iterate through each location and map possible states from that location
    # If neighbor is a wall, set it back to the current location
    #
    # state:   The current game state
    #
    def mapStates(self, state):
        walls = set(api.walls(state))
        state_map = dict.fromkeys(self.rewards_map.keys())
        for key in state_map.keys():
            neighbors = self.getNeighbors(key)
            state_map[key] = {
                'North': [neighbors[0], neighbors[2], neighbors[3]],
                'South': [neighbors[1], neighbors[2], neighbors[3]],
                'East': [neighbors[2], neighbors[0], neighbors[1]],
                'West': [neighbors[3], neighbors[0], neighbors[1]]
            }
        
            for x, y in state_map[key].items():
                for st in y:
                    if st in walls:
                        y[y.index(st)] = key
        
        self.states_map = state_map
    
    # Get the neighbors of a location
    #
    # location:    The location to get the neighbors of
    #
    def getNeighbors(self, location):
        (x, y) = location
        return [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]
    
    # Map rewards for each location in the game
    #
    # state:   The current game state
    #
    def mapRewards(self, state):
        food = set(api.food(state))
        walls = self.walls
        ghost_states = api.ghostStates(state)
        capsules = set(api.capsules(state))

        # Set default values of -1 for all states
        rewards_map = {}
        for key in self.grid:
            if key not in walls:
                rewards_map[key] = -1
        self.rewards_map = rewards_map

        # Set values of utilities for all states
        utilities = {}
        for key in self.grid:
            if key not in walls:
                utilities[key] = 0
        self.utilities = utilities

        # Set reward values for food
        food_map = {}
        for key, value in self.rewards_map.items():
            if key in food:
                food_map[key] = 10
        self.rewards_map.update(food_map)

        # Set reward values for capsules
        capsule_map = {}
        for key, value in self.rewards_map.items():
            if key in capsules:
                capsule_map[key] = 20
        self.rewards_map.update(capsule_map)

        # Set reward values for ghosts
        # For each ghost set negative reward if they are scared
        # Set negative reward for ghost halo
        for gs in ghost_states:
            if gs[0] in self.rewards_map.keys():
                if gs[1] == 0:
                    self.rewards_map[gs[0]] = -50
                    halo = self.getGhostHalo(state, gs[0], 3)
                    halo_rewards = {}
                    for key, value in self.rewards_map.items():
                        if key in halo:
                            halo_rewards[key] = -25
                    self.rewards_map.update(halo_rewards)

    # Get the halo of a ghost
    # Returns a set of locations around the ghost within a given radius
    # Recursively fetch locations around the ghost
    # 
    # state:   The current game state
    # ghost:   The ghost to get the halo of
    # radius:  The radius of the halo
    # 
    # Referenced from https://github.com/Jay-Down
    #
    # Initially wanted to just calculate manhattan distance of ghost from pacman
    # This was not effecient so I decided to use a halo instead
    # Came across this solution on github and decided to use it
    #
    def getGhostHalo(self, state, ghosts, radius, next=None):
        ghost_locations = api.ghosts(state)
        walls = set(api.walls(state))

        if radius < 1:
            raise ValueError("Radius must be greater than 1")
        
        if next is None:
            next = []
            ghost_neighbors = self.getNeighbors(ghosts)
            ghost_neighbors = [n for n in ghost_neighbors if n not in walls]
            ghost_neighbors = [n for n in ghost_neighbors if n not in ghost_locations]
        
        if next:
            ghost_neighbors = [self.getNeighbors(g) for g in ghosts]
            ghost_neighbors = itertools.chain.from_iterable(ghost_neighbors)
            ghost_neighbors = [n for n in ghost_neighbors if n not in walls]
            ghost_neighbors = [n for n in ghost_neighbors if n not in ghost_locations]
        
        if radius == 1:
            next.append(set(ghost_neighbors))
            final = [list(x) for x in next]
            final = set(itertools.chain.from_iterable(final))
            return final
        else:
            radius -= 1
            next.append(set(ghost_neighbors))
            return self.getGhostHalo(state, set(ghost_neighbors), radius, next)

    # This is what gets run in between multiple games
    #
    # Update dicts and lists when game ends
    #
    def final(self, state):
        print "Looks like the game just ended!"
        self.walls, self.grid = [], []
        self.rewards_map, self.states_map, self.utilities = {}, {}, {}

    # Value iteration
    #
    # state:   The current game state
    #
    def valueIteration(self, state):
        gamma = 0.6 # Discount factor
        epsilon = 0.001 # Convergence factor

        # All possible states, rewards, and utilities
        # Components of Bellman equation
        states = self.states_map
        rewards = self.rewards_map
        utilities = self.utilities

        while True:
            delta = 0 # Change in utility

            # For each location in the game
            # Calculate the utility for each state
            # Update the utility for each location
            for location, utility in utilities.items():
                temp_utilities = {}

                for direction, state in states[location].items():
                    state_utility = rewards[location] + gamma * (0.8 * utilities[state[0]] + 0.1 * 
                                            utilities[state[1]] + 0.1 * utilities[state[2]])
                    temp_utilities[direction] = state_utility
                
                # Get max utility for each location
                max_utility = max(temp_utilities.values())
                utilities[location] = max_utility

                # Get change in utility
                delta = max(delta, abs(utilities[location] - utility))
            
            # If change in utility is less than convergence factor
            # Return utilities
            if delta < epsilon * (1 - gamma) / gamma:
                return utilities

    # Get the best move
    # Get the neighbors of pacman
    # Get the utilities of the neighbors
    # Return the neighbor with the highest utility
    #
    # utilities:   The utilities for each state
    # pacman:      Pacman's location
    #
    def getBestMove(self, utilities, pacman):
        walls = self.walls
        neighbors = [n for n in self.getNeighbors(pacman) if n not in walls]
        neighbor_utilities = [utilities[n] for n in neighbors]
        
        return neighbors[neighbor_utilities.index(max(neighbor_utilities))]

    # Get the direction to move in
    # Get the difference between pacman and the best move
    # Return the direction to move in based on the difference
    #
    # pacman:      Pacman's location
    # best_move:   The best move to make
    #
    def getDirection(self, pacman, best_move):
        diff = tuple(x - y for x, y in zip(pacman, best_move))
        if diff == (0, 1):
            return Directions.SOUTH
        elif diff == (0, -1):
            return Directions.NORTH
        elif diff == (1, 0):
            return Directions.WEST
        elif diff == (-1, 0):
            return Directions.EAST

    def getAction(self, state):

        pacman = api.whereAmI(state)
        legal = api.legalActions(state)
        
        self.mapRewards(state)
        if not self.states_map:
            self.mapStates(state)
        
        utilities = self.valueIteration(state)
        util_keys = utilities.keys()
        util_values = utilities.values()

        for i in range(len(utilities)):
            x = util_keys[i][0]
            y = util_keys[i][1]
            value = '{:3.2f}'.format(util_values[i])
            self.map.setValue(x, y, value)

        best_move = self.getBestMove(utilities, pacman)
        direction = self.getDirection(pacman, best_move)

        return api.makeMove(direction, legal)