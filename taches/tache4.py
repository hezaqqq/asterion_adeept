#!/usr/bin/env python3
import time
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import motor

# ── Initialisation ──────────────────────────────────────────
class MotorController:
    def __init__(self):
        self.i2c = busio.I2C(SCL, SDA)
        self.pwm_motor = PCA9685(self.i2c, address=0x5f)
        self.pwm_motor.frequency = 1000  # 1 kHz pour moteurs DC

        # Configuration des canaux pour les moteurs
        self.MOTOR_M1_IN1, self.MOTOR_M1_IN2 = 15, 14
        self.MOTOR_M2_IN1, self.MOTOR_M2_IN2 = 12, 13
        self.MOTOR_M3_IN1, self.MOTOR_M3_IN2 = 11, 10
        self.MOTOR_M4_IN1, self.MOTOR_M4_IN2 = 8, 9

        # Création des objets moteur
        self.motor1 = motor.DCMotor(self.pwm_motor.channels[self.MOTOR_M1_IN1], self.pwm_motor.channels[self.MOTOR_M1_IN2])
        self.motor2 = motor.DCMotor(self.pwm_motor.channels[self.MOTOR_M2_IN1], self.pwm_motor.channels[self.MOTOR_M2_IN2])
        self.motor3 = motor.DCMotor(self.pwm_motor.channels[self.MOTOR_M3_IN1], self.pwm_motor.channels[self.MOTOR_M3_IN2])
        self.motor4 = motor.DCMotor(self.pwm_motor.channels[self.MOTOR_M4_IN1], self.pwm_motor.channels[self.MOTOR_M4_IN2])
        
        for m in (self.motor1, self.motor2, self.motor3, self.motor4):
            m.decay_mode = motor.SLOW_DECAY


# Servo de direction sur le même PCA9685, canal 0
SERVO_CHANNEL = 0
SERVO_LEFT    = 3277
SERVO_CENTER  = 4915
SERVO_RIGHT   = 6554

# ── Fonctions internes ───────────────────────────────────────
def _map(self, x, in_min, in_max, out_min, out_max):
    return (x - in_min) / (in_max - in_min) * (out_max - out_min) + out_min

def _set_all_motors(self, throttle_value):
    for m in (self.motor1, self.motor2, self.motor3, self.motor4):
        m.throttle = throttle_value

def _set_servo(self, duty):
    self.pwm_motor.channels[SERVO_CHANNEL].duty_cycle = int(duty)

# ── Fonction de pilotage avec rampe ─────────────────────────
# throttle courant global (-1.0 a +1.0)
current_throttle = 0.0

def drive_ramp(self, target_throttle, ramp_time=1.0):
    # target_throttle : valeur signee -1.0 (arriere) a +1.0 (avant), 0=stop
    # ramp_time       : duree de la transition en secondes
    global current_throttle
    target_throttle = max(-1.0, min(1.0, target_throttle))
    steps = 100
    delay = ramp_time / steps
    for step in range(1, steps + 1):
        t = self._map(step, 0, steps, current_throttle, target_throttle)
        self._set_all_motors(t)
        time.sleep(delay)
    current_throttle = target_throttle
    if target_throttle > 0:
        print(f"[AVANT]   {round(target_throttle * 100)}%")
    elif target_throttle < 0:
        print(f"[ARRIERE] {round(abs(target_throttle) * 100)}%")
    else:
        print("[STOP]")

# ── Etalonnage servo ─────────────────────────────────────────
def calibrate_servo(self):
    print("\n=== ETALONNAGE SERVO ===")
    print("Le servo est place au centre theorique (duty=4915).")
    print("Commandes : l=gauche | r=droite | ok=terminer\n")
    self._set_servo(SERVO_CENTER)

    offset = 0
    step   = 50
    while True:
        cmd = input(f"  decalage={offset:+d} > ").strip().lower()
        if cmd == 'ok':
            print(f"\nDecalage mesure : {offset:+d} (soit duty={SERVO_CENTER + offset})")
            self._set_servo(SERVO_CENTER)   # remet au centre theorique avant de sortir
            break
        elif cmd == 'l':
            offset -= step
            self._set_servo(SERVO_CENTER + offset)
        elif cmd == 'r':
            offset += step
            self._set_servo(SERVO_CENTER + offset)

# ── Arret propre ─────────────────────────────────────────────
def destroy(self):
    self._set_all_motors(0)
    self.pwm_motor.deinit()

# ── Programme principal : commande manuelle ──────────────────
if __name__ == '__main__':
    speed = 25  # vitesse de base en %

    print("=== COMMANDE MANUELLE ===")
    print("  f/b  - avant/arriere   |  s  - stop")
    print("  +/-  - vitesse +-10%   |  c  - etalonner servo")
    print("  q    - quitter")
    print(f"  Vitesse de base = {speed}%  |  Rampe = 1s\n")

    try:
        while True:
            cmd = input("Commande > ").strip().lower()
            if cmd == 'q':
                break
            elif cmd == 'f':
                drive_ramp(speed / 100.0)
            elif cmd == 'b':
                drive_ramp(-speed / 100.0)
            elif cmd == 's':
                drive_ramp(0.0)
            elif cmd == '+':
                speed = min(100, speed + 10)
                # reapplique la meme direction avec la nouvelle vitesse
                if current_throttle > 0:
                    drive_ramp(speed / 100.0)
                elif current_throttle < 0:
                    drive_ramp(-speed / 100.0)
                print(f"  Vitesse -> {speed}%")
            elif cmd == '-':
                speed = max(5, speed - 10)
                if current_throttle > 0:
                    drive_ramp(speed / 100.0)
                elif current_throttle < 0:
                    drive_ramp(-speed / 100.0)
                print(f"  Vitesse -> {speed}%")
            elif cmd == 'c':
                calibrate_servo()
            else:
                print("  Commande inconnue.")
    except KeyboardInterrupt:
        pass
    finally:
        destroy()