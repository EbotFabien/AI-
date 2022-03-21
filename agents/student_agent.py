# Student agent: Add your own agent here
from pickle import NONE
from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import sys
from functools import lru_cache

sys.setrecursionlimit(10000)



@register_agent("student_agent")
class StudentAgent(Agent):
    """
    A dummy class for your implementation. Feel free to use this class to
    add any helper functionalities needed for your agent.
    """

    def __init__(self):
        super(StudentAgent, self).__init__()
        self.name = "StudentAgent"
        self.k=0
        self.recurs=300
        self.autoplay = True
        self.dir_map = {
            "u": 0,
            "r": 1,
            "d": 2,
            "l": 3,
        }

    def check_barrier(self,chess_board,r,c,dir):
        if chess_board[r, c, dir] == True:
            return True
        else:
            return False
    
    def check_lock(self,chess_board,r,c):
        for barrier in range(0,4):
            if chess_board[r, c, barrier] == True:
                self.k +=1
        if self.k >2:
            self.k = 0
            return True
        else:
            return False
    
    

    def available_moves(self,my_pos,chess_board,adv_pos):#BFS

        M=len(chess_board)-1 #get board length
        x,y=my_pos
        dir={}
        #get all possible moves from point my_pos
        dir['D']=M-x
        dir['R']=M-y
        dir['U']=M-dir['D']
        dir['L']=M-dir['R']

        for direc in dir:
            if direc=='U':
                mov=x-dir[direc]#get the desired position to move to
                for direction in range(-(dir[direc]),mov+1):
                        check=self.check_barrier(chess_board,(-1*direction),y,0) #check if you have barrier 
                        if check ==True  or my_pos == adv_pos:
                            dir[direc]=(dir[direc]-(-1*direction)) #assign new  steps after barrier found
                            break
            if direc=='D' :
                mov=x+dir[direc] #get the desired position to move to
                for direction in range(x,mov+1):
                        check=self.check_barrier(chess_board,direction,y,2) #check if you have barrier 
                        if check ==True or my_pos == adv_pos:
                            mov=(M-direction)-dir[direc] #assign new  steps after barrier found
                            if mov < 0:
                                mov=(-1*mov)
                            break
            if direc=='L':
                mov=y-dir[direc] #get the desired position to move to
                for direction in range(-(dir[direc]),mov+1):
                    check=self.check_barrier(chess_board,x,(-1*direction),3)  #check if you have barrier 
                    if check ==True or my_pos == adv_pos:
                        dir[direc]=(dir[direc]-(-1*direction)) #assign new  steps after barrier found
                        break
            if direc=='R':
                mov=y+dir[direc] #get the desired position to move to
                for direction in range(y,mov+1):
                    check=self.check_barrier(chess_board,x,direction,1)
                    if check ==True or my_pos == adv_pos:
                        mov=(M-direction)-dir[direc] #assign new  steps after barrier found
                        if mov < 0:
                            mov=(-1*mov)
                        dir[direc]=mov
                        break
        return dir

        

    def search_best_move(self,sort,my_pos,max_step,chess_board):# Mini Max  algorithm to find the best and longest path
        x,y=my_pos
        final_steps=None
        mov_dir=None
        bar=None
        moves = {}
        sorted_keys = sorted(sort, key=sort.get)  # [1, 3, 2]
        for w in sorted_keys:
            moves[w] = sort[w]
        
        
        #arrange moves from  highest to lowest
        for move in moves:
            if moves[move] < max_step:
                if move =='U':
                    x-=moves[move]
                    if self.check_lock(chess_board,x,y) == False:
                        final_steps=moves[move]
                        mov_dir=0
                        break
                if move =='D':
                    x+=moves[move]
                    if self.check_lock(chess_board,x,y) == False:
                        final_steps=moves[move]
                        mov_dir=2
                        break
                if move =='L':
                    y-=moves[move]
                    if self.check_lock(chess_board,x,y) == False:
                        final_steps=moves[move]
                        mov_dir=3
                        break
                if move =='R':
                    y+=moves[move]
                    if self.check_lock(chess_board,x,y) == False:
                        final_steps=moves[move]
                        mov_dir=1
                        break
            if moves[move] > max_step:
                if move =='U':
                    x-=max_step
                    if self.check_lock(chess_board,x,y) == False:
                        final_steps=max_step
                        mov_dir=0
                        break
                if move =='D':
                    x+=max_step
                    if self.check_lock(chess_board,x,y) == False:
                        final_steps=max_step
                        mov_dir=2
                        break
                if move =='L':
                    y-=max_step
                    if self.check_lock(chess_board,x,y) == False:
                        final_steps=max_step
                        mov_dir=3
                        break
                if move =='R':
                    y+=max_step
                    if self.check_lock(chess_board,x,y) == False:
                        final_steps=max_step
                        mov_dir=1
                        break
        #sort from lowest,the one that doesn't contain a bar then set as bar 
        least={}
        lower_band_list=sorted(sort, key=sort.get,reverse=True)
        for w in lower_band_list:
            least[w] = sort[w]
        for bard in least:
            if least[bard] != final_steps:
                direction_barrier=bard
                if direction_barrier == 'U':
                    check=self.check_barrier(chess_board,x,y,0)
                    if check == False:
                        bar=0
                        break
                if direction_barrier == 'D':
                    check=self.check_barrier(chess_board,x,y,0)
                    if check == False:
                        bar=2
                        break
                if direction_barrier == 'L':
                    check=self.check_barrier(chess_board,x,y,0)
                    if check == False:
                        bar=3
                        break
                if direction_barrier == 'R':
                    check=self.check_barrier(chess_board,x,y,0)
                    if check == False:
                        bar=1
                        break
            else:
                direction_barrier=bard
                if direction_barrier == 'U':
                    check=self.check_barrier(chess_board,x,y,0)
                    if check == False:
                        bar=0
                        break
                if direction_barrier == 'D':
                    check=self.check_barrier(chess_board,x,y,0)
                    if check == False:
                        bar=2
                        break
                if direction_barrier == 'L':
                    check=self.check_barrier(chess_board,x,y,0)
                    if check == False:
                        bar=3
                        break
                if direction_barrier == 'R':
                    check=self.check_barrier(chess_board,x,y,0)
                    if check == False:
                        bar=1
                        break
        
        
        if final_steps == None:
            for step in range(0,max_step + 1):
                pos=(x+step,y)
                if self.boundary(pos,chess_board) == False:
                    mov_dir=2
                    final_steps=step
                    break
                pos=(x-step,y)
                if self.boundary(pos,chess_board) == False:
                    mov_dir=0
                    final_steps=step
                    break
                pos=(x,y-step)
                if self.boundary(pos,chess_board) == False:
                    mov_dir=3
                    final_steps=step
                    break
                pos=(x,y+step)
                if self.boundary(pos,chess_board) == False:
                    mov_dir=1
                    final_steps=step
                    break

        if bar == None:
            bar = np.random.randint(0, 4)

        return final_steps,mov_dir,bar
    
    def boundary(self,pos,chess_board):
        x,y=pos
        dim=len(chess_board)-1
        if 0 == x == dim or  0 == y == dim:
            return True
        else:
            return False
    
    
    def step(self, chess_board, my_pos, adv_pos, max_step):
        """
        Implement the step function of your agent here.
        You can use the following variables to access the chess board:
        - chess_board: a numpy array of shape (x_max, y_max, 4)
        - my_pos: a tuple of (x, y)
        - adv_pos: a tuple of (x, y)
        - max_step: an integer

        You should return a tuple of ((x, y), dir),
        where (x, y) is the next position of your agent and dir is the direction of the wall
        you want to put on.

        Please check the sample implementation in agents/random_agent.py or agents/human_agent.py for more details.
        """
        # dummy return
        # Moves (Up, Right, Down, Left)
        moves=self.available_moves(my_pos,chess_board,adv_pos) #definig the different children in the nodes of our search
        speculation=self.search_best_move(moves,my_pos,max_step,chess_board)# gets the steps ,movement and position of bar
        
        
        
        ori_pos = deepcopy(my_pos)
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        steps,mov_dir,bar=speculation
       

        

        # Random Walk
        for _ in range(steps):
            r, c = my_pos
            dir = mov_dir
            m_r, m_c = moves[dir]
            my_pos = (r + m_r, c + m_c)
            
            # Special Case enclosed by Adversary
            k = 0
            while chess_board[r, c, dir] or my_pos == adv_pos:
                k += 1
                if k > 300:
                    break
                dir = np.random.randint(0, 4)
                m_r, m_c = moves[dir]
                my_pos = (r + m_r, c + m_c)

            if k > 300:
                my_pos = ori_pos
                break
            

                    
       
        

        
        r, c = my_pos
        while chess_board[r, c, bar]:
            bar = np.random.randint(0, 4)
        
            
        self.recurs=300
        return my_pos,bar
    
    
    