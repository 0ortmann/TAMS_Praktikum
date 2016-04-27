#! /usr/bin/env python

from clock import ClkDriver, Clock

from myhdl import Signal, toVHDL, traceSignals, Simulation, ResetSignal

if __name__ == "__main__":
    #ones_led = Signal(intbv(0)[7:])
    reset = ResetSignal(1, active=0, async=True)
    clk1us = Signal(bool(0))
    clk1ms = Signal(bool(0))
    clk500ms = Signal(bool(0))
    clk1s = Signal(bool(0))

    clkDriver = ClkDriver(clk1us)

    clock = Clock(clk1s, clk500ms, clk1ms, clk1us, reset)

    sim = Simulation(clkDriver, clock)

    #toVHDL(Clock, clk1s, clk500ms, clk1ms, clk1us, reset)
    traceSignals(Clock, clk1s, clk500ms, clk1ms, clk1us, reset)
    sim.run(9000000*500)
