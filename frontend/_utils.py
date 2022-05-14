import json
import socket
from typing import Dict
from uuid import uuid4

PORT = 62003

class InvalidReqBodyException(Exception):
    """
    Exception is raised when the input request object is
    either corrupted or invalid according to the jsonrpc
    specification as of May 13, 2022
    """
    pass

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

def pipe_to_kernel(obj:str=None)->str:
    """
    ? Send cmds to kernel via socket
    """
    global PORT
    while True:
        try:
            s = socket.socket()		
            s.connect(('127.0.0.1', PORT))
            s.send(obj.encode('utf-8'))
            s.close()
        except ConnectionRefusedError:
            break
        else:
            break

def get_rpc_req(req:Dict)->str:
    
    # begin make sure req_body req is specification valid --------------------------------------------------------
    if len(req.keys()) != 2:
        raise InvalidReqBodyException("Wrong No of keys")
    
    try:
        if (not isinstance(req['params'], list)) and (not isinstance(req['params'], str)):
            raise InvalidReqBodyException("Bad params")
        
        if not isinstance(req['method'], str):
            raise InvalidReqBodyException("Bad method value")
    except KeyError:
        raise InvalidReqBodyException("Key error in Req Body")
    except Exception as e:
        raise InvalidReqBodyException(e.__str__())
    # end make sure req_body req is specification valid ----------------------------------------------------------

    req['jsonrpc'] = '2.0'
    req['id'] = str(uuid4())

    return json.dumps(req)
    
