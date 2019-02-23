
from solver import *


class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """

        if self.currentState.state == self.victoryCondition:
            return True

        movables = self.gm.getMovables()

        for index in range(len(movables)):
            self.gm.makeMove(movables[index])
            tmp = GameState(self.gm.getGameState(), self.currentState.depth + 1, movables[index])
            if tmp not in self.visited:
                self.visited[tmp] = True
                tmp.parent = self.currentState
                self.currentState = tmp
                if self.currentState.state == self.victoryCondition:
                    return True
                else:
                    return False
            self.gm.reverseMove(movables[index])

        if self.currentState.parent is not None:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState.parent = self.currentState.parent.parent
            self.currentState = self.currentState.parent
            return False

        return True


class SolverBFS(UninformedSolver):

    def __init__(self, gameMaster, victoryCondition):
        GameState.FIRST_CHILD_INDEX = 0
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """

        if self.currentState.state == self.victoryCondition:
            return True

        movables = self.gm.getMovables()

        for index in range(len(movables)):
            self.gm.makeMove(movables[index])
            tmp = GameState(self.gm.getGameState(), self.currentState.depth + 1, movables[index])
            tmp.parent = self.currentState
            if tmp not in self.visited:
                self.visited[tmp] = True
                self.currentState.children.append(tmp)
            self.gm.reverseMove(movables[index])

        path = []
        tmp = self.currentState
        while tmp.parent is not None:
            path.append(tmp.requiredMovable)
            tmp = tmp.parent
        for index in range(len(path)):
            self.gm.reverseMove(path[index])

        if GameState.FIRST_CHILD_INDEX < len(self.currentState.children):
            self.currentState.children[GameState.FIRST_CHILD_INDEX].children = self.currentState.children
            self.currentState = self.currentState.children[GameState.FIRST_CHILD_INDEX]
            GameState.FIRST_CHILD_INDEX += 1

            path = []
            tmp = self.currentState
            while tmp.parent is not None:
                path.append(tmp.requiredMovable)
                tmp = tmp.parent
            path.reverse()
            for index in range(len(path)):
                self.gm.makeMove(path[index])

            if self.currentState.state == self.victoryCondition:
                return True
            else:
                return False

        return True
