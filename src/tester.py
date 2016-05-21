import RPi.GPIO as GPIO
import time

## Global variables
# Values
clkVal = False
spiVal = False
resoln = 0
direcn = 0
stpCnt = 1
# Pins
clkPin = 11
swtPin = 12
# Delays
clkDel = 2
spiDel = 3

## This sets mode to BOARD, which means we refer to pin rather than GPIO
#GPIO.setmode(GPIO.BOARD)
## Set the clock pin as an output
#GPIO.setup(clkPin, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)
## Set the switch pin as an output
#GPIO.setup(swtPin, GPIO.OUT, pull_up_down = GPIO.PUD_DOWN)

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

## Generate spi signal for the chip
def spi(spiPin, csPin, resololution, direction, count):
    binary = inputToBinary(resolution, direction, count)
    GPIO.output(csPin, True)
    GPIO.output(csPin, False)

## Transform input to the SPI module into a binary list
def inputToBinary(resolution, direction, count):   
    binary = [resolution, direction]
    for i in range(13,-1,-1):
        if count >= (1 << i):
            count = count - (1 << i)
            binary.append(1)
        else:
            binary.append(0)
    return(binary)


print(inputToBinary(0,0,3))
# GPIO.cleanup()

#    thread = Thread(target = toggleSwitch)
#    thread.start()
#    thread.join()
