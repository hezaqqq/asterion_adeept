import tache1 as t1
import tache2 as t2
import tache3 as t3
import tache4 as t4
import tache5 as t5
import tache6 as t6

robot_led_controller = t1.RobotLEDController()
led_controller = t2.LEDController(led_count=14)
servo_controller = t3.ServoController()
servo_sequence = t3.ServoTester(servo_controller)
servo_manual = t3.ServoManual(servo_controller)
motor_controller = t4.MotorController()
line_follower = None  # Don't initialize - will be created fresh for each task 6 run


if __name__ == "__main__":
    action = input("Entrez les numeros de tache a executer separes d'un espace : ").strip().split()
    for i in range(len(action)):
        try:
            if action[i] == '1':
                t1.run()
            elif action[i] == '2':
                t2.run()
            elif action[i] == '3':
                t3.run()
            elif action[i] == '4':
                t4.run()
            elif action[i] == '5':
                t5.run()
            elif action[i] == '6':
                t6.run()
        except KeyboardInterrupt:
            print("\nTask interrupted by user")
            break
        except Exception as e:
            print(f"Error running task {action[i]}: {e}")
            # Cleanup GPIO resources if tasks have cleanup methods
            try:
                if hasattr(t5, 'distance_sensor') and hasattr(t5.distance_sensor, 'cleanup'):
                    t5.distance_sensor.cleanup()
            except:
                pass

