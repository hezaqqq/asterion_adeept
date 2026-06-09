import numpy
import spidev


class LEDController:

    def __init__(self, led_count=14):
        self.led_count = led_count
        self.led_red_offset = 1
        self.led_green_offset = 0
        self.led_blue_offset = 2

        self.led_brightness_list = [255] * self.led_count
        self.led_color = [0] * (self.led_count * 3)

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0) 
        self.spi.mode = 0

    def set_led_color_data(self, index, r, g, b, brightness=255):
        if not (0 <= index < self.led_count):
            return

        self.led_brightness_list[index] = brightness
        current_brightness = self.led_brightness_list[index]

        self.led_color[index * 3 + self.led_red_offset] = round(
            r * current_brightness / 255
        )
        self.led_color[index * 3 + self.led_green_offset] = round(
            g * current_brightness / 255
        )
        self.led_color[index * 3 + self.led_blue_offset] = round(
            b * current_brightness / 255
        )

        self.show()

    def show(self):
        d = numpy.array(self.led_color).ravel()
        tx = numpy.zeros(len(d) * 8, dtype=numpy.uint8)
        for ibit in range(8):
            tx[7 - ibit :: 8] = ((d >> ibit) & 1) * 0x78 + 0x80

        self.spi.xfer(tx.tolist(), int(8 / 1.25e-6))

    def turn_off_all(self):
        self.led_color = [0] * (self.led_count * 3)
        self.show()


if __name__ == "__main__":
    controller = LEDController(led_count=14)
    controller.turn_off_all()

    while True:
        try:
            commande = input().strip()
            if commande.upper() in ["Q", "0"]:
                controller.turn_off_all()
                break

            elements = commande.split()
            if len(elements) < 4:
                continue

            index = int(elements[0])
            r = int(elements[1])
            g = int(elements[2])
            b = int(elements[3])
            brightness = int(elements[4]) if len(elements) >= 5 else 255

            controller.set_led_color_data(index, r, g, b, brightness)

        except (KeyboardInterrupt, SystemExit):
            controller.turn_off_all()
            break
        except Exception:
            continue