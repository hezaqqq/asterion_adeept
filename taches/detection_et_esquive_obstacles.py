import tache9 as t9
import tache5 as t5
import tache3 as t3
import threading
import time

ANGLE_CENTER_ROUE  = 100
ANGLE_MIN_ROUE     = 60
ANGLE_MAX_ROUE     = 140

ANGLE_CENTER_TETE_GD  = 108
ANGLE_MIN_TETE_GD     = 78
ANGLE_MAX_TETE_GD     = 138

if __name__ == "__main__":
    try:
        tete = t3.ServoController()
        angle_tete_gd = ANGLE_CENTER_TETE_GD
        tete.set_angle(1, angle_tete_gd)
        tete.set_angle(2, 85)
        gauche = True

        sensor = t5.Distance()

        while True:
            if angle_tete_gd < ANGLE_MAX_TETE_GD and gauche:
                angle_tete_gd += 1
            elif angle_tete_gd > ANGLE_MIN_TETE_GD and not gauche:
                angle_tete_gd -= 1
            elif angle_tete_gd >= ANGLE_MAX_TETE_GD:
                gauche = False
            elif angle_tete_gd <= ANGLE_MIN_TETE_GD:
                gauche = True
            tete.set_angle(1, angle_tete_gd)

            distance = sensor.checkdist()
            if distance < 200:
                print("Obstacle detected! Stopping the robot.")

            time.sleep(0.05)
    
    except KeyboardInterrupt:
        angle_tete_gd = ANGLE_CENTER_TETE_GD
        tete.set_angle(1, angle_tete_gd)
        pass  