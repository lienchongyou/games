'''
List of agents to play Tic Tac Toe:
Human-controlled
Random-choice
Alpha-Beta minimax

http://www.ntu.edu.sg/home/ehchua/programming/java/javagame_tictactoe_ai.html

'''

from board import Board
from copy import deepcopy
from collections import Counter
import numpy as np

class Human:
    def __init__(self):
        pass
    def act(self, board, player):
        print(board.action_space)
        board.render()
        action = int(input('Human move: '))
        while action not in board.action_space:
            action = int(input('Human move: '))
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
        # initialise players
        self.player = player
        self.other = (self.player + 1) % 2
        # find available actions
        available_actions = board.action_space
        # hard-coded actions
        if len(available_actions) == 9:
            return np.random.choice([0, 2, 6, 8])
        elif 4 in available_actions:
            return 4
        # initialise alpha-beta pruning
        alpha, beta, final_score = -1.0e4, 1.0e4, -1.0e4
        moves = [] # array of moves
        for action in available_actions:
            next_board = deepcopy(board)
            _, _, _, done, _ = next_board.step(player, action)
            if done: # if done, choose action to win
                return action
            score = self.recur(next_board, alpha, beta, self.other)
            if score > final_score: # choose move with best final score
                moves = [action]
                final_score = score
            elif score == final_score:
                moves.append(action)
        move = np.random.choice(moves) # randomly choose from all moves
        return move

    def recur(self, board, alpha, beta, curr_player):
        # tree traversal with iteration and recursion
        score = 1.0e4 if (curr_player is self.other) else -1.0e4
        available_actions = board.action_space
        for action in available_actions:
            next_board = deepcopy(board)
            _, _, _, done, _ = next_board.step(next_board.turn(), action)
            if done:
                return self.evaluate(next_board) # heuristic evaluation at end-node
            next_score = self.recur(next_board, alpha, beta, ((curr_player+1)%2))
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
        # heuristic evaluation
        lines = board.lines
        score = 0.0

        for line in lines:
            line_list = list(map(lambda x: board.state[x],line))
            line_dict = Counter(line_list)
            line_score = 0.0

            if self.player in line_dict and self.other not in line_dict:
                if line_dict[self.player] == 1:
                    line_score = 1.0
                elif line_dict[self.player] == 2:
                    line_score = 10.0
                elif line_dict[self.player] == 3:
                    line_score = 100.0
            elif self.other in line_dict and self.player not in line_dict:
                if line_dict[self.other] == 1:
                    line_score = -1.0
                elif line_dict[self.other] == 2:
                    line_score = -10.0
                elif line_dict[self.other] == 3:
                    line_score = -100.0

            score += line_score

        return score








