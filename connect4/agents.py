'''
Agents for connect4
'''

from connect4 import Board
from copy import deepcopy
from collections import Counter
from itertools import groupby, chain
import numpy as np

class Human:
    def __init__(self):
        pass

    def act(self, board, player):
        turn = board.turn()
        board.render()
        print(board.action_space)
        action = int(input('Human {}\'s turn: '.format('X' if turn == 0 else 'O')))
        while action not in board.action_space:
            action = int(input('Human {}\'s turn: '.format('X' if turn == 0 else 'O')))
        return action

class Random:
    def __init__(self):
        pass
    def act(self, board, player):
        return np.random.choice(board.action_space)

class AlphaBeta:
    def __init__(self):
        pass
    def act(self, board, player):
        self.player = player
        self.other = (self.player + 1) % 2

        available_actions = board.action_space

        alpha, beta, final_score = -1.0e40, 1.0e40, -1.0e40
        moves = []
        for action in available_actions:
            next_board = deepcopy(board)
            _, _, _, done, _ = next_board.step(player, action)
            if done:
                return action
            score = self.recur(next_board, alpha, beta, self.other, depth=8)
            if score > final_score:
                moves = [action]
                final_score = score
            elif score == final_score:
                moves.append(action)
        move = np.random.choice(moves)
        return move

    def recur(self, board, alpha, beta, curr_player, depth):
        score = 1.0e40 if (curr_player is self.other) else -1.0e40
        available_actions = board.action_space
        for action in available_actions:
            next_board = deepcopy(board)
            _, _, _, done, _ = next_board.step(next_board.turn(), action)
            if done or depth <= 0:
                return self.evaluate(next_board)  # heuristic evaluation at end-node
            next_score = self.recur(next_board, alpha, beta, ((curr_player + 1) % 2), depth - 1)
            if curr_player is self.other:
                score = min(score, next_score)
                if score <= alpha:
                    return score
                beta = min(beta, score)
            elif curr_player is self.player:
                score = max(score, next_score)
                if score >= beta:
                    return score
                alpha = max(alpha, score)
        return score

    def evaluate(self, board):
        # heuristic

        lines = (board.state,
                 zip(*board.state),
                 board.diagPos(),
                 board.diagNeg())

        done, winner = False, None

        score = 0.0

        for line in chain(*lines):
            line_length = len(line)
            if line_length < board.win:
                continue
            lines_number = line_length - board.win + 1
            for n in range(lines_number):
                check_line = line[n:(n+board.win)]
                line_dict = Counter(check_line)
                line_score = 0.0

                if self.player in line_dict and self.other not in line_dict:
                    if line_dict[self.player] == 1:
                        line_score = 1.0e0
                    elif line_dict[self.player] == 2:
                        line_score = 1.0e2
                    elif line_dict[self.player] == 3:
                        line_score = 1.0e4
                    elif line_dict[self.player] == 4:
                        line_score = 1.0e6
                elif self.other in line_dict and self.player not in line_dict:
                    if line_dict[self.other] == 1:
                        line_score = -1.0e0
                    elif line_dict[self.other] == 2:
                        line_score = -1.0e2
                    elif line_dict[self.other] == 3:
                        line_score = -1.0e4
                    elif line_dict[self.other] == 4:
                        line_score = -1.0e6

                score += line_score

        return score


if __name__ == "__main__":
    iters = 1
    play_board = Board()
    player0 = AlphaBeta()
    player1 = AlphaBeta()
    for _ in range(iters):

        play_board.reset()
        done = False
        winner = False

        while not done:
            player = play_board.turn()
            deep_board = deepcopy(play_board)
            if player is 0:
                action = player0.act(deep_board, player)
            elif player == 1:
                action = player1.act(deep_board, player)
            else:
                break
            play_board.render()
            _, _, _, done, winner = play_board.step(player, action)

        play_board.render()
        print(winner)



