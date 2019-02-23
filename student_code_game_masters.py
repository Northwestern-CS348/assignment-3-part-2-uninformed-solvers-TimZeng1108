from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """

        disk_on_peg1 = self.kb.kb_ask(parse_input('fact: (on ?disk peg1)'))
        peg1 = []
        if disk_on_peg1:
            for disk in disk_on_peg1:
                peg1.append(int(disk.bindings[0].constant.element[4:]))
        peg1.sort()

        disk_on_peg2 = self.kb.kb_ask(parse_input('fact: (on ?disk peg2)'))
        peg2 = []
        if disk_on_peg2:
            for disk in disk_on_peg2:
                peg2.append(int(disk.bindings[0].constant.element[4:]))
        peg2.sort()

        disk_on_peg3 = self.kb.kb_ask(parse_input('fact: (on ?disk peg3)'))
        peg3 = []
        if disk_on_peg3:
            for disk in disk_on_peg3:
                peg3.append(int(disk.bindings[0].constant.element[4:]))
        peg3.sort()

        return tuple(peg1), tuple(peg2), tuple(peg3)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """

        sl = movable_statement.terms

        cur_state = list(self.getGameState())
        for index in range(3):
            tmp = cur_state[index]
            if len(tmp) == 0:
                disk = 'base'
            else:
                disk = 'disk' + str(tmp[0])
            fact = 'fact: (top ' + str(disk) + ' peg' + str(index + 1) + ')'
            self.kb.kb_retract(parse_input(fact))

        self.kb.kb_retract(Fact(Statement(['on', sl[0], sl[1]])))
        self.kb.kb_assert(Fact(Statement(['on', sl[0], sl[2]])))

        cur_state = list(self.getGameState())
        for index in range(3):
            tmp = cur_state[index]
            if len(tmp) == 0:
                disk = 'base'
            else:
                disk = 'disk' + str(tmp[0])
            fact = 'fact: (top ' + str(disk) + ' peg' + str(index + 1) + ')'
            self.kb.kb_add(parse_input(fact))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))


class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """

        res = [0] * 9

        ask = self.kb.kb_ask(parse_input('fact: (on ?piece ?pos pos1)'))
        if ask:
            for ele in ask:
                index = int(ele.bindings[1].constant.element[3:])
                tmp = str(ele.bindings[0].constant.element)
                if tmp == 'empty':
                    res[index - 1] = -1
                else:
                    res[index - 1] = int(tmp[4:])

        ask = self.kb.kb_ask(parse_input('fact: (on ?piece ?pos pos2)'))
        if ask:
            for ele in ask:
                index = int(ele.bindings[1].constant.element[3:])
                tmp = str(ele.bindings[0].constant.element)
                if tmp == 'empty':
                    res[index + 2] = -1
                else:
                    res[index + 2] = int(tmp[4:])

        ask = self.kb.kb_ask(parse_input('fact: (on ?piece ?pos pos3)'))
        if ask:
            for ele in ask:
                index = int(ele.bindings[1].constant.element[3:])
                tmp = str(ele.bindings[0].constant.element)
                if tmp == 'empty':
                    res[index + 5] = -1
                else:
                    res[index + 5] = int(tmp[4:])

        return tuple(res[0:3]), tuple(res[3:6]), tuple(res[6:9])

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        sl = movable_statement.terms
        self.kb.kb_retract(Fact(Statement(['on', sl[0], sl[1], sl[2]])))
        self.kb.kb_retract(Fact(Statement(['on', Term('empty'), sl[3], sl[4]])))
        self.kb.kb_assert(Fact(Statement(['on', sl[0], sl[3], sl[4]])))
        self.kb.kb_assert(Fact(Statement(['on', Term('empty'), sl[1], sl[2]])))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
