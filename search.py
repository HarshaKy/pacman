import util

def dfs(problem):
    start = problem.getStartState()
    stack_dfs = util.Stack()
    visited = []
    stack_dfs.push((start, [], 0))

    # while the stack is not empty
    # get the successor, action and cost
    # if the successor is the goal state, return the action
    # if the successor is not in the visited list, add it to the visited list
    # get the next state, action and cost
    # push the next state, action and cost to the stack
    while not stack_dfs.isEmpty():
        successor, action, cost = stack_dfs.pop()
        if problem.isGoalState(successor):
            return action
        if successor not in visited:
            visited.append(successor)
            for nextState, nextAction, nextCost in problem.getSuccessors(successor):
                stack_dfs.push((nextState, action + [nextAction], nextCost))
