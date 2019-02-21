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

i = 1  ## [0,1] 0 is player first, 1 is cpu first
your_num = i%2 + 1
agent_num = (i+1)%2 + 1
agent = Agent(env, epsilon, agent_num, V)
players = ["you", agent]
done = False


print('If you put [H], \n\n - H -\n - - -\n - - -\n\nyou type "1,2"\n===========\nstart')
#exit()
while not done:
    player = i % 2
    if players[player] == "you":
        print("")
        print(env.board.show_board())
        print("your turn: ")
        try:
            action = input()
            line, col = action.split(",")
            line, col = int(line), int(col)
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
        if done:
            print("you win!")
            lose_score = -50
            players[(i+1)%2].result_update(lose_score)
    else:
        print("CPU turn... ")
        print(players[player].show_policy(env.board.board))
        reward, done, retry = players[player].act()
        if retry:
            i -= 1
        else:
            print("CPU turn: "+str(agent.now_line)+", "+str(agent.now_col))
        if done:
            print("cpu win!")
            win_score = 50
            players[player].result_update(win_score)
            exit()
    i += 1

def save_model(agent):
    model_dir = "Model"
    game_size = str(agent.env.line_size)+"x"+str(agent.env.col_size)
    name = game_size+"_agent"+str(int(agent.epsilon*100))+".model"
    model_name = os.path.join(model_dir, name)
    f = open(model_name,'wb')
    pickle.dump(agent.V, f)
    f.close
    print("save model:", model_name)

save_model(agent)
