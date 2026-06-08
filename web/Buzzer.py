#!/usr/bin/env python
# File name   : Buzzer.py
# Website     : www.Adeept.com
# Author      : Adeept
# Date        : 2025/04/19
from gpiozero import TonalBuzzer
import time
import threading

tb = TonalBuzzer(18)

class Player(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.ERIKA = [
            # "Auf der Hei-de blüht ein klei-nes Blü-me-lein"
            ["Eb4", 0.25],
            ["Ab4", 0.5], ["Ab4", 0.25], ["Bb4", 0.25],
            ["C5",  0.5], ["C5",  0.25], ["Bb4", 0.25],
            ["Ab4", 1.0],
            ["rest", 0.5],

            # "und das heißt... E-ri-ka"
            ["Bb4", 0.25], ["Bb4", 0.25],
            ["C5",  0.5],
            ["Ab4", 0.25], ["F4",  0.25],
            ["Eb4", 1.0],
            ["rest", 0.5],

            # "Heiß von hunderttausend kleinen Bienelein"
            ["Eb4", 0.25], ["Eb4", 0.25],
            ["Bb4", 0.5], ["Bb4", 0.25], ["C5",  0.25],
            ["Db5", 0.5], ["Db5", 0.25], ["C5",  0.25],
            ["Bb4", 1.0],
            ["rest", 0.5],

            # "wird umschwärmt und auserkoren... E-ri-ka"
            ["C5",  0.25], ["Bb4", 0.25],
            ["C5",  0.5],
            ["Ab4", 0.25], ["F4",  0.25],
            ["Eb4", 1.0],
            ["rest", 0.5],

            # "In der Heimat wohnt ein kleines Mägdelein"
            ["Eb4", 0.25],
            ["Ab4", 0.5], ["Ab4", 0.25], ["Bb4", 0.25],
            ["C5",  0.5], ["C5",  0.25], ["Bb4", 0.25],
            ["Ab4", 1.0],
            ["rest", 0.5],

            # "und das heißt... E-ri-ka"
            ["Bb4", 0.25], ["Bb4", 0.25],
            ["C5",  0.5],
            ["Ab4", 0.25], ["F4",  0.25],
            ["Eb4", 1.0],
            ["rest", 0.5],

            # "Dieses Mägdlein ist mein treues Schätzelein"
            ["Eb4", 0.25], ["Eb4", 0.25],
            ["Bb4", 0.5], ["Bb4", 0.25], ["C5",  0.25],
            ["Db5", 0.5], ["Db5", 0.25], ["C5",  0.25],
            ["Bb4", 1.0],
            ["rest", 0.5],

            # "und mein Glück heißt... E-ri-ka"
            ["C5",  0.25], ["Bb4", 0.25],
            ["C5",  0.5],
            ["Ab4", 0.25], ["F4",  0.25],
            ["Eb4", 1.0],
        ]

        self.__flag = threading.Event()
        self.__flag.clear()
        self.MusicMode = 0
        super(Player, self).__init__(*args, **kwargs)

    def play(self, tune):
        for note, duration in tune:
            if self.MusicMode == 0:
                break
            if note == "rest":
                tb.stop()
            else:
                tb.play(note)
            time.sleep(float(duration))
        tb.stop()

    def start_playing(self):
        self.MusicMode = 1
        self.resume()

    def pause(self):
        self.__flag.clear()
        tb.stop()
        self.MusicMode = 0

    def resume(self):
        self.__flag.set()

    def run(self):
        while True:
            self.__flag.wait()
            try:
                self.play(self.ERIKA)
            except KeyboardInterrupt:
                self.pause()
                print("Program terminated by user.")

if __name__ == "__main__":
    player = Player()
    player.start()
    player.start_playing()
    time.sleep(30)
    player.pause()