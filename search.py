import util

def dfs(problem):
    start = problem.getStartState()
    stack_dfs = util.Stack()
    visited = []
    stack_dfs.push((start, [], 0))

    while not stack_dfs.isEmpty():
        successor, action, cost = stack_dfs.pop()
        if problem.isGoalState(successor):
            return action
        if successor not in visited:
            visited.append(successor)
            for nextState, nextAction, nextCost in problem.getSuccessors(successor):
                stack_dfs.push((nextState, action + [nextAction], nextCost))
