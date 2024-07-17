from game import *
from RLAgents import RLAgent
from features import *

import util, random

class QLearningAbstract(RLAgent):

    def __init__(self, **args):
        RLAgent.__init__(self, **args)
        self.QValues = util.Counter()
    
    def getQValue(self, state, action):
        return self.QValues[state, action]
    
    def calculateValue(self, state):
        values = [self.getQValue(state, action) for action in self.legalActions(state)]
        if values:
            return max(values)
        else:
            return 0.0
    
    def calculateAction(self, state):

        actions = self.legalActions(state)
        val = self.calculateValue(state)
        for action in actions:
            if val == self.getQValue(state, action):
                return action

    def update(self, state, action, nextState, reward):
        newQ = (1 - self.alpha) * self.getQValue(state, action)
        newQ += self.alpha * (reward + (self.discount * self.calculateValue(nextState)))
    
class QLearningAgent(QLearningAbstract):

    def __init__(self, extractor='Simple', epsilon=0.5, gamma=0.8, alpha=0.2, numTraining=0, **args):
        self.feature = util.lookup(extractor, globals())()
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0
        QLearningAbstract.__init__(self, **args)
        self.weights = util.Counter()
    
    def getWeights(self):
        return self.weights
    
    def getQValue(self, state, action):
        features = self.feature.getFeatures(state, action)
        QValue = 0.0

        for feature in features:
            QValue += self.weights[feature] * features[feature]
        
        return QValue

    def update(self, state, action, nextState, reward):

        diff = reward + (self.discount * self.calculateValue(nextState) - self.getQValue(state, action))
        features = self.feature.getFeatures(state, action)

        for feature in features:
            self.weights[feature] += self.alpha * features[feature] * diff
    
    def getAction(self, state):
        actions = self.legalActions(state)
        action = None

        if util.flipCoin(self.epsilon):
            action = random.choice(actions)
        else:
            action = self.calculateAction(state)
    
        self.doAction(state, action)
        return action

    def final(self, state):
        QLearningAbstract.final(self, state)
        if self.episodes == self.numTraining:
            pass