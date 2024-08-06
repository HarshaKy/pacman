import util, time

# Base class for reinforcement learning agents
# This class specifies the interface for reinforcement learning agents in pacman
# A reinforcement learning agent should be able to interact with an environment
# and learn from the interactions
class RLAgent:

    # legalActions is a function that returns the legal actions in a state
    # numTraining is the number of training episodes
    # epsilon is the exploration probability
    # alpha is the learning rate
    # gamma is the discount factor
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
        self.totalTrainTime = 0.0
        self.totalTestTime = 0.0
        self.trainEpsiodeTimes = []
        self.testEpisodeTimes = []
    
    # setters for the parameters
    def setEpsilon(self, epsilon):
        self.epsilon = epsilon
    
    def setAlpha(self, alpha):
        self.alpha = alpha

    def setDiscount(self, gamma):
        self.gamma = gamma
    
    # update function which will be overrided by the child classes
    def update(self, state, action, nextState, reward):
        util.raiseNotDefined()
    
    # get a list of legal actions for a given state
    def getLegalActions(self, state):
        return self.legalActions(state)
    
    # register the initial state
    def registerInitialState(self, state):
        self.beginEpisode()

        if self.episodes == 0:
            print 'Starting %d episodes of Training' % (self.numTraining)

    # begin a new training episode
    # reset the last state, last action and episode rewards
    def beginEpisode(self):
        self.lastState = None
        self.lastAction = None
        self.episodeRewards = 0.0

    # transition function
    # update the agent with the new state, action, next state and reward
    # update the episode rewards
    def transition(self, state, action, nextState, reward):
        self.episodeRewards += reward
        self.update(state, action, nextState, reward)
    
    # end the episode
    # update the total rewards
    # update the number of episodes
    # update the epsilon and alpha values
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
    
    # observation function
    # update the agent with the new state
    # if the last state is not None, update the agent with the new state, action, next state and reward
    def observationFunction(self, state):

        if self.lastState is not None:
            reward = state.getScore() - self.lastState.getScore()
            self.transition(self.lastState, self.lastAction, state, reward)
        
        return state

    # final function
    # update the agent with the new state, action, next state and reward
    # end the episode
    # if the number of episodes is a multiple of 10, print the status of the agent
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
                self.trainEpsiodeTimes.append(time.time() - self.episodeStartTime)
                self.totalTrainTime += time.time() - self.episodeStartTime
            else:
                testingAverage = float(self.totalTestRewards) / float(self.episodes - self.numTraining)
                print '\tCompleted %d testing episodes' % (self.episodes - self.numTraining)
                print '\tAverage rewards over testing: %.2f' % (testingAverage)
                self.testEpisodeTimes.append(time.time() - self.episodeStartTime)
                self.totalTestTime += time.time() - self.episodeStartTime
            
            print '\tAverage rewards for last %d episodes: %.2f' % (EPISODES_BEFORE_UPDATE, windowAvg)
            print '\tEpisode took %.2f seconds' % (time.time() - self.episodeStartTime)
            self.lastWindowTotalRewards = 0.0
            self.episodeStartTime = time.time()

        if self.episodes == self.numTraining:
            txt = 'Training Done'
            self.saveData(self.trainEpsiodeTimes, self.totalTrainTime)
            print '%s\n%s' % (txt, '-' * len(txt))

    def saveData(self, episodeTimes, totalTime):
        filename = 'rlagenttimes.csv'
        import csv
        with open(filename, 'ab') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([totalTime/len(episodeTimes), totalTime])