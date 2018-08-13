'''
Environment for tic-tac-toe

where grid is

0 1 2
3 4 5
6 7 8

players: O, X

'''

class Board(object):

    def __init__(self, state=None, player=None):

        self.NIL = '.'      # blank
        self.CROSS = 'X'    # first (0)
        self.NAUGHT = 'O'   # second (1)

        self.rows = 3
        self.columns = 3
        self.cells = 9
        self.win = 3

        self.lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                      [0, 3, 6], [1, 4, 7], [2, 5, 8],
                      [0, 4, 8], [2, 4, 6]]

        self.reset()

        if state is not None:
            self.state = state
            self.player = player
            for n in range(self.cells):
                if state[n] is not None:
                    self.action_space.remove(n)

    def step(self,player,action):
        if action not in self.action_space or player != self.player:
            reward_player, reward_opp, done, winner = self.check_win()
            return self.turn_state(player), reward_player, reward_opp, done, winner

        self.state[action] = player
        self.action_space.remove(action)

        self.player = (self.player + 1) % 2

        # print(self.action_space)

        reward_player, reward_opp, done, winner = self.check_win()

        return self.turn_state(player), reward_player, reward_opp, done, winner

    def render(self, state = None): # draws environment
        if state is None:
            state = self.state

        state_printer = []
        for cell in state:
            if cell is 0:
                state_printer.append(self.CROSS)
            elif cell is 1:
                state_printer.append(self.NAUGHT)
            else:
                state_printer.append(self.NIL)

        for x in range(self.rows):
            for y in range(self.columns):
                print(state_printer[x*3+y],end="")
            print()
        print()

    def reset(self):
        self.state = [None] * self.cells
        self.player = 0
        self.action_space = list(range(self.cells))
        return self.turn_state(self.player)

    def turn(self): # returns current player
        return self.player

    def turn_state(self, turn=None): # return state based on player, turn = 0 (cross) or 1 (naught)
                                # self = A, other player = Z
        if turn == 0:
            cross = 1
            naught = 2
        elif turn == 1:
            cross = 1
            naught = 2
        else:
            return self.state

        state_list = []

        for cell in self.state:
            if cell == 0:
                state_list.append(cross)
            elif cell == 1:
                state_list.append(naught)
            else:
                state_list.append(cell)

        return state_list

    # Internal functions

    def check_win(self): # check for win conditions

        done = False
        winner = None

        line_set = set()

        for line in self.lines:
            for cell in line:
                line_set.add(self.state[cell])
            if len(line_set) == 1 and None not in line_set:
                done = True
                winner = line_set.pop()
            line_set.clear()

        if done:
            reward_player = 1
            reward_opp = -1
        else:
            if not self.action_space: # if empty
                done = True
                reward_player, reward_opp = 0, 0
            else:
                reward_player, reward_opp = 0, 0

        return reward_player, reward_opp, done, winner

