from connect4 import Board

NIL = '.'      # blank
CROSS = 'X'    # first (0)
NAUGHT = 'O'   # second (1)

def stateInt(state):
    stateString = ''
    for x in state:
        for y in x:
            if y == 'A':
                z = '0'
            elif y == 'Z':
                z = '1'
            else:
                z = '2'
            stateString+=z
    print(stateString)
    stateInt = int(stateString,3)
    return stateInt


if __name__ == '__main__':

    env = Board()

    while True:
        turn = env.turn()
        env.render()

        action = int(input('{}\'s turn: '.format('0' if turn == 0 else '1')))

        state,reward_0,reward_1,done,winner = env.step(turn,action)

        if done:
            env.render()
            print('Winner: {}'.format(winner))
            break
