import os
import socket			
from kernel.audio.angine import Angine, test
import zerorpc
from kernel.ipc_pipe import IPCPipe

def pprint(str:str)->None:
    with open('kernel.log', 'a') as log:
        log.write(str+'\n')

def bootstrap_kernel_old():
    # s = socket.socket()	
    # pprint ("Socket successfully created")

    # PORT = 62003
    # s.bind(('127.0.0.1', PORT))		
    # pprint ("socket binded to %s" %(PORT))

    # s.listen(5)	
    # pprint ("kernel is listening")		

    # while True:
    #     c, _ = s.accept()	
    #     req_len = int(c.recv(1024).decode('utf-8'))
    #     msg = b''
    #     while req_len:
    #         msg += c.recv(1024)
    #         req_len -= 1024
        
    #     pprint(msg.decode('utf-8'))
    #     c.close()

    #     s = os.path.abspath('dummy/au.mp3')
    #     player = Angine(path=s)
    #     player.play()
    #     while player._state == 1:
    #         pass
    #     continue
    pass

def bootstrap_kernel():
    pass

if __name__ == '__main__':
    bootstrap_kernel()
