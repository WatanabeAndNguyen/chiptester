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
csPin = 15
mosiPin = 16
# Delays
clkDel = 0.5
spiDel = 1.3


class Clock:
    def __init__(self, pin, delay):
        self.value = False
        self.pin = pin
        self.delay = delay
        self.subscribers = set()
    def register(self, module):
        self.subscribers.add(module)
    def toggle(self, value):
        self.value = value
        for subscriber in self.subscribers:
            subscriber.trigger(value)

class Switch:
    def __init__(self, pin):
        self.pin = pin
        self.subscribers = set()
    def register(self, module):
        self.subscribers.add(module)
    def toggle(self):
        for subscriber in self.subscribers:
            subscriber.trigger(value)
            
class SPI:
    def __init__(self, mosiPin, csPin, resolution, direction, count):
        self.isActive = False
        self.index = -1
        self.mosiPin = mosiPin
        self.csPin = csPin
        self.resolution = resolution
        self.direction = direction
        self.count = count
        self.binary = []
        
    def trigger(self, value):
        if value & self.isActive:
            if self.index < 0:
                GPIO.output(self.csPin, True)
            elif self.index < 16:
                GPIO.output(self.mosiPin, True)
                self.index = self.index + 1
            else:
                GPIO.output(self.csPin, False)
                isActive = False
            print('Triggered')
    def active():
        self.binary = inputToBinary(resolution, direction, count)
        self.isActive = True
    ## Transform input to the SPI module into a binary list
    def inputToBinary(resolution, direction, count):   
        binary = [resolution, direction]
        for i in range(13,-1,-1):
            if count >= (1 << i):
                count = count - (1 << i)
                binary.append(1)
            else:
                binary.append(0)
        binary.reverse()
        return(binary)

def setup()
    global global_clk, spi_clock, spi_module
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(swtPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(swtPin, GPIO.RISING, callback=toggle, bouncetime=300)
    global_clk = Clock(clkPin, clkDel)
    spi_clock = Clock(spiPin, spiDel)
    spi_module = SPI(mosiPin, csPin, resolution, direction, count)
## Generate clock signal for the chip
def clock(clk):
    while isActive:
        time.sleep(clk.delay)
        clk.toggle(not(clk.value))

if __name__ == '__main__':
    global global_clk, spi_clock, spi_module
    print("Initialization\n")

    try:
        print("Running code\n")
        clkThread = threading.Thread(target=global_clock, args=(global_clk))
        spiThread = threading.Thread(target=spi_clock, args=(spi_clock))
        clkThread.start()
        spiThread.start()
        clkThread.join()
        spiThread.join()
    except KeyboardInterrupt:
        isActive = False
        print("Cleaning up\n")
        GPIO.cleanup()
        print("Done\n")


