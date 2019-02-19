import numpy as np

class Board():
    def __init__(self, col_size=19, line_size=19):
        self.col_size = col_size
        self.line_size = line_size
        self.board = np.zeros((self.line_size, self.col_size), dtype="int32")

    def reset(self):
        self.board = np.zeros((self.line_size, self.col_size), dtype="int32")

    def show_board(self):
        print(self.board)

    def put_stone(self, line_num, col_num, player):
        self.board[line_num][col_num] = player



class Gomoku():
    def __init__(self, col_size=19, line_size=19, length=5, reward_type="count"):
        self.col_size = col_size
        self.line_size = line_size
        self.board = Board(self.col_size, self.line_size)
        self.steps = self.line_size * self.col_size
        self.length = length
        self.reward_type = reward_type
        
    def actions(self):
        actions = []
        for i in range(self.line_size):
            for j in range(self.col_size):
                actions.append([i, j])
        return actions

    def reward_calc(self, wins, counts):
        winner_rate = 5
        count_rate = 0.2
        if self.reward_type == "count":
            reward = wins * winner_rate + counts * count_rate
        else:
            reward = wins
        return reward
    
    def step(self, line, col, player):
        self.steps -= 1
        done = False
        retry= False
        reward = 0
        if self.steps < 0:
            done = True
        else:
            wins, counts, retry = self.action(line, col, player)
            reward = self.reward_calc(wins, counts)
            if wins >= 1:
                done = True
        if retry:
            self.steps += 1
                
        return reward, done, retry
        
    def action(self, line_num, col_num, player=1):
        retry = False
        if self.board.board[line_num][col_num] == 0:
            self.board.put_stone(line_num, col_num, player)
        else:
            #print("cant put here!")
            retry = True
            wins = -1
            counts = 0
            return wins, counts, retry
        wins, counts = self.victory_check(line_num, col_num)

        return wins, counts, retry
        
    def victory_check(self, line_num, col_num):
        player = self.board.board[line_num][col_num]
        wins = 0
        counts = 0
        col_num_min = col_num - (self.length - 1)
        line_num_min = line_num - (self.length - 1)

        ## - horizontal
        count= 0
        for i in range(self.length*2-1):
            col = col_num_min + i
            line = line_num
            count, win = self.judge(line, col, player, count)
            wins += win
        counts += count - 1
        ## | vertical
        count= 0
        for i in range(self.length*2-1):
            col = col_num
            line = line_num_min + i
            count, win = self.judge(line, col, player, count)
            wins += win
        counts += count - 1
                        
        ## \ stanting : upper-right to left
        count= 0
        for i in range(self.length*2-1):
            col = col_num_min + i
            line= line_num_min + i
            count, win = self.judge(line, col, player, count)
            wins += win
        counts += count - 1

        ## / slanting : upper-left to right
        count= 0
        col_num_max = col_num + (self.length - 1)
        for i in range(self.length*2-1):
            col = col_num_max - i
            line= line_num_min + i
            count, win = self.judge(line, col, player, count)
            wins += win
        counts += count - 1

        return wins, counts

        
    def judge(self, line, col, player, count):
        win = 0
        if col<0 or self.col_size<=col or line<0 or self.line_size<=line: 
            ## Out of the board
            pass
        else:
            if self.board.board[line][col] == player:
                count += 1
            else:
                count = 0
            if count >= self.length:
                win = 1
        return count, win

    def reset(self):
        self.board.reset()
        self.steps = self.line_size * self.col_size

# hoge = Board(3,3,3)
# hoge.action(1,1,2)
# hoge.action(1,0,1)
# hoge.action(0,0,2)
# hoge.action(2,2,1)
# hoge.action(0,1,2)
# hoge.action(2,1,1)
# hoge.action(0,2,2)
# hoge.show_board()
# hoge.reset()
# hoge.show_board()
