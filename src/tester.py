import RPi.GPIO as GPIO
import time

## Global variables
clkVal = FALSE
clkPin = 11
swtPin = 12

## This sets mode to BOARD, which means we refer to pin rather than GPIO
GPIO.setmode(GPIO.BOARD)
## Set the clock pin as an output
GPIO.setup(clkPin, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
## Set the switch pin as an output
GPIO.setup(swtPin, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)

## Do something when button is pressed
def toggleSwitch(pin):
    while True:
        if GPIO.input(pin) == GPIO.LOW:
            print("Switch pressed.")
            break

## Generate clock signal for the chip
def clock(pin, delay):
    global clk
    while True:
        GPIO.output(pin, TRUE)
        time.sleep(delay)
        clk = not(clk)
    
# GPIO.cleanup()

#    thread = Thread(target = toggleSwitch)
#    thread.start()
#    thread.join()
