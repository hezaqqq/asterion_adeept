import tache9 as t9
import tache5 as t5
import tache3 as t3
import threading
import time

ANGLE_CENTER_ROUE  = 100
ANGLE_MIN_ROUE     = 60
ANGLE_MAX_ROUE     = 140

if __name__ == "__main__":
    try:
        tete = t3.ServoController()
        tete.set_angle(2, 85)
        tete.set_angle(1, 105)
    
    except KeyboardInterrupt:
        pass  