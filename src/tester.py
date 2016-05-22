####################################################################
####################################################################
####################################################################
######                                                        ######
######                                                        ######
######                Stepper Moter Driver                    ######
######                   Testing Module                       ######
######                                                        ######
######          Tramy Nguyen - Leandro Watanabe               ######
######                                                        ######
####################################################################
####################################################################
####################################################################

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
resoln = 1
direcn = 1
stpCnt = 24
# Pins
clkPin = 11
swtPin = 12
spiPin = 13
csPin = 37
mosiPin = 15
# Delays
clkSpeed = 25
clkDel = 1/(2 * clkSpeed)
spiDel = 4*clkDel

# 
class Clock:
    #
    def __init__(self, pin, delay):
        self.value = False
        self.pin = pin
        self.delay = delay
        self.subscribers = set()

    #
    def register(self, module):
        self.subscribers.add(module)

    #
    def toggle(self, value):
        self.value = value
        for subscriber in self.subscribers:
            subscriber.trigger(value)
#            
class SPI:
    #
    def __init__(self, mosiPin, csPin):
        self.isActive = False
        self.index = 0
        self.mosiPin = mosiPin
        self.csPin = csPin
        self.binary = []

    #    
    def trigger(self, value):
        if value and self.isActive:
            if self.index > 15:
                GPIO.output(self.mosiPin, False)
                GPIO.output(self.csPin, False)
                self.isActive = False
                print("Finished sending data")
            else:
                GPIO.output(self.mosiPin, self.binary[self.index])
                print("bit: " + str(self.index) + " = " + str(self.binary[self.index]))
                self.index = self.index + 1
    #
    def active(self, resolution, direction, count):
        print("Sending data")
        self.binary = self.inputToBinary(resolution, direction, count)
        self.index = 0
        self.isActive = True
        GPIO.output(self.csPin, True)
                
    ## Transform input to the SPI module into a binary list
    def inputToBinary(self, resolution, direction, count):   
        binary = [resolution, direction]
        for i in range(13,-1,-1):
            if count >= (1 << i):
                count = count - (1 << i)
                binary.append(1)
            else:
                binary.append(0)
        binary.reverse()
        return(binary)

# todo: don't let the user press this twice until the first is ready
def pushButton(self):
    spi_module.active(resoln, direcn, stpCnt)

#    
def setup():
    global global_clk, spi_clock, spi_module
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(swtPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(swtPin, GPIO.RISING, callback=pushButton, bouncetime=300)
    global_clk = Clock(clkPin, clkDel)
    GPIO.setup(clkPin, GPIO.OUT)
    spi_clock = Clock(spiPin, spiDel)
    GPIO.setup(spiPin, GPIO.OUT)    
    spi_module = SPI(mosiPin, csPin)
    spi_clock.register(spi_module)
    GPIO.setup(spi_module.mosiPin,GPIO.OUT)
    GPIO.setup(spi_module.csPin,GPIO.OUT)

#
def resetPins():
    GPIO.output(clkPin, 0)
    GPIO.output(spiPin, 0)
    GPIO.output(csPin, 0)
    GPIO.output(mosiPin, 0)
    
## Generate clock signal for the chip
def clock(clk):
    while isActive:
        GPIO.output(clk.pin, clk.value)
        time.sleep(clk.delay)
        clk.toggle(not(clk.value))

#
if __name__ == '__main__':
    global global_clk, spi_clock, spi_module
    print("Initialization\n")
    setup()
    try:
        print("Running code\n")
        clkThread = threading.Thread(target=clock, args=(global_clk,))
        spiThread = threading.Thread(target=clock, args=(spi_clock,))
        clkThread.start()
        spiThread.start()
        clkThread.join()
        spiThread.join()
    except KeyboardInterrupt:
        isActive = False
        resetPins()
        print("Cleaning up\n")
        GPIO.cleanup()
        print("Done\n")


