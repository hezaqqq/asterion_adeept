import tache9 as t9
import tache5 as t5
import tache3 as t3
import time

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

        sensor = t5.Distance()
        robot = t9.RobotController(capteur=sensor)
        controller.set_angle(0, ANGLE_CENTER_ROUE)
        robot.demarrer()

        #robot = t9.RobotController(capteur=sensor)
        #controller.set_angle(0, ANGLE_CENTER_ROUE)
        #robot.demarrer()        

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

            distance = sensor.checkdist()

            if distance < 200 and distance > 0:
                if not avoiding:
                    if angle_tete_gd < ANGLE_CENTER_TETE_GD:
                        turn_direction = 1
                        controller.set_angle(0, ANGLE_MAX_ROUE) 
                    else:
                        # Obstacle à droite donc on tourne à gauche
                        turn_direction = -1
                        controller.set_angle(0, ANGLE_MIN_ROUE)
                    
                    avoiding = True
                    robot.demarrer()

            else:
                # Pas d'obstacles
                if avoiding:
                    avoiding = False
                    controller.set_angle(0, ANGLE_CENTER_ROUE)  
                else:
                    controller.set_angle(0, ANGLE_CENTER_ROUE)
                    robot.demarrer()

            time.sleep(0.05)

#            distance = sensor.checkdist()
#            if distance < 200:
#                print("Obstacle detected! Stopping the robot.")
#                robot.arreter()
#            else:
#                if not robot.en_marche:
#                    robot.demarrer()
    
    except KeyboardInterrupt:
        #robot.mc._set_all_motors(0)
        #robot.desactiver_feux()
        controller.set_angle(1, ANGLE_CENTER_TETE_GD)
        #robot.mc.pwm_motor.deinit()