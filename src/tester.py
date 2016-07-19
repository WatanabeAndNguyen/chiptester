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
clkFreq = 25
clkDel = 1/(2 * clkFreq)
spiDel = 4*clkDel

# This class defines a clock. Every clock is associated with a GPIO pin and
# a delay that determines the clock frequency. It is possible to register 
# modules that get updated every time clock changes.
class Clock:

    # Construct clock.
    def __init__(self, pin, delay):
        self.value = False
        self.pin = pin
        self.delay = delay
        self.subscribers = set()

    # Register modules that will listen to this clock.
    def register(self, module):
        self.subscribers.add(module)

    # When clock changes, the module subscribers should get updated.
    def toggle(self, value):
        self.value = value
        for subscriber in self.subscribers:
            subscriber.trigger(value)

# This class defines the SPI module for the stepper motor driver. It has
# two outputs: mosi and cs. The mosi signal is used to transmit serial data to
# the chip and the cs signal indicates when data is being transmitted.            
class SPI:

    # Construct the SPI module
    def __init__(self, mosiPin, csPin):
        self.isActive = False
        self.index = 0
        self.mosiPin = mosiPin
        self.csPin = csPin
        self.binary = []

    # On a positive SPI clock edge, the SPI module is triggered and the values are
    # updated if the module is in the active state. The active state indicates the
    # module is in the process of sending serial data to the chip and is not yet
    # done. The signals of the SPI module will be triggered for 16 cycles after it
    # enters then active state. Once the the data has been fully transmitted, the
    # SPI module will be inactive. 
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

    # When the user requests to send signal to the chip, this method will prepare the
    # SPI module to begin sending data. 
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

# There is a switch button that is used to request data to be sent to the chip.
# This method checks if the user has pressed a button. If so, data will be sent
# to the chip. While data is being transmitted to the user, other requests will
# be ignored.
def pushButton(self):
    if not(spi_module.isActive):
        spi_module.active(resoln, direcn, stpCnt)

#  This method sets up the GPIOs.
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

# This method clears up the output values,
def resetPins():
    GPIO.output(clkPin, 0)
    GPIO.output(spiPin, 0)
    GPIO.output(csPin, 0)
    GPIO.output(mosiPin, 0)
    
# Generates clock signal for the chip
def clock(clk):
    while isActive:
        GPIO.output(clk.pin, clk.value)
        time.sleep(clk.delay)
        clk.toggle(not(clk.value))

# Each clock is run in a different thread. When stopping the program with a keyboard interrupt,
# the pins are resetted.
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
        spi_module.isActive = False
        print("Cleaning up\n")
        GPIO.cleanup()
        print("Done\n")


