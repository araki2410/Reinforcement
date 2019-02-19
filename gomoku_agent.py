import random
import numpy as np


class Agent():
    
    def __init__(self, env, epsilon, player_number=1):
        self.player = player_number
        self.env = env
        self.actions = self.env.actions()
        self.epsilon = epsilon
        self.num_len = 13
        #self.V = np.array([hllist for j in range(self.num_len)])

    def policy(self, state):
#        if random.random() < self.epsilon:
        return random.choice(self.actions)
#        else:
#            return np.argmax(self.V[state])

    def act(self):
        state = self.env.board.board
        action = self.policy(state)
        line, col = action
        reward, done, retry = self.env.step(line, col, self.player)
        return reward, done, retry

        
    def play(self):
        ## Initialize position of agent.
                
        self.env.reset()
        done = False
        rewards = []
        state = self.env.board.board.copy()
        
        while not done:
            action = self.policy(state)
            line, col = action
            reward, done, retry = self.env.step(line, col, player)
            next_state = self.env.board.board.copy()
            print(state, "\n", next_state, action, reward)
            exit()

            rewards.append(reward)
#            n = N[state][action]
#            average = V[state][action]
#            new_average = (average * n + reward) / (n + 1)
#            N[state][action] += 1
#            V[state][action] = new_average
            V[state][action] = V[state][action] + reward 
            state = next_state
           
        self.V = self.V + np.array(V)
        
        return rewards

    
