python program to recieve DMX over Artnet

Written to run on Raspberry Pi.
You will need to set the correct broadcast IP address in the code for your network! Line 24 of the file.

1. Connect a strip/matrix of WS2812b multicolour LEDs to a pin on the Pi.
2. Connect power and ground to the Pi GPIO.
3. Connect 5 volts to the WS2812b strip/matrix, and it should power the pi as well.
4. Run the included python script with relevant options.
5. Send DMX commands over the artnet - I use the excellent QLC+ to send dmx commands
6. Relax and enjoy your light show.


usage: artnet.py [-h] [-c] [-b BRIGHTNESS] [-u UNIVERSE] [-l LEDS] [-p PIN] [-n NUMPERUNI]

options:
-  -h, --help            show this help message and exit
-  -c, --clear           clear the display on exit
-  -b BRIGHTNESS, --brightness BRIGHTNESS
                        set the brightness of the display - defaults to 32
-  -u UNIVERSE, --universe UNIVERSE
                        start the strip at this defined universe number - defaults to 0
-  -l LEDS, --leds LEDS  the number of RGB LEDs to be controlled - defaults to 256
-  -p PIN, --pin PIN     the pin for this strip of LEDs - defaults to 18
-  -n NUMPERUNI, --numperuni NUMPERUNI
                        the number of LEDs per universe - defaults to 168

The number of LEDs per universe will be defined by how your DMX controller allocates the LEDs in the Matrix
If using QLC+, create the RGB matrix, and then check in the Universes how many channels have been created per
Universe to give you the number of LEDs per universe.
                        
