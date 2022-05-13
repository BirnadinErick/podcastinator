import os
import socket			
from kernel.audio.angine import Angine, test

def pprint(str:str)->None:
    with open('kernel.log', 'a') as log:
        log.write(str)

# next create a socket object
def bootstrap_kernel():
    s = socket.socket()		
    pprint ("Socket successfully created")

    PORT = 3000
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', PORT))		
    pprint ("socket binded to %s" %(PORT))

    s.listen(5)	
    pprint ("kernel is listening")		

    while True:
        c, _ = s.accept()	
        msg = c.recv(1024)
        
        pprint(msg.decode('utf-8'))
        c.close()

        s = os.path.abspath('dummy/au.mp3')
        player = Angine(path=s)
        player.play()
        while player._state == 1:
            pass
        continue

if __name__ == '__main__':
    bootstrap_kernel()
