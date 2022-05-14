import logging
import os

from kernel.audio.angine import Angine


class IPCPipe(object):

    def log_hello(self, str:str)->None:
        s = os.path.abspath('dummy/au.mp3')
        player = Angine(path=s)
        player.play()
        while player._state == 1:
            pass
