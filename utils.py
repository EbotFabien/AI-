from contextlib import contextmanager
import logging


@contextmanager
def all_logging_disabled(highest_level=logging.CRITICAL):
    """
    A context manager that will prevent any logging messages
    triggered during the body from being processed.
    :param highest_level: the maximum logging level in use.
      This would only need to be changed if a custom level greater than CRITICAL
      is defined.
    """
    # two kind-of hacks here:
    #    * can't get the highest logging level in effect => delegate to the user
    #    * can't get the current module-level override => use an undocumented
    #       (but non-private!) interface

    previous_level = logging.root.manager.disable

    logging.disable(highest_level)

    try:
        yield
    finally:
        logging.disable(previous_level)


'''if final_steps == None or bar == None:
            if self.recurs > 0:
                self.recurs-=1
                if final_steps == None:
                    final_steps = np.random.randint(0, max_step + 1)
                    mov_dir = np.random.randint(0, 4)
                    pos=(x+final_steps,y)
                    if self.boundary(pos,chess_board) == False:
                        if self.check_lock(chess_board,x,y) == True:
                            self.search_best_move(sort,my_pos,max_step,chess_board)
                    pos=(x-final_steps,y)
                    if self.boundary(pos,chess_board) == False:
                        if self.check_lock(chess_board,x,y) == True:
                            self.search_best_move(sort,my_pos,max_step,chess_board)
                    pos=(x,y-final_steps)
                    if self.boundary(pos,chess_board) == False:
                        if self.check_lock(chess_board,x,y) == True:
                            self.search_best_move(sort,my_pos,max_step,chess_board)
                    pos=(x,y+final_steps)
                    if self.boundary(pos,chess_board) == False:
                        if self.check_lock(chess_board,x,y) == True:
                            self.search_best_move(sort,my_pos,max_step,chess_board)
                if bar == None:
                    bar = np.random.randint(0, 4)
                    while self.check_barrier(chess_board,x,y,bar):
                        bar = np.random.randint(0, 4)
'''