import random
from card_env import Highlow
import numpy as np

class Agent():
    
    def __init__(self, env, epsilon):
        self.actions = env.actions()
        self.epsilon = epsilon
        self.num_len = 13
        hllist= [0.0] * len(self.actions)
        self.V = np.array([hllist for j in range(self.num_len)])

    def policy(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            #print(state, self.V[state], np.argmax(self.V[state]))
            return np.argmax(self.V[state])
        
    def play(self, env):
        ## Initialize position of agent.
        hllist= [0] * len(self.actions)
        N = [hllist for j in range(self.num_len)]
        hllist= [0.0] * len(self.actions)
        V = np.array([hllist for j in range(self.num_len)])
        
        env.reset()
        env.draw()
        done = False
        rewards = []
        state = env.top-1 ## 1~13 --> 0~12

        while not done:
            action = self.policy(state)
            next_state, reward, done = env.step(action)
#            print(state, next_state, action, reward)
            rewards.append(reward)
#            n = N[state][action]
#            average = V[state][action]
#            new_average = (average * n + reward) / (n + 1)
#            N[state][action] += 1
#            V[state][action] = new_average
            V[state][action] = V[state][action] + reward 
            state = next_state-1 ## 1~13 --> 0~12
           
        self.V = self.V + np.array(V)
        
        return rewards

            
def main():

    env = Highlow()
    epsilon = [0.0, 0.3, 0.6, 0.9]
    game_steps = list(range(10, 510, 10))
    result = {}
    for e in epsilon:
        agent = Agent(env, e)
        means = []
        # Try 310 episode.
        for i in game_steps:
            env.steps = i
            rewards = agent.play(env)
            means.append(np.mean(rewards))
            print("Episode {}: Agent gets {} reward.".format(i, np.mean(rewards)))
#        print(agent.V)
#        print(env.top)
#        print(agent.V[env.top])
#        print(np.argmax(agent.V[env.top]))
#        exit()
        result["epsilon={}".format(e)] = means
        result["draw_count"] = game_steps
        result = pd.DataFrame(result)
        result.set_index("draw_count", drop=True, inplace=True)
        result.plot.line(figsize=(10, 5))
        plt.savefig("./Img/result.png")
        
if __name__ == "__main__":
    import pandas as pd
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    main()
