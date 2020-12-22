# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]		
        pos = currentGameState.getPacmanPosition()
        GhostStates = currentGameState.getGhostStates()
        "*** YOUR CODE HERE ***"
        
        newGhostDistance = [manhattanDistance(ghost.getPosition(), newPos) for ghost in newGhostStates]
        newFoodDistance = [manhattanDistance(f, newPos) for f in newFood.asList()]
        score = 0
        if newGhostDistance:
        	score -= 10/(min(newGhostDistance)+1)
        if newFoodDistance:
            score += 1/(min(newFoodDistance)+1)
        score += successorGameState.getScore() - currentGameState.getScore()
        return score
        
def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    from math import inf
    def max_value(state, depth, max_depth):
        legalMoves = state.getLegalActions()
        if(depth == max_depth): return max([self.evaluationFunction(state, action) for action in legalMoves])
        maxi = -inf
        numAgents = state.getNumAgents()
        for action in legalMoves:
        	#for agentIndex in range(1,numAgents):
            maxi = max(maxi, min_value(state.generateSuccessor(1, action), depth+1, max_depth))
        return maxi
    def min_value(state, depth, max_depth):
        legalMoves = state.getLegalActions()
        if(depth == max_depth): return max([self.evaluationFunction(state, action) for action in legalMoves])
        mini = +inf
        for action in legalMoves:
            mini = min(mini, max_value(state.generateSuccessor(0, action), depth+1, max_depth))
        return mini
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        from math import inf
        def max_value(state, depth):
            legalMoves = state.getLegalActions(0)
            if state.isWin() or state.isLose() or (depth+1 == self.depth): return self.evaluationFunction(state)
            maxi = -inf
            for action in legalMoves:
                maxi = max(maxi,min_value(state.generateSuccessor(0, action), depth+1, 1))
            return maxi
        def min_value(state, depth, agentIndex):
            legalMoves = state.getLegalActions(agentIndex)
            if state.isWin() or state.isLose(): return self.evaluationFunction(state)
            mini = +inf
            for action in legalMoves:
                numAgents = gameState.getNumAgents()
                if agentIndex == numAgents-1:
                    mini = min(mini, max_value(state.generateSuccessor(agentIndex, action), depth))
                else:
                    mini = min(mini, min_value(state.generateSuccessor(agentIndex, action), depth, agentIndex+1))
            return mini
        legalMoves = gameState.getLegalActions(0)
        numAgents = gameState.getNumAgents()
        maxi = -inf
        best = None
        for action in legalMoves:
            temp = min_value(gameState.generateSuccessor(0, action), 0, 1)
            if temp >= maxi:
                maxi = temp
                best = action
        return best

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        from math import inf
        def max_value(state, alpha, beta, depth):
            legalMoves = state.getLegalActions(0)
            if state.isWin() or state.isLose() or (depth+1 == self.depth): return self.evaluationFunction(state)
            maxi = -inf
            newAplha = alpha
            for action in legalMoves:
                maxi = max(maxi,min_value(state.generateSuccessor(0, action), newAplha, beta, 1, depth+1))
                if maxi > beta: return maxi
                newAplha = max(newAplha, maxi)
            return maxi
        def min_value(state, alpha, beta, agentIndex, depth):
            legalMoves = state.getLegalActions(agentIndex)
            if state.isWin() or state.isLose(): return self.evaluationFunction(state)
            mini = +inf
            newBeta = beta
            for action in legalMoves:
                numAgents = gameState.getNumAgents()
                if agentIndex == numAgents-1:
                    mini = min(mini, max_value(state.generateSuccessor(agentIndex, action), alpha, newBeta, depth))
                    if mini < alpha: return mini
                    newBeta = min(newBeta, mini)
                else:
                    mini = min(mini, min_value(state.generateSuccessor(agentIndex, action), alpha, newBeta, agentIndex+1, depth))
                    if mini < alpha: return mini
                    newBeta = min(newBeta, mini)
            return mini
        legalMoves = gameState.getLegalActions(0)
        numAgents = gameState.getNumAgents()
        maxi = -inf
        alpha = -inf
        beta = inf
        best = None
        for action in legalMoves:
            temp = min_value(gameState.generateSuccessor(0, action), alpha, beta, 1, 0)
            if temp >= maxi:
                maxi = temp
                best = action
            if temp > beta:
                return best
            alpha = max(temp, alpha)
        return best

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        from math import inf
        def max_value(state, depth):
            legalMoves = state.getLegalActions(0)
            if state.isWin() or state.isLose() or (depth+1 == self.depth): return self.evaluationFunction(state)
            maxi = -inf
            for action in legalMoves:
                maxi = max(maxi,min_value(state.generateSuccessor(0, action), depth+1, 1))
            return maxi
        def min_value(state, depth, agentIndex):
            legalMoves = state.getLegalActions(agentIndex)
            if state.isWin() or state.isLose(): return self.evaluationFunction(state)
            mini = +inf
            expectation = 0
            for action in legalMoves:
                numAgents = gameState.getNumAgents()
                if agentIndex == numAgents-1:
                    mini = max_value(state.generateSuccessor(agentIndex, action), depth)
                else:
                    mini = min_value(state.generateSuccessor(agentIndex, action), depth, agentIndex+1)
                expectation += mini
            if len(legalMoves) == 0:
                return 0
            return expectation/len(legalMoves)
        legalMoves = gameState.getLegalActions(0)
        numAgents = gameState.getNumAgents()
        maxi = -inf
        best = None
        for action in legalMoves:
            temp = min_value(gameState.generateSuccessor(0, action), 0, 1)
            if temp >= maxi:
                maxi = temp
                best = action
        return best

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood()
    currentFoodDistance = [manhattanDistance(f, pos) for f in currentFood.asList()]
    currentNumFood = currentGameState.getNumFood()
    GhostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    currentGhostDistance = [manhattanDistance(ghost.getPosition(), pos) for ghost in GhostStates]		
    currentCaps = currentGameState.getCapsules()
    currentCapsDist = [manhattanDistance(c, pos) for c in currentCaps]
    if currentGameState.isWin():
        return 9999
    score = 0
    score -= 10*currentNumFood
    score += 50*len(scaredTimes)
    score += 25*len(currentCaps)
    if currentGhostDistance:
        score -= 100/(min(currentGhostDistance)+1)
    if currentFoodDistance:
        score += 10/(min(currentFoodDistance)+1)
    if currentCapsDist:
        score += 10/(min(currentCapsDist)+1)
    return score

# Abbreviation
better = betterEvaluationFunction
