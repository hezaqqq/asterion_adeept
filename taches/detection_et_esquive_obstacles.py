import tache9 as t9
import tache5 as t5
import tache3 as t3
import time

import threading

ANGLE_CENTER_ROUE = 100
ANGLE_MIN_ROUE = 60
ANGLE_MAX_ROUE = 140

ANGLE_CENTER_TETE_GD = 108
ANGLE_MIN_TETE_GD = 78
ANGLE_MAX_TETE_GD = 138

if __name__ == "__main__":
    try:
        controller = t3.ServoController()
        angle_tete_gd = ANGLE_CENTER_TETE_GD
        controller.set_angle(1, angle_tete_gd)
        controller.set_angle(2, 85)
        gauche = True

        robot = t9.RobotController()
        controller.set_angle(0, ANGLE_CENTER_ROUE)
        robot.demarrer()     

        while True:
            if angle_tete_gd < ANGLE_MAX_TETE_GD and gauche:
                angle_tete_gd += 1
            elif angle_tete_gd > ANGLE_MIN_TETE_GD and not gauche:
                angle_tete_gd -= 1
            elif angle_tete_gd >= ANGLE_MAX_TETE_GD:
                gauche = False
            elif angle_tete_gd <= ANGLE_MIN_TETE_GD:
                gauche = True
            controller.set_angle(1, angle_tete_gd)

            time.sleep(0.05)

            threading.Thread(target=robot._surveiller_distance, daemon=True).start()
    
    except KeyboardInterrupt:
        robot.mc._set_all_motors(0)
        robot.desactiver_feux()
        controller.set_angle(1, ANGLE_CENTER_TETE_GD)
        robot.mc.pwm_motor.deinit()