#!/usr/bin/python

from myhdl import *
import sevenSegment


code = [None] * 10
for key, val in sevenSegment.encoding.items():
    if 0 <= key <= 9:
        code[key] = int(val, 2)
code = tuple(code)

def bcd2led(led, bcd, clock):

    @always(clock.posedge)
    def logic():
        led.next = code[int(bcd)]
        #print("{:07b}".format(int(led.next)))

    return logic


def ClkDriver(clk):

    halfPeriod = delay(1)

    @always(halfPeriod)
    def driveClk():
        clk.next = not clk

    return driveClk


def TimeCount(ones, reset, clock):
	
	@instance
	def count():
		while True:
			yield clock.posedge, reset.posedge

			if reset: ones.next = 0
			else: ones.next = ones + 1 if ones < 9 else 0
			#print(ones)
			#print("%s counter" % now())

	return count



def SimpleWatch(ones_led, reset, clock):
	ones = Signal(intbv(0)[4:])
	counter = TimeCount(ones, reset, clock)
	bcd2led_ones = bcd2led(ones_led, ones, clock)
	return counter, bcd2led_ones



ones_led = Signal(intbv(0)[7:])
reset, clock = [Signal(bool(0)) for i in range(2)]

clkDriver = ClkDriver(clock)

watch = SimpleWatch(ones_led, reset, clock)
sim = Simulation(clkDriver, watch)



toVHDL(SimpleWatch, ones_led, reset, clock)
traceSignals(SimpleWatch, ones_led, reset, clock)
sim.run(30)