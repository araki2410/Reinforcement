import random, os
from board_env import Gomoku
import numpy as np
import pickle

class Agent():
    
    def __init__(self, env, epsilon, player_number=1):
        self.player = player_number
        self.env = env
        self.actions = self.env.actions()
        self.epsilon = epsilon
        self.num_len = 13
        #self.V = np.array([hllist for j in range(self.num_len)])
        self.V = {}

    def policy(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            state = state.reshape(-1).tolist()
            state = str(state)
            if state not in self.V:
                return random.choice(self.actions)

            mean = self.V[state][0] / self.V[state][1]

            fixed_num  = np.argmax(mean)
            line = int(fixed_num / self.env.line_size)
            col = fixed_num % self.env.col_size
#            print(fixed_num, line, col)
            return line, col

    def expected_reward(self, next_state):
        next_state = next_state.reshape(-1).tolist()
        next_state = str(next_state)
        expected = 0
        if next_state not in self.V:
            return expected

        expected = self.V[next_state][0][self.V[next_state][0] > 0].sum() ## sum of grater than 0
        return expected

    def act(self):
        state = self.env.board.board.copy()
        line, col = self.policy(state)
#        line, col = action
        reward, done, retry = self.env.step(line, col, self.player)
        next_state = self.env.board.board.copy()
        expected_reward = self.expected_reward(next_state)

        self.update(state, line, col, reward, expected_reward)
        return reward, done, retry
    
    def update(self, state, line, col, reward, expected_reward):
        state = state.reshape(-1).tolist()
        state = str(state)
        expected_rate = 0.8

        if state not in self.V:
            total_reward = 0
            N = np.ones((self.env.line_size, self.env.col_size))
            V = np.zeros((self.env.line_size, self.env.col_size))
            self.V[state]=[V, N]

        reward = reward + expected_reward * expected_rate      ## total reward
        self.V[state][0][line][col] += reward
        self.V[state][1][line][col] += 1 ## times of try to put


def save_model(agent):
    model_dir = "Model"
    game_size = str(agent.env.line_size)+"x"+str(agent.env.col_size)
    name = game_size+"_agent"+str(int(agent.epsilon*100))+".model"
    model_name = os.path.join(model_dir, name)
    f = open(model_name,'wb')
    pickle.dump(agent.V, f)
    f.close
    print("save model:", model_name)

def main(board_lines, board_cols, target_length, epsilon_1, epsilon_2):
    env = Gomoku(board_lines, board_cols, target_length)
    ep1, ep2 = epsilon_1, epsilon_2
    player_number_1 = 1
    player_number_2 = 2
    agent1 = Agent(env, ep1, player_number_1)
    agent2 = Agent(env, ep2, player_number_2)
    agents = [agent1, agent2]
    wins = [0,0,0]  ## logs
    #game_steps = list(range(10, 510, 10))
    game_steps = list(range(1, 10000, 1))
    #print(game_steps)

    for g in game_steps:
        env.reset()
        done = False
        i = 0
        while not done:
            player = i % len(agents)
            reward, done, retry = agents[player].act()
            i += 1
            if retry:
                # "retry!"
                i -= 1
        print(env.board.board)

        if reward == 0:
            print("draw")
            wins[0] += 1 ## draw logs
        else:
            winner = (i-1) % 2 + 1
            print("winner : ", winner,  ", steps:",env.line_size * env.col_size - env.steps)
            wins[winner] += 1  ## won logs

    print("draw:",wins[0],", win_pl1:",wins[1],", win_pl2:",wins[2])
    save_model(agent1)
    save_model(agent2)

if __name__ == "__main__":
    board_lines, board_cols = 3,3
    target_length = 3
    epsilon_1 = 0.2 ## random rate for agent 1
    epsilon_2 = 0.3 ## random rate for agent 2
    main(board_lines, board_cols, target_length, epsilon_1, epsilon_2)
