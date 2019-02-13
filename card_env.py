import random

class Card():
    def __init__(self):
        self.deck = []
        self.table = []
        self.trash = []
        marks = ["h","s","c","d"]
        num = 13
        for i in marks:
            for j in range(num):
                self.deck.append([i+str(j+1), j+1])
                
    def random_pick(self):
        peace_num = len(self.deck)-1
        if peace_num <= 0:
            print("deck empty! reset!")
            #self.reset()
            #peace_num = len(self.deck)-1
            return -1
        picked = self.deck.pop(random.randrange(peace_num))
        self.table.append(picked)
        return picked

    def clean_table(self):
        self.trash.extend(self.table)
        self.table = {}
        
    def reset(self):
        self.deck.extend(self.table)
        self.deck.extend(self.trash)

class Highlow():        
    def __init__(self, steps=40):
        self.cards = Card()
        self.steps = steps
        self.draw_count = 0
        self.top = -1
        
    def draw(self):
        self.top = self.cards.random_pick()[1]

    def highlow(self, action):
        chosen = int(action) % 2  ## 0:low, 1:high 
        newone = self.cards.random_pick()[1]
        draw = 2
        if newone < self.top:
            hl = 0
        elif newone > self.top:
            hl = 1
        elif newone == self.top:
            hl = 2  ## Draw game

        self.top = newone
        
        if hl == draw:
            reword = 0
        elif chosen == hl:
            reword = 1  ## Win!
        else:
            reword = -1 ## Lose..

        return self.top, reword
            
    def actions(self):
        low = 0
        high = 1
        return [low, high]

    def reset(self):
        self.cards.reset()
        self.draw_count = 0
        self.top = -1

    def step(self, action):
        step = self.steps - 1
        if self.draw_count > step:
            raise Exception("The step count exceed maximum. Please reset env")
        else:
            done = True if self.draw_count==step else False

        self.draw_count += 1    
        state, reword = self.highlow(action)
        return state, reword, done
        
# game = Highlow()
# game.draw()
# for i in range(5):
#     #print(game.top, game.highlow(0))
#     print(game.top, game.step(0))
#     print(game.top)
