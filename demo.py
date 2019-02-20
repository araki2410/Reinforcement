import numpy as np
from board_env import Gomoku
from gomoku_agent import Agent
import pickle
import os, sys

args = sys.argv
if len(args) <= 1:
    print("./hoge.py hoge.model")
    exit()

model = args[1]
if model.split(".")[-1] != "model":
    print("./hoge.py hoge.model")
    exit()

f = open(model, 'rb')

V = pickle.load(f)
line_size = 3
col_size = 3
length = 3
env = Gomoku(line_size, col_size, length)
epsilon = 0.2

your_num = 1
agent_num = 2
agent = Agent(env, epsilon, agent_num, V)
players = ["you", agent]
done = False
i = 1

print('If you put [H], \n\n - H -\n - - -\n - - -\n\nyou type "1,2"\n===========\nstart')
#exit()
while not done:
    player = i % 2
    if players[player] == "you":
        print("")
        print(env.board.show_board())
        print("your turn: ")
        action = input()
        line, col = action.split(",")
        line, col = int(line), int(col)
        try:
            if line <= line_size and col <= col_size:
                reward, done, retry = env.step(line-1, col-1, your_num)
                if retry:
                    i -= 1
            else:
                i -= 1
            
        except:
            i -= 1

        print("")
        print(env.board.show_board())
        
    else:
        print("CPU turn... ")
        reward, done, retry = players[player].act()
        if retry:
            i -= 1
        else:
            print("CPU turn: "+str(agent.now_line)+", "+str(agent.now_col))
    i += 1

