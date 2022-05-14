import multiprocessing
from curses import wrapper
import zerorpc as rpc
from kernel.ipc_pipe import IPCPipe

from kernel.kernel import bootstrap_kernel
from frontend.main import main


def pprint(str:str)->None:
    with open('ui.log', 'w') as log:
        log.write(str)

def init_ui()->None:
    wrapper(main)

def boot_kernel():
    kernel_pipe = rpc.Server(IPCPipe())
    kernel_pipe.bind('tcp://0.0.0.0:62003')
    kernel_pipe.run()


if __name__ == '__main__':
    
    
    kernel = multiprocessing.Process(target=boot_kernel)
    kernel.start()

    init_ui()
    
    kernel.kill()
