from board_env import Gomoku
#from gomoku_agent import Agent
import numpy as np


env = Gomoku(3,3,3)
ep1, ep2 = 0.2, 0.8
agent1 = Agent(env, ep1, 1)
agent2 = Agent(env, ep2, 2)
agents = [agent1, agent2]

#game_steps = list(range(10, 510, 10))
game_steps = list(range(1, 3, 1))
#print(game_steps)

for g in game_steps:
    env.reset()
    done = False
    i = 0
    while not done:
        player = i % len(agents)
        i += 1
        reward, done, retry = agents[player].act()

        if retry:
            # "retry!"
            i -= 1

    print(env.board.board)
    print(reward)

