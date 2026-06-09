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
["C4", 0.45],
            ["Db4", 0.15], 
            ["Eb4", 0.15], ["rest", 0.15],
            ["Eb4", 0.15], ["rest", 0.15], 
            ["Eb4", 0.15], ["rest", 0.15], 
            ["C5", 0.15],  ["rest", 0.15], 
            ["C5", 0.15],  ["rest", 0.15], 
            ["Eb5", 0.15], ["rest", 0.15], 
            ["C5", 0.45], 
            ["Bb5", 0.15], 
            ["Ab5", 0.15], ["rest", 0.15],
            ["Eb4", 0.15], ["rest", 0.15], 
            ["Eb4", 0.15], ["rest", 0.15], 
            ["Eb4", 0.15], ["rest", 0.15], 
            ["G4", 0.15],  ["rest", 0.15], 
            ["C5", 0.15],  ["rest", 0.15], 
            ["Eb5", 0.15], ["rest", 0.15], 
            ["Eb4", 0.15], ["rest", 0.15], 
            ["Eb4", 0.15], ["rest", 0.15], 
            ["Eb4", 0.15], ["rest", 0.15], 
            ["C5", 0.45], 
            ["Bb5", 0.15], 
            ["Ab5", 0.15], ["rest", 0.15],
            ["rest",0.1],
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