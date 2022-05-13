import socket

def clear_refresh(scr):
    """
    Clears the screen and refreshes it
    * scr: screen
    """
    scr.clear()
    scr.refresh()

def f5(scr):
    """
    Refreshes the given screen
    """
    scr.refresh(scr)

def pprint(scr, str, attr,*pos,):
    """
    curses_screen.addstr wrapper
    * scr: screen, str: string to add
    * *args: other arguments that should go before the str
    ?        i.e. position/ attributes etc
    """
    scr.addstr(*pos, str,attr)

def pipe_to_kernel(obj:object=None)->object:
    s = socket.socket()		
    PORT = 62003
    s.connect(('127.0.0.1', PORT))
    s.send(obj.encode('utf-8')[:1024])
    s.close()