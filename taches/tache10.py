import tache3 as t3

adc = ADS7830()
servo = t3.ServoController()

current_angle = 90
servo.set_angle(0, current_angle)

while True:
    adc_value = adc.analogRead(1)

    if adc_value < 125:
        current_angle -= 5
    elif adc_value > 140:
        current_angle += 5

    current_angle = max(0, min(180, current_angle))

    servo.set_angle(0, current_angle)

    time.sleep(0.05)