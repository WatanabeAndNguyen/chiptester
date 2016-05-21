import RPi.GPIO as GPIO
import time
import threading

## Global variables
# States
isActive = True
# Clocks
clkVal = False
spiVal = False
# Data
resoln = 0
direcn = 0
stpCnt = 1
# Pins
clkPin = 11
swtPin = 12
spiPin = 13
# Delays
clkDel = 0.5
spiDel = 1.3

## Sets up the board
def setup():
    ## This sets mode to BOARD, which means we refer to pin rather than GPIO
    GPIO.setmode(GPIO.BOARD)
    ## Set the clock pin as an output
    GPIO.setup(clkPin, GPIO.OUT)
    ## Set the spi clock pin as an output
    GPIO.setup(spiPin, GPIO.OUT)
    ## Set the switch pin as an output
    GPIO.setup(swtPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #GPIO.add_event_detect(swtPin, GPIO.RISING, callback=toggleSwitch, bouncetime=300)


    
def mycallback(channel):
    global clkVal, clkPin
    GPIO.output(clkPin, clkVal)
    clkVal = not(clkVal)
        
def toggleSwitch():
    global swtPin
    while True:
        if GPIO.input(swtPin) == GPIO.HIGH:
            GPIO.output(clkPin, True)
        else:
            GPIO.output(clkPin, False)

## Generate clock signal for the chip
def global_clock(pin, delay):
    global clkVal
    while isActive:
        GPIO.output(pin, clkVal)
        time.sleep(delay)
        clkVal = not(clkVal)

## Generate clock signal for the chip
def spi_clock(pin, delay):
    global spiVal
    while isActive:
        GPIO.output(pin, spiVal)
        time.sleep(delay)
        spiVal = not(spiVal)

## Generate spi signal for the chip
def spi(spiPin, csPin, resolution, direction, count):
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




if __name__ == '__main__':
    print("Initialization\n")
    setup()
    try:
        #clock(clkPin, clkDel)
        #toggleSwitch()
        print("Running code\n")
        clkThread = threading.Thread(target=global_clock, args=(clkPin, clkDel))
        spiThread = threading.Thread(target=spi_clock, args=(spiPin, spiDel))
        clkThread.start()
        spiThread.start()
        clkThread.join()
        spiThread.join()
    except KeyboardInterrupt:
        isActive = False
        print("Cleaning up\n")
        GPIO.cleanup()
        print("Done\n")


