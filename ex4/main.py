#! /usr/bin/env python

from clock import ClkDriver, Clock
from timer import Timer
from alarm import Alarm
from alarmCompare import AlarmCompare
from buzzer import Buzzer
from outmux import Outmux
from bitDeterminer import SignalValue
from dcf77gen import dcf_time_gen, dcf_signal_gen
from decodeDCF import DCFDecoder

from myhdl import Signal, toVHDL, traceSignals, Simulation, ResetSignal, toVerilog, intbv

if __name__ == "__main__":
    #ones_led = Signal(intbv(0)[7:])
    reset = ResetSignal(1, active=0, async=True)
    clk1us = Signal(bool(1))
    clk1ms = Signal(bool(0))
    clk500ms = Signal(bool(0))
    clk1s = Signal(bool(0))
    set_time = Signal(bool(0))
    set_ala = Signal(bool(0))
    set_hrs = Signal(bool(1))
    set_mins = Signal(bool(0))

    tim_sender_secs1 = Signal(intbv(8, min=0, max=10))
    tim_sender_secs10 = Signal(intbv(5, min=0, max=6))
    tim_sender_mins1 = Signal(intbv(9, min=0, max=10))
    tim_sender_mins10 = Signal(intbv(5, min=0, max=6))
    tim_sender_hrs1 = Signal(intbv(1, min=0, max=10))
    tim_sender_hrs10 = Signal(intbv(2, min=0, max=3))

    tim_secs1 = Signal(intbv(8, min=0, max=10))
    tim_secs10 = Signal(intbv(5, min=0, max=6))
    tim_mins1 = Signal(intbv(9, min=0, max=10))
    tim_mins10 = Signal(intbv(5, min=0, max=6))
    tim_hrs1 = Signal(intbv(1, min=0, max=10))
    tim_hrs10 = Signal(intbv(2, min=0, max=3))

    ala_mins1 = Signal(intbv(9, min=0, max=10))
    ala_mins10 = Signal(intbv(5, min=0, max=6))
    ala_hrs1 = Signal(intbv(1, min=0, max=10))
    ala_hrs10 = Signal(intbv(2, min=0, max=3))
    compare = Signal(bool(0))
    alarm_toggle = Signal(bool(1))
    alarm_act = Signal(bool(0))
    alarm_out = Signal(bool(0))
    sev_seg_digit = Signal(intbv(0, min=0, max=128))
    select_digit = Signal(intbv(0, min=0, max=64))
    dcf_state = Signal(intbv(0, min=0, max=2))
    dcf_begin = Signal(intbv(0, min=0, max=2))
    dcf_sig = Signal(intbv(0, min=0, max=2))
    dcf_bit = Signal(intbv(0, min=0, max=3))

    dcf_hrs1 = Signal(intbv(0, min=0, max=4))
    dcf_hrs10 = Signal(intbv(0, min=0, max=2))
    dcf_mins1 = Signal(intbv(0, min=0, max=4))
    dcf_mins10 = Signal(intbv(0, min=0, max=3))
    dcf_signal_ok = Signal(intbv(0, min=0, max=2))
    dcf_load = Signal(intbv(0, min=0, max=2))


    clkDriver = ClkDriver(clk1us)

    clock = Clock(clk1s, clk500ms, clk1ms, clk1us, reset)

    # sender timeblock for dcf generation:
    # dcf_load has to be 0 for the sender to work
    timblk_sender = Timer(tim_sender_secs1, tim_sender_secs10, tim_sender_mins1, tim_sender_mins10, tim_sender_hrs1, tim_sender_hrs10, clk1s, clk500ms, set_time, set_hrs, set_mins, dcf_load, dcf_hrs1, dcf_hrs10, dcf_mins1, dcf_mins10, reset)
    
    timblk_receiver = Timer(tim_secs1, tim_secs10, tim_mins1, tim_mins10, tim_hrs1, tim_hrs10, clk1s, clk500ms, set_time, set_hrs, set_mins, dcf_load, dcf_hrs1, dcf_hrs10, dcf_mins1, dcf_mins10, reset)
    
    alarm = Alarm(ala_mins1, ala_mins10, ala_hrs1, ala_hrs10, clk500ms, set_ala, set_hrs,
           set_mins, reset)
    compblk = AlarmCompare(tim_mins1, tim_mins10, tim_hrs1, tim_hrs10, ala_mins1, ala_mins10, ala_hrs1, ala_hrs10, compare)
    buz = Buzzer(alarm_act, alarm_out, clk1ms, alarm_toggle, compare, reset)

    outmux = Outmux(sev_seg_digit, select_digit, tim_secs1, tim_secs10, tim_mins1, tim_mins10, tim_hrs1, tim_hrs10,
                    ala_mins1, ala_mins10, ala_hrs1, ala_hrs10, set_ala, clk1ms, reset)


    dcf_generator = dcf_time_gen(clk1s, tim_sender_mins1, tim_sender_mins10, tim_sender_hrs1, tim_sender_hrs10, dcf_bit, reset)
    dcf_signal = dcf_signal_gen(clk1ms, dcf_bit, dcf_sig, reset)

    signal_value = SignalValue(dcf_state, dcf_begin, dcf_sig, clk1ms, reset)
    decoder = DCFDecoder(dcf_load, dcf_signal_ok, dcf_hrs1, dcf_hrs10, dcf_mins1, dcf_mins10,
        dcf_begin, dcf_state, clk1s, reset)


    sim = Simulation(clkDriver, clock, timblk_sender, dcf_generator, dcf_signal, signal_value, decoder)

    #toVHDL(Clock, clk1s, clk500ms, clk1ms, clk1us, reset)
    #toVHDL(Timer, tim_secs1, tim_secs10, tim_mins1, tim_mins10, tim_hrs1, tim_hrs10, clk1s, clk500ms, set_time, set_hrs, set_mins, dcf_load, dcf_hrs1, dcf_hrs10, dcf_mins1, dcf_mins10, reset)
    #toVHDL(Alarm, ala_mins1, ala_mins10, ala_hrs1, ala_hrs10, clk500ms, set_ala, set_hrs, set_mins, reset)
    #toVHDL(Buzzer, alarm_act, alarm_out, clk1ms, alarm_toggle, compare, reset)
    #toVHDL(Outmux, sev_seg_digit, select_digit, tim_secs1, tim_secs10, tim_mins1, tim_mins10, tim_hrs1, tim_hrs10,
                    #ala_mins1, ala_mins10, ala_hrs1, ala_hrs10, set_ala, clk1ms, reset)
    #toVerilog(Timer, tim_secs1, tim_secs10, tim_mins1, tim_mins10, tim_hrs1, tim_hrs10, clk1s, clk500ms, set_time, set_hrs, set_mins, dcf_load, dcf_hrs1, dcf_hrs10, dcf_mins1, dcf_mins10, reset)
    #toVerilog(Clock, clk1s, clk500ms, clk1ms, clk1us, reset)
    #traceSignals(Clock, clk1s, clk500ms, clk1ms, clk1us, reset)
    #traceSignals(Timer, tim_secs1, tim_secs10, tim_mins1, tim_mins10, tim_hrs1, tim_hrs10, clk1s, clk500ms, set_time, set_hrs,
    #   set_mins, dcf_load, dcf_hrs1, dcf_hrs10, dcf_mins1, dcf_mins10, reset)
    #traceSignals(Alarm, ala_mins1, ala_mins10, ala_hrs1, ala_hrs10, clk500ms, set_ala, set_hrs,
    #       set_mins, reset)
    #traceSignals(AlarmCompare, tim_mins1, tim_mins10, tim_hrs1, tim_hrs10, ala_mins1, ala_mins10, ala_hrs1, ala_hrs10, compare)
    #traceSignals(Buzzer, alarm_act, alarm_out, clk1ms, alarm_toggle, compare, reset)
    #traceSignals(Outmux, sev_seg_digit, select_digit, tim_secs1, tim_secs10, tim_mins1, tim_mins10, tim_hrs1, tim_hrs10,
    #                ala_mins1, ala_mins10, ala_hrs1, ala_hrs10, set_ala, clk1ms, reset)
    #traceSignals(dcf_time_gen, clk1s, tim_sender_mins1, tim_sender_mins10, tim_sender_hrs1, tim_sender_hrs10, dcf_bit, reset)
    #traceSignals(dcf_signal_gen, clk1ms, dcf_bit, dcf_sig, reset)
    #traceSignals(SignalValue, dcf_state, dcf_begin, dcf_sig, clk1ms, reset)
    traceSignals(DCFDecoder, dcf_load, dcf_signal_ok, dcf_hrs1, dcf_hrs10, dcf_mins1, dcf_mins10, dcf_begin, dcf_state, clk1s, reset)
    sim.run(10 * 1000000*1000)
    #sim.run(5 * 1000000*1000)
