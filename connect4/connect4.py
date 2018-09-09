# Environment for connect four with two players, X and O.

from itertools import groupby, chain

class Board:

    def __init__(self):

        self.NIL = '.'      # blank
        self.CROSS = 'X'    # first (0)
        self.NAUGHT = 'O'   # second (1)

        self.columns = 7
        self.rows = 6
        self.win = 4

        self.action_space = list(range(7))

        self.reset()

    def step(self,player,action):
        if action not in self.action_space or player != self.player:
            reward_player, reward_opp, done, winner = self.checkWin()
            return self.turn_state(player), reward_player, reward_opp, done, winner

        c = self.state[action]
        i = -1
        while c[i] != self.NIL:
            i -= 1
        c[i] = self.CROSS if self.player == 0 else self.NAUGHT

        self.player = (self.player + 1) % 2

        if c[0] != self.NIL:
            self.action_space.remove(action)

        # print(self.action_space)

        reward_player, reward_opp, done, winner = self.checkWin()

        return self.turn_state(player), reward_player, reward_opp, done, winner

    def render(self, state = None): # draws environment
        if state == None:
            state = self.state
        print('  '.join(map(str, range(self.columns))))
        for y in range(self.rows):
            print('  '.join(str(state[x][y]) for x in range(self.columns)))
        print()

    def reset(self):
        self.state = [[self.NIL] * self.rows for _ in range(self.columns)]
        self.player = 0
        self.action_space = list(range(7))
        return self.state

    def turn(self): # returns current player
        return self.player

    def turn_state(self, turn): # return state based on player, turn = 0 (cross) or 1 (naught)
                                # self = A, other player = Z
        if turn == 0:
            cross = 'A'
            naught = 'Z'
        elif turn == 1:
            cross = 'Z'
            naught = 'A'
        else:
            return self.state

        state_list = []

        for column in self.state:
            column_list = []
            for cell in column:
                if cell == self.CROSS:
                    new_cell = cross
                elif cell == self.NAUGHT:
                    new_cell = naught
                else:
                    new_cell = cell
                column_list.append(new_cell)
            state_list.append(column_list)

        return state_list

    # Internal functions

    def checkWin(self): # check for win conditions

        if self.action_space == []:

            reward_player = 0
            reward_opp = 0
            done = True
            winner = None

            return reward_player, reward_opp, done, winner

        lines = (
            self.state,
            zip(*self.state),
            self.diagPos(),
            self.diagNeg()
        )

        done = False
        winner = None

        for line in chain(*lines):
            for team, group in groupby(line):
                if team != self.NIL and len(list(group)) >= self.win:
                    done = True
                    winner = team

        if done:
            reward_player = 1
            reward_opp = -1
        else:
            reward_player = 0
            reward_opp = 0

        return reward_player, reward_opp, done, winner

    def diagPos(self): # checks diagonals
        matrix = self.state
        columns = self.columns
        rows = self.rows
        for di in ([(j, i - j) for j in range(columns)] for i in range(columns + rows - 1)):
            yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < columns and j < rows]

    def diagNeg(self): # checks diagonals
        matrix = self.state
        columns = self.columns
        rows = self.rows
        for di in ([(j, i - columns + j + 1) for j in range(columns)] for i in range(columns + rows - 1)):
            yield [matrix[i][j] for i, j in di if i >= 0 and j >= 0 and i < columns and j < rows]

