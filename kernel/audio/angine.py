import click
import os

import time
def seconds_to_time(seconds: int) -> str:
    seconds = max(0, seconds)
    return time.strftime("%H:%M:%S", time.gmtime(seconds))

class Angine:
    def __init__(self, title=None, path=None, episode=None) -> None:
        self._title = title
        self._path = path
        self._episode = episode
        self._media = None
        self._player = None
        self._duration = -1 
        self._state = 0
        
        # ! add the current directory to the path to let ctypes find mvp-2.dll
        # ! before importing the module into memoryspace
 
        os.environ["PATH"] += os.pathsep + os.path.dirname(__file__)
        import mpv
        self.mpv = mpv
    
    
    @property
    def state(self) -> int:
        """int: the state of the player"""
        return self._state

    @property
    def title(self) -> str:
        """str: the title of the player"""
        return self._title

    def _create_player(self) -> None:
        """Creates the player object while making sure it is a valid file."""
        self._player = self.mpv.MPV()
        self._player.vid = False
        self._player.pause = False

        self._duration = 5

    def play(self) -> None:
        """Plays the media."""
        if self._player is None:
            self._create_player()

        self._player.play(self._path)

        self._player.pause = False
        self._state = 1

    def play_from(self, seconds) -> None:
        """play media from point."""
        if self._player is None:
            self._create_player()

        timestamp = seconds_to_time(seconds)
        self._player.start = timestamp

        self.play()

    def stop(self) -> None:
        """Stops the media."""
        if self._player is not None:
            self._player.terminate()
            self._state = 0

    def pause(self) -> None:
        """Pauses the media."""
        if self._player is not None:
            self._player.pause = True
            self._state = 2

    def seek(self, direction, amount) -> None:
        """Seek forward or backward in the media."""
        assert direction == 1 or direction == -1
        if self._player is not None:
            self._player.seek(direction * amount)

    def set_rate(self, rate) -> None:
        """Set the playback speed."""
        if self._player is not None:
            self._player.speed = rate

    def set_volume(self, volume) -> None:
        """Set the player volume."""
        if self._player is not None:
            self._player.volume = volume

    @property
    def duration(self) -> int:
        """int: the duration of the player"""
        result = 0
        if self._player is not None:
            d = self._player.duration
            result = 5000 if d is None else d * 1000
        return result

    @property
    def volume(self) -> int:
        """int: the volume of the player"""
        if self._player is not None:
            return self._player.volume

    @property
    def time(self) -> int:
        """int: the current time of the player"""
        if self._player is not None:
            t = self._player.time_pos
            return 0 if t is None else t * 1000

    @property
    def time_str(self) -> str:
        """str: the formatted time and duration of the player"""
        result = "00:00:00/00:00:00"
        if self._player is not None:
            time_seconds = int(self.time / 1000)
            length_seconds = int(self.duration / 1000)
            t = seconds_to_time(time_seconds)
            d = seconds_to_time(length_seconds)
            result = "%s/%s" % (t, d)
        return result


def test():
    s = os.path.abspath('dummy/au.mp3')
    player = Angine(path=s)
    player.play()

if __name__ == "__main__":
    s = os.path.abspath('dummy/au.mp3')
    player = Angine(path=s)
    player.play()
    # stop, duration = "", ""
    # duration = player.duration
    # # print(f"This is {duration} long")

    # while True:
    #     # click.clear()
    #     # print(f"Now playing: {player.time}")
    #     # if stop:
    #     #     # print(f"paused at {stop}")
    #     # else:
    #     #     # print("playing something...")
    #     i = input()
    #     if i == '!k':
    #         stop = player.time
    #         # print(f'Paused at {stop}')
    #         player.pause()
            
    #         continue
    #     elif i == 's':
    #         player.stop()
    #         break
    #     else:
    #         player.play_from(stop/1000)
    #         stop = 0
    #         continue