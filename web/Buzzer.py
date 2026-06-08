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
        self.HAPPY_BIRTHDAY_SONG = [
            ["G4", 0.3], ["G4", 0.3], ["A4", 0.3], ["G4", 0.3], ["C5", 0.3], ["B4", 0.6],
            ["G4", 0.3], ["G4", 0.3], ["A4", 0.3], ["G4", 0.3], ["D5", 0.3], ["C5", 0.6],
            ["G4", 0.3], ["G4", 0.3], ["C5", 0.3], ["B4", 0.3], ["C5", 0.3], ["B4", 0.3], ["A4", 0.6],
            ["F5", 0.3], ["F5", 0.3], ["B4", 0.3], ["C5", 0.3], ["D5", 0.3], ["C5", 0.6]
        ]
        self.SONG_1 = [
            # "Auf der Hei - de blüht ein klein - es"
            ["Ab4", 0.3], ["Eb4", 0.15], ["Eb4", 0.15],
            ["F4",  0.3], ["Eb4", 0.15], ["Eb4", 0.15],
            ["Eb4", 0.3], ["Bb4", 0.15], ["Bb4", 0.15],
            ["Ab4", 0.6],

            # "Blü - me - lein"
            ["Ab4", 0.3], ["Bb4", 0.15], ["Ab4", 0.15],
            ["Gb4", 0.3], ["Eb4", 0.15], ["Eb4", 0.15],
            ["Eb4", 0.6],

            # "Und das heißt"
            ["Eb4", 0.3], ["F4",  0.15], ["Eb4", 0.15],
            ["Gb4", 0.3], ["F4",  0.15], ["Eb4", 0.15],
            ["Eb4", 0.6],

            # "E - ri - ka"
            ["Eb4", 0.4], ["F4", 0.2],
            ["Gb4", 0.4], ["Eb4", 0.2],
            ["Ab4", 0.9],

            # "Heiß von hun-dert-tau-send klein-es"
            ["Ab4", 0.3], ["Bb4", 0.15], ["Ab4", 0.15],
            ["Gb4", 0.3], ["Eb4", 0.15], ["Eb4", 0.15],
            ["Eb4", 0.3], ["F4",  0.15], ["Eb4", 0.15],
            ["Db4", 0.6],

            # Continuation / ending phrase
            ["Db4", 0.3], ["Eb4", 0.15], ["Db4", 0.15],
            ["C4",  0.3], ["Bb3", 0.15], ["Bb3", 0.15],
            ["Bb3", 0.6],

            ["Bb3", 0.3], ["C4",  0.15], ["Bb3", 0.15],
            ["Db4", 0.3], ["C4",  0.15], ["Bb3", 0.15],
            ["Ab3", 0.9],
        ]
        self.__flag = threading.Event()
        self.__flag.clear()
        self.MusicMode = 0

        super(Player, self).__init__(*args, **kwargs)

    def play(self, tune):
        for note, duration in tune:
            if self.MusicMode == 0:
                break
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
                self.play(self.SONG_1)
            except KeyboardInterrupt:
                self.pause()
                print("Program terminated by user.")

if __name__ == "__main__":
    player = Player()
    player.start()
    player.start_playing() 
    time.sleep(5)
    player.pause()

