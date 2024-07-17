from game import Actions
import util

def closestFood(pacman, food, walls):
    q = [(pacman[0], pacman[1], 0)]
    visited = set()

    while q:
        x, y, distance = q.pop(0)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if food[x][y]:
            return distance
        neighbors = Actions.getLegalNeighbors((x, y), walls)
        for nx, ny in neighbors:
            q.append((nx, ny, distance+1))
    return None

class Simple:

    def getFeatures(self, state, action):
        food = state.getFood()
        walls = state.getWalls()
        ghosts = state.getGhostPositions()

        features = util.Counter()
        features['bias'] = 1.0

        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        nx, ny = int(x + dx), int(y + dy)

        features['ghosts_1_step'] = sum((nx, ny) in Actions.getLegalNeighbors(g, walls) for g in ghosts)

        if not features['ghosts_1_step'] and food[nx][ny]:
            features['eat_food'] = 1.0
        
        distance = closestFood((nx, ny), food, walls)
        if distance is not None:
            features['closest_food'] = float(distance) / (walls.width * walls.height)
        
        features.divideAll(10.0)
        
        return features