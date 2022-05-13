import multiprocessing
import os		
import subprocess
from curses import wrapper
from kernel.kernel import bootstrap_kernel
import multiprocessing
from ui.main import main

def pprint(str:str)->None:
    with open('ui.log', 'w') as log:
        log.write(str)

def ui()->None:
    wrapper(main)


if __name__ == '__main__':
    bk = multiprocessing.Process(target=bootstrap_kernel)
    bk.start()
    # kernel = subprocess.Popen(['python', os.path.join('kernel','kernel.py')])
    ui()
    # kernel.terminate()
    bk.kill()
