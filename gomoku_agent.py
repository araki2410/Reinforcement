import random
from board_env import Gomoku
import numpy as np


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

    def act(self):
        state = self.env.board.board
        line, col = self.policy(state)
#        line, col = action
        reward, done, retry = self.env.step(line, col, self.player)
        self.update(state, line, col, reward)
        return reward, done, retry
    
    def update(self, state, line, col, reward):
        state = state.reshape(-1).tolist()
        state = str(state)
        if state not in self.V:
            total_reward = 0
            N = np.ones((self.env.line_size, self.env.col_size))
            V = np.zeros((self.env.line_size, self.env.col_size))
            self.V[state]=[V, N]

        self.V[state][0][line][col] += reward       ## total reward
        self.V[state][1][line][col] += 1 ## times of try to put

def main():
    env = Gomoku(3,3,3)
    ep1, ep2 = 0.2, 0.5 ## random rate
    agent1 = Agent(env, ep1, 1)
    agent2 = Agent(env, ep2, 2)
    agents = [agent1, agent2]
    wins = [0,0,0]
    #game_steps = list(range(10, 510, 10))
    game_steps = list(range(1, 4000, 1))
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
            wins[0] += 1
        else:
            winner = (i-1) % 2 + 1
            print("winner : ", winner)
            wins[winner] += 1

    print("draw:",wins[0],", win_pl1:",wins[1],", win_pl2:",wins[2])


if __name__ == "__main__":
    main()
