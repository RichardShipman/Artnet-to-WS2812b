#!/usr/bin/env python3
# ArtNET to WS2812B led matrix mapper
# Author: Richard Shipman (richard@shipman.me.uk)
# Version 1.2 8th March 2024
# Fixed multi-universe fixtures, and non 0 universe start.
#
# Inspired by https://srsoftware.de/en/led-matrix

import time,socket,sys
from rpi_ws281x import *
import argparse

# LED strip configuration:
LED_COUNT      = 256      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 32     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
ONE_CHANNEL    = [13,19,41,45,53]

UDP_IP = "192.168.3.255"
UDP_PORT = 6454;

BASE_UNIVERSE = 0  # Base universe is DMX universe-1 for starting universe for strips.
LEDS_PER_UNIVERSE = 168  # adjust this depending on how qlc+ distributes your RGB matrix = max channel / LED_CHANNELS
LED_CHANNELS = 3  # 3 for RGB or 4 for RGBW, maybe 1 for single LEDs 

def b2i(bytes):
    result = 0
    for b in bytes:
        result = result*256+b
    return result

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=20):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('-b', '--brightness', type=int, help='set the brightness of the display')
    parser.add_argument('-u', '--universe', type=int, help='start the strip at this defined universe number')
    parser.add_argument('-l', '--leds', type=int, help='the number of RGB LEDs to be controlled')
    parser.add_argument('-p', '--pin', type=int, help='the pin for this strip of LEDs')
    parser.add_argument('-n', '--numperuni', type=int, help='the number of LEDs per universe')
    args = parser.parse_args()

    if (args.universe) and (args.universe<1024):
        BASE_UNIVERSE=args.universe

    if (args.leds) and (args.leds<4096):
        LED_COUNT=args.leds

    if (args.pin) and (args.pin<80):
        LED_PIN=args.pin

    if (args.numperuni) and (numperuni.pin<512/LED_CHANNELS):
        LEDS_PER_UNIVERSE=args.numperuni

    for test in ONE_CHANNEL:
        if test == LED_PIN:
            LED_CHANNEL=1
            break

    if (args.brightness) and (args.brightness<256):
        LED_BRIGHTNESS=args.brightness

    CHANNELS_PER_UNIVERSE = LED_CHANNELS*LEDS_PER_UNIVERSE
    END_UNIVERSE = BASE_UNIVERSE+((LED_COUNT*LED_CHANNELS)//CHANNELS_PER_UNIVERSE) 

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ("Universe: ",BASE_UNIVERSE," - ",END_UNIVERSE)
    print ("leds per uni: ",LEDS_PER_UNIVERSE,"*",LED_CHANNELS," ch per uni:",CHANNELS_PER_UNIVERSE)
    print ("Brightness: ",LED_BRIGHTNESS)
    print ("WS2812B leds: ",LED_COUNT)
    print ("pin: ",LED_PIN)

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    # set up socket listener bound to broadcast ArtNET port.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet / UDP
    sock.bind((UDP_IP, UDP_PORT))
    
    buf_size = 3*LED_COUNT;
    last_data = "";

    try:
        while True:
            data, addr = sock.recvfrom(3000);

#            print (data);
#            print ("ID   ",data[0:7]);
#            print ("OP Cd",data[8:9]);
#            print ("Pro V",data[10:11]);
#            print ("Seq  ",data[12]);
#            print ("Phys ",data[13]);
#            print ("Sub  ",data[14]);
#            print ("Net  ",data[15]);
#            print ("Len  ",data[16:17]);
            
#            header = data[0:7]
#            opcode = data[8:9]
#            protoV = data[10:11]
#            seq = b2i(data[12])
#            phys = b2i(data[13])

            length = b2i(data[16:17])
            if length == 0:
                continue
            universe = b2i(data[14:15])
#            print (universe, "rec ",BASE_UNIVERSE," ",END_UNIVERSE)
            
            if (universe >= BASE_UNIVERSE) and (universe <= END_UNIVERSE):
            
#                print (universe, "len: ", length)
#  i is counter to each led coloured pixel in the array.
                i=0;  
                while i<buf_size:
                    
# Work out which universe this led should be in
# Calculate offset from the base of the correct universe
                    ind = i
                    uni = BASE_UNIVERSE
                    if (ind >= CHANNELS_PER_UNIVERSE):
                       uni = ind // CHANNELS_PER_UNIVERSE + BASE_UNIVERSE
                       ind = ind % CHANNELS_PER_UNIVERSE

# Are we receiving the correct universe for this LED? 
#                    print ("universe ",universe," uni ",uni)	
                    if (universe == uni):
                       r=data[ind+18]
                       g=data[ind+19]
                       b=data[ind+20]
                       index=int((CHANNELS_PER_UNIVERSE*(universe-BASE_UNIVERSE)+ind)/LED_CHANNELS)
#                       print (universe, i, buf_size, len(data), r, g, b, index)
                       strip.setPixelColorRGB(index, r, g, b)
                    i+=LED_CHANNELS
                strip.show()

    except KeyboardInterrupt:
        sock.close()
        if args.clear:
            colorWipe(strip, Color(0,0,0), 0)

