from board import Board
from copy import deepcopy
from agents import Human, Random, AlphaBeta

class Runner:

    def __init__(self, player0, player1):

        self.wins, self.draws, self.losses = 0, 0, 0

        self.play_board = Board()

        self.player0 = player0
        self.player1 = player1

    def run(self, iters):
        for _ in range(iters):

            self.play_board.reset()
            done = False
            winner = False
            while not done:
                player = self.play_board.turn()
                deep_board = deepcopy(self.play_board)
                if player == 0:
                    action = self.player0.act(deep_board, player)
                elif player == 1:
                    action = self.player1.act(deep_board, player)
                else:
                    break
                state, reward_player, reward_opp, done, winner = self.play_board.step(player, action)
            self.play_board.render()
            if winner is 0:
                self.wins += 1
            elif winner is 1:
                self.losses += 1
            else:
                self.draws += 1
            print('{} wins, {} draws, {} losses'.format(self.wins, self.draws, self.losses))

        return self.wins, self.draws, self.losses


if __name__ == '__main__':

    runner = Runner(AlphaBeta(), AlphaBeta())
    runner.run(1000)

