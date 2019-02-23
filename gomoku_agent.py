import random, os, sys
from board_env import Gomoku
import numpy as np
import pickle

class Agent():
    
    def __init__(self, env, epsilon, player_number=1, V={}):
        self.player = player_number
        self.env = env
        self.actions = self.env.actions()
        self.epsilon = epsilon
        self.V = V
        self.game_size = "games"
        if self.game_size not in self.V:
            self.V["games"] = 0
        self.states = [] ## for demo test

    def policy(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
#            print(state)
            state = state.reshape(-1).tolist()
            state = str(state)
            if state not in self.V:
                return random.choice(self.actions)

            mean = self.V[state][0] / self.V[state][1]

            fixed_num  = np.argmax(mean)
#            fixed_num = np.argmax(self.V[state][0])
            line = int(fixed_num / self.env.line_size)
            col = fixed_num % self.env.col_size
#            print(line, col)
            return line, col

    def show_policy(self, state):
        state = state.reshape(-1).tolist()
        state = str(state)
        if state not in self.V:
            return "no policy"

        mean = self.V[state][0] / self.V[state][1]

        #return self.V[state][1]
        return mean
        

    def expected_reward(self, next_state):
        next_state = next_state.reshape(-1).tolist()
        next_state = str(next_state)
        expected = 0
        if next_state not in self.V:
            return expected

        # expected = self.V[next_state][0][self.V[next_state][0] > 0].sum() ## sum of grater than 0
        # expected = expected / (self.env.line_size * self.env.col_size)
        expected = self.V[next_state][0].sum() / (self.env.line_size * self.env.col_size)
        return expected

    def act(self):
        state = self.env.board.board.copy()
        line, col = self.policy(state)
        self.now_line, self.now_col = line, col ## for demo

        reward, done, retry = self.env.step(line, col, self.player)  ## put stone
        # next_state = self.env.board.board.copy()
        # expected_reward = self.expected_reward(next_state)
        expected_reward = 0 ## why add enemys reward? its should be less than 0

        self.update(state, line, col, reward)
        if not retry:
            state = state.reshape(-1).tolist()
            state = str(state)
            self.states.append([state, line, col])
    
        return reward, done, retry
    
    def update(self, state, line, col, reward):
        self.old_state = state ## for result_update for losser
        state = state.reshape(-1).tolist()
        state = str(state)

        if state not in self.V:
            total_reward = 0
            N = np.ones((self.env.line_size, self.env.col_size))
            V = np.zeros((self.env.line_size, self.env.col_size))
            self.V[state]=[V, N]

        self.V[state][0][line][col] += reward
        self.V[state][1][line][col] += 1 ## times of try to put
        #self.old_line = line ## for demo test
        #self.old_col = col ## for demo test


    def result_update(self, final_reward, rate=2.0):
        last_state, last_line, last_col = self.states[-1]
        for state, line, col in self.states[-self.env.length:][::-1]:
            self.V[state][0][line][col] += final_reward
            final_reward = final_reward * rate

        self.V[self.game_size] += 1

        return last_line, last_col


#==================
def save_model(agent):
    model_dir = "Model"
    game_size = str(agent.env.line_size)+"x"+str(agent.env.col_size)
    name = game_size+"_agent"+str(int(agent.epsilon*100))+".model"
    model_name = os.path.join(model_dir, name)
    f = open(model_name,'wb')
    pickle.dump(agent.V, f)
    f.close
    print("save model:", model_name)

def main(board_lines, board_cols, target_length, epsilon_1, epsilon_2, max_steps=1000, V1={}, V2={}):
    env = Gomoku(board_lines, board_cols, target_length)
    ep1, ep2 = epsilon_1, epsilon_2
    player_number_1 = 1
    player_number_2 = 2
    agentA = Agent(env, ep1, player_number_1, V1)
    agentB = Agent(env, ep2, player_number_2, V2)
    agents = [[agentA, "agentA"], [agentB, "agentB"]]
    wins = {"draw":0, "agentA":0, "agentB":0}  ## logs
    #game_steps = list(range(10, 510, 10))
    game_steps = list(range(1, max_steps, 1))
    for g in game_steps:
        env.reset()
        done = False
        i = 0
        while not done:
            player = i % len(agents)
            reward, done, retry = agents[player][0].act()
            i += 1
            if retry:
                # "retry!"
                i -= 1
#            else:
        print(env.board.board)

        if reward == 0:
            print("draw")
            wins["draw"] += 1 ## draw logs
            ## Draw Update
            ## TODO
            agents[0][0].result_update(-1) ## First player must win
            agents[1][0].result_update(1) ## 2nd player's playing is good
        else:
            ## Winner Update 
            last_line, last_col = agents[player][0].result_update(1) ## win
            ## Losser Update
            losser = i%2
            agents[losser][0].result_update(-2)                                     ## lose
            agents[losser][0].update(agents[losser][0].old_state, last_line, last_col, 1)  ## lose

            winner = agents[player][1]
            print("winner : ", winner, ":", player+1,  ", steps:",env.line_size * env.col_size - env.steps, ", progress:", str(int((g/max_steps)*100))+"%" )
            wins[winner] += 1  ## won logs

        agents = agents[::-1] ## Change first player
        for i in range(len(agents)): ## First player number = 1
            agents[i][0].player=i+1


    print("draw:",wins["draw"],", win_pl1:",wins["agentA"],", win_pl2:",wins["agentB"])

    print("learned games:", agentA.V[agentA.game_size])
    save_model(agentA)
#    save_model(agentB)

if __name__ == "__main__":
    V1={}
    V2={}
    args = sys.argv
    if len(args) > 1:
        model = args[1]
        if model.split(".")[-1] == "model":
            f1 = open(model, 'rb')
            f2 = open(model, 'rb')
            V1 = pickle.load(f1)
            V2 = pickle.load(f2)
#            f.close

    board_lines, board_cols = 3, 3
    target_length = 3
    epsilon_1 = 0.2 ## random rate for agent 1
    epsilon_2 = 0.01 ## random rate for agent 2
    steps = 1001

    VA = V1.copy()
    VB = V2.copy()
    main(board_lines, board_cols, target_length, epsilon_1, epsilon_2, steps, VA, VB)
