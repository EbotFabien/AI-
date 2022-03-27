# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import sys





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
        self.enemy_moves=[]
        self.my_moves=[]
        self.test_list=[]
        self.M=0
        self.latest_len=0
        self.all_lengths={}
        self.last_moves={}
        self.vals=None
        self.autoplay = True
        self.dir_map = {
            "u": 0,
            "r": 1,
            "d": 2,
            "l": 3,
        }

    
    
    
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
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        self.M=len(chess_board)
        self.available_moved(my_pos,self.M,chess_board,adv_pos,self.my_moves,None)#get player available moves 
        self.M=len(chess_board)

        self.latest_len=len(self.my_moves)
        self.available_moved(adv_pos,self.M,chess_board,my_pos,self.enemy_moves,None)#get enemy available moves   
        
        

        self.M=len(chess_board)
        self.Bfs(my_pos,chess_board,adv_pos,max_step)# go through all available moves using bfs

        self.minimax(my_pos)# evaluate if winning or loosing
        

        
        
        length,position,barrier=self.vals
        
        if position != None:
            f=position[1:-1]
            last_pos=(int(f[0]),int(f[-1]))
        else:
            self.random_move(moves,max_step,my_pos,adv_pos,chess_board)
            length,last_pos,barrier=self.vals
        
        if not self.check_valid_step(my_pos, last_pos,barrier,chess_board,adv_pos,max_step,moves):
            self.random_move(moves,max_step,my_pos,adv_pos,chess_board)
            length,last_pos,barrier=self.vals

        #reset all attributes
        self.enemy_moves=[]
        self.my_moves=[]
        self.M=0
        self.latest_len=0
        self.test_list=[]
        self.last_moves={}
        self.all_lengths={}
        self.vals=None
        
        return last_pos,int(barrier)
    
    

    def evaluate(self):#Heuristic evaluation function
        if len(self.my_moves) > len(self.enemy_moves):
            return 'winning'
        if len(self.my_moves) < len(self.enemy_moves):
            return 'loosing'
        if len(self.my_moves) == len(self.enemy_moves):
            return 'Draw'
    
    def random_move(self,moves,max_step,my_pos,adv_pos,chess_board):
        ori_pos = deepcopy(my_pos)
        steps = np.random.randint(0, max_step + 1)

        # Random Walk
        for _ in range(steps):
            r, c = my_pos
            dir = np.random.randint(0, 4)
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
  
        # Put Barrier
        dir = np.random.randint(0, 4)
        r, c = my_pos
        while chess_board[r, c, dir]:
            dir = np.random.randint(0, 4)
        
        self.vals=('random',my_pos,dir)

    def available_moved(self,my_pos,M,chess_board,adv_pos,move_lis,old_pos):

            if M > 0: #recursion limit
                x,y=my_pos
                dir={}
                #get all possible moves from point my_pos
                dir['D']=self.check_barrier(chess_board,x,y,2)
                dir['R']=self.check_barrier(chess_board,x,y,1)
                dir['U']=self.check_barrier(chess_board,x,y,0)
                dir['L']=self.check_barrier(chess_board,x,y,3)

                for direc in dir:
                    if direc=='U':
                        if dir["U"] == False:
                            x2=x-1

                            if (x2,y) != old_pos and my_pos != adv_pos:
                                move_lis.append([str((x,y)),[str((x2,y)),'u']])
                                dir[direc] =(x2,y)

                    if direc=='D':
                        if dir["D"] == False:
                            x2=x+1
                            if (x2,y) != old_pos and my_pos != adv_pos:
                                move_lis.append([str((x,y)),[str((x2,y)),'d']])
                                dir[direc] =(x2,y)
                                
                    if direc=='L':
                        if dir["L"] == False:
                            y2=y-1
                            if (x,y2) != old_pos and my_pos != adv_pos:
                                move_lis.append([str((x,y)),[str((x,y2)),'l']])
                                dir[direc] =(x,y2)
                    if direc=='R':
                        if dir["R"] == False:
                            y2=y+1
                            if (x,y2) != old_pos and my_pos != adv_pos:
                                move_lis.append([str((x,y)),[str((x,y2)),'r']])
                                dir[direc] =(x,y2)
                
                for i in dir:
                    if isinstance(dir[i],tuple) == True:
                        self.M = self.M -1
                        self.available_moved(dir[i],self.M,chess_board,adv_pos,move_lis,my_pos)

            


    def check_barrier(self,chess_board,r,c,dir):
            if chess_board[r, c, dir] == True:
                return True
            else:
                return False

    def check_lock(self,chess_board,r,c):
        for barrier in range(0,4):
            if chess_board[r, c, barrier] == True:
                self.k +=1
        if self.k >=2:
            self.k = 0
            return True
        else:
            return False
    
    def minimax(self,my_pos):#minmax function
        eva=self.evaluate()
        vals=None
        
        if eva == 'winning' or eva == 'Draw' :

            return self.finalmoves(2,len(self.my_moves),'max')

        if eva == 'loosing':

            return self.finalmoves(2,len(self.enemy_moves),'max')


            
    def analyze_future(self,chess_board,adv_pos,my_pos,new_point,x,y):#future available moves
       
        for block in range(0,4):
            if self.check_barrier(chess_board,int(x),int(y),block) == False:
                move_len=self.future_moves(new_point,self.M,chess_board,block,adv_pos,self.test_list,my_pos)
                self.M=len(chess_board)
                self.all_lengths[str(len(self.test_list))]=block
                self.test_list=[]


    def addEdge(self,graph):
            # Function call to make an edge
            for i in self.my_moves:
                if i[0] in graph:
                    pass
                else:
                    graph[i[0]] = []
            for i in range(0, len(self.my_moves)) :

                # Function call to make an edge
                if self.my_moves[i][1][0] in graph:
                    pass
                else:
                    graph[self.my_moves[i][1][0]]=[]

                graph[self.my_moves[i][0]].append(self.my_moves[i][1])
            
            return graph
    
    def bfs(self,visited,queue, graph, node,my_pos,chess_board,adv_pos,max_step):
            visited.append(node)
            queue.append(node)

            while queue:
                s = queue.pop(0) 
                f=s[1:-1]
                new_point=(int(f[0]),int(f[-1]))
               
                #def steps not allowed
                x,y=my_pos
                step1=x-int(f[0])
                step2=y-int(f[-1])

                if step1<0:
                    step1=(-1*step1)
                if step2<0:
                    step2=(-1*step2)

                final=step1+step2
                if final > max_step:
                    Task=False
                else:
                    Task=True


                if s != str(my_pos) and Task==True:
                    self.analyze_future(chess_board,adv_pos,my_pos,new_point,f[0],f[-1])
                    locks_3=self.check_lock(chess_board,int(f[0]),int(f[-1]))
                    self.last_moves[s]=[locks_3,self.all_lengths]
                
                    
                
                #reset variables for bfs
                self.test_list=[]
                self.all_lengths={}
                self.M=len(chess_board)
                
                  
                for neighbour in graph[s]:
                    if neighbour[0] not in visited:
                        visited.append(neighbour[0])
                        queue.append(neighbour[0])

    def Bfs(self,my_pos,chess_board,adv_pos,max_step):
        g ={}
        
        g=self.addEdge(g)
        visited = [] # List to keep track of visited nodes.
        queue = [] 
        
            # Driver Code
        for i in self.my_moves:
            if i[0] == str(my_pos):
                self.bfs(visited,queue,g, i[0],my_pos,chess_board,adv_pos,max_step)


    def finalmoves(self,depth,maximum,frequency): #get the best move available
        sol=None
        win=None
        dire=None
        
        if depth >0:
            for pos in self.last_moves:
              
                if  self.last_moves[pos][0] == False:# do when false is = to true or check boundary well
                    
                    for moves in self.last_moves[pos][1]:
                        
                        if sol ==None:
                            if int(moves) >=maximum:
                                sol=int(moves)
                                dire=self.last_moves[pos][1][moves]
                                win=pos
                        elif sol != None:
                            if int(moves) > sol:
                                sol=int(moves)
                                dire=self.last_moves[pos][1][moves]
                                win=pos
                        
            final=sol
            Barrier=dire
            pos_win=win
            if final == None:
               # self.finalmoves(depth-1,maximum,'min')
               for pos in self.last_moves:
                
                    if  self.last_moves[pos][0] == False:
                        for moves in self.last_moves[pos][1]:
                            #print(moves)
                            #if frequency == 'min':
                            if sol == None:
                                sol=int(moves)
                                dire=self.last_moves[pos][1][moves]
                                win=pos
                            elif sol != None:
                                if int(moves) > sol:
                                    sol=int(moves)
                                    dire=self.last_moves[pos][1][moves]
                                    win=pos
            final=sol
            Barrier=dire
            pos_win=win
            self.vals=(final,pos_win,Barrier)
        else:
            return final,pos_win,Barrier

    
    def future_moves(self,my_pos,M,chess_board,block,adv_pos,move_lis,old_pos):#make adjescent list considering blocks for future moves

            if M > 0: #get board length
                x,y=my_pos
                dir={}
                #get all possible moves from point my_pos
                if block ==2:
                    dir['D']=True
                else:
                    dir['D']=self.check_barrier(chess_board,x,y,2)
                if block ==0:
                    dir['U']=True
                else:
                    dir['U']=self.check_barrier(chess_board,x,y,0)
                if block ==3:
                    dir['L']=True
                else:
                    dir['L']=self.check_barrier(chess_board,x,y,3)
                if block ==1:
                    dir['R']=True
                else:
                    dir['R']=self.check_barrier(chess_board,x,y,1)
                

                for direc in dir:
                    if direc=='U':
                        if dir["U"] == False:
                            x2=x-1

                            if (x2,y) != old_pos and my_pos != adv_pos:
                                move_lis.append([str((x,y)),[str((x2,y)),'u']])
                                dir[direc] =(x2,y)

                    if direc=='D':
                        if dir["D"] == False:
                            x2=x+1
                            if (x2,y) != old_pos and my_pos != adv_pos:
                                move_lis.append([str((x,y)),[str((x2,y)),'d']])
                                dir[direc] =(x2,y)
                                
                    if direc=='L':
                        if dir["L"] == False:
                            y2=y-1
                            if (x,y2) != old_pos and my_pos != adv_pos:
                                move_lis.append([str((x,y)),[str((x,y2)),'l']])
                                dir[direc] =(x,y2)
                    if direc=='R':
                        if dir["R"] == False:
                            y2=y+1
                            if (x,y2) != old_pos and my_pos != adv_pos:
                                move_lis.append([str((x,y)),[str((x,y2)),'r']])
                                dir[direc] =(x,y2)
                #print(self.available)
                for i in dir:
                    if isinstance(dir[i],tuple) == True:
                        self.M = self.M -1
                        self.future_moves(dir[i],self.M,chess_board,block,adv_pos,move_lis,my_pos)

    def check_valid_step(self, start_pos, end_pos, barrier_dir,chess_board,adv_pos,max_step,moves):
        
        # Endpoint already has barrier or is boarder
        r, c = end_pos
        if chess_board[r, c, barrier_dir]:
            return False
        if np.array_equal(start_pos, end_pos):
            return True


        state_queue = [(start_pos, 0)]
        visited = {tuple(start_pos)}
        is_reached = False
        while state_queue and not is_reached:
            cur_pos, cur_step = state_queue.pop(0)
            r, c = cur_pos
            if cur_step == max_step:
                break
            for dir, move in enumerate(moves):
                if chess_board[r, c, dir]:
                    continue
                l,d=move
                next_pos = (l+r,c+d)
                if np.array_equal(next_pos, adv_pos) or tuple(next_pos) in visited:
                    continue
                if np.array_equal(next_pos, end_pos):
                    is_reached = True
                    break

                visited.add(tuple(next_pos))
                state_queue.append((next_pos, cur_step + 1))

        return is_reached