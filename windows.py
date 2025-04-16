import threading
import curses 


class Windows():
    def __init__(self):
        self.print_mutex = threading.Lock()
        self.input_win = None
        self.community_win = None 
        self.hand_win = None
        self.error_win = None

        curses.curs_set(1)
        curses.echo()
        
        # colors 
        curses.can_change_color()
        curses.start_color()
        curses.init_color(curses.COLOR_WHITE, 1000, 1000, 1000) # redefine white
        curses.init_color(8, 500, 500, 500) # grey 
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE) 
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, 8, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_WHITE)
        curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_WHITE)
    
    
    def init_windows(self, stdscr):
        height, width = stdscr.getmaxyx()
        input_height = 3
        output_height = height - input_height * 2
        self.hand_win = curses.newwin(output_height, int(width / 2), 0, 0)
        self.community_win = curses.newwin(output_height, int(width / 2), 0, int(width / 2))
        self.input_win = curses.newwin(input_height, width, output_height + 3, 0)
        self.error_win = curses.newwin(input_height, width, output_height, 0)

        self.hand_win.bkgd(' ', curses.color_pair(3))
        self.community_win.bkgd(' ', curses.color_pair(3))
        self.input_win.bkgd(' ', curses.color_pair(3))
        self.error_win.bkgd(' ', curses.color_pair(3))