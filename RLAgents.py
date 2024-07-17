import util, time
    
class RLAgent:

    def __init__(self, legalActions = None, numTraining = 100, epsilon = 0.5, alpha = 0.5, gamma = 1):

        if legalActions is None:
            legalActions = lambda state: state.getLegalActions()

        self.legalActions = legalActions
        self.episodes = 0
        self.totalTrainRewards = 0.0
        self.totalTestRewards = 0.0
        self.numTraining = int(numTraining)
        self.epsilon = float(epsilon)
        self.alpha = float(alpha)
        self.gamma = float(gamma)
        self.discount = float(gamma)
    
    def setEpsilon(self, epsilon):
        self.epsilon = epsilon
    
    def setAlpha(self, alpha):
        self.alpha = alpha

    def setDiscount(self, gamma):
        self.gamma = gamma
    
    def update(self, state, action, nextState, reward):
        util.raiseNotDefined()
    
    def getLegalActions(self, state):
        return self.legalActions(state)
    
    def registerInitialState(self, state):
        self.beginEpisode()

        if self.episodes == 0:
            print 'Starting %d episodes of Training' % (self.numTraining)

    def beginEpisode(self):
        self.lastState = None
        self.lastAction = None
        self.episodeRewards = 0.0

    def transition(self, state, action, nextState, reward):
        self.episodeRewards += reward
        self.update(state, action, nextState, reward)
    
    def endEpisode(self):
        if self.episodes < self.numTraining:
            self.totalTrainRewards += self.episodeRewards
        else:
            self.totalTestRewards += self.episodeRewards
        self.episodes += 1
        
        if self.episodes >= self.numTraining:
            self.epsilon = 0.0
            self.alpha = 0.0
    
    def isTraining(self):
        return self.episodes < self.numTraining

    def isTesting(self):
        return not self.isTraining()
    
    def doAction(self, state, action):
        self.lastState = state
        self.lastAction = action
    
    def observationFunction(self, state):

        if self.lastState is not None:
            reward = state.getScore() - self.lastState.getScore()
            self.transition(self.lastState, self.lastAction, state, reward)
        
        return state

    def final(self, state):
        reward = state.getScore() - self.lastState.getScore()
        self.transition(self.lastState, self.lastAction, state, reward)
        self.endEpisode()

        if not 'episodeStartTime' in self.__dict__:
            self.episodeStartTime = time.time()
        
        if not 'lastWindowTotalRewards' in self.__dict__:
            self.lastWindowTotalRewards = 0.0
        
        self.lastWindowTotalRewards += state.getScore()

        EPISODES_BEFORE_UPDATE = 10

        if self.episodes % EPISODES_BEFORE_UPDATE == 0:
            print 'RL Status:'
            windowAvg = self.lastWindowTotalRewards / float(EPISODES_BEFORE_UPDATE)

            if self.episodes <= self.numTraining:
                trainingAverage = self.totalTrainRewards / float(self.episodes)
                print '\tCompleted %d out of %d training episodes' % (self.episodes, self.numTraining)
                print '\tAverage rewards over all training: %.2f' % (trainingAverage)
            else:
                testingAverage = float(self.totalTestRewards) / float(self.episodes - self.numTraining)
                print '\tCompleted %d testing episodes' % (self.episodes - self.numTraining)
                print '\tAverage rewards over testing: %.2f' % (testingAverage)
            
            print '\tAverage rewards for last %d episodes: %.2f' % (EPISODES_BEFORE_UPDATE, windowAvg)
            print '\tEpisode took %.2f seconds' % (time.time() - self.episodeStartTime)
            self.lastWindowTotalRewards = 0.0
            self.episodeStartTime = time.time()

        if self.episodes == self.numTraining:
            txt = 'Training Done'
            print '%s\n%s' % (txt, '-' * len(txt))
