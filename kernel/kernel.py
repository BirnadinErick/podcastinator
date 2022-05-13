import socket			

def pprint(str:str)->None:
    with open('kernel.log', 'w') as log:
        log.write(str)

# next create a socket object
def bootstrap_kernel():
    s = socket.socket()		
    pprint ("Socket successfully created")

    PORT = 62003			

    s.bind(('127.0.0.1', PORT))		
    pprint ("socket binded to %s" %(PORT))

    s.listen(5)	
    pprint ("kernel is listening")		

    while True:
        c, _ = s.accept()	
        msg = c.recv(1024)
        
        pprint(msg.decode('utf-8'))

        c.close()
        continue

if __name__ == '__main__':
    bootstrap_kernel()
