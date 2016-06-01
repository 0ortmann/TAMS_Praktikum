from myhdl import delay, always, instance, Signal, intbv, always_seq
import sevenSegment

code = [None] * 10
for key, val in sevenSegment.encoding.items():
    if 0 <= key <= 9:
        code[key] = int(val, 2)
code = tuple(code)


def bcd2led(led, bcd):
    led.next = code[int(bcd)]


def incrementInBounds(bitv):
    bitv.next = bitv + 1 if bitv < bitv.max -1 else 0

def signalToPlainBV(signal):
    bv = intbv(0, min=0, max=64)
    bv[signal] = 1
    return bv



def Outmux(sev_seg_digit, select_digit,
           time_secs1, time_secs10, time_mins1, time_mins10, time_hrs1, time_hrs10, alarm_mins1, alarm_mins10,
           alarm_hrs1, alarm_hrs10, set_alarm, clk1ms, reset):
    """
    General output multiplexer
    :param sev_seg_digit: decoded seven segment digit output
    :param select_digit: indicator which digit refers to sev_seg_digit output
    :param time_secs1: time seconds input
    :param time_secs10: time seconds input
    :param time_mins1: time minute input
    :param time_mins10: time 10th-minute input
    :param time_hrs1: time hour input
    :param time_hrs10: time 10th-hour input
    :param alarm_mins1: alarm minute input
    :param alarm_mins10: alarm 10th-minute input
    :param alarm_hrs1: alarm hour input
    :param alarm_hrs10: alarm 10th-hour input
    :param set_alarm: alarm set input
    :param clk1ms: 1ms Clock input
    :param reset: Reset input
    :return:
    """

    current_time_digit = Signal(intbv(0, min=0, max=6))
    current_alarm_digit = Signal(intbv(0, min=0, max=4))

    @instance
    def multiplex():
        while True:
            if not reset:
                print "reset"
            if set_alarm:
                # display alarm time
                print "wait clock"
                yield clk1ms.posedge, reset
                print "display alarm"
                incrementInBounds(current_alarm_digit)
                if current_alarm_digit == 0:
                    bcd2led(sev_seg_digit, alarm_hrs10)
                elif current_alarm_digit == 1:
                    bcd2led(sev_seg_digit, alarm_hrs1)
                elif current_alarm_digit == 2:
                    bcd2led(sev_seg_digit, alarm_mins10)
                elif current_alarm_digit == 3:
                    bcd2led(sev_seg_digit, alarm_mins1)
                select_digit.next = signalToPlainBV(current_alarm_digit)
            else:
                # display time
                print "wait clock"
                yield clk1ms.posedge, reset
                print "display next"
                incrementInBounds(current_time_digit)
                if current_time_digit == 0:
                    bcd2led(sev_seg_digit, time_hrs10)
                elif current_time_digit == 1:
                    bcd2led(sev_seg_digit, time_hrs1)
                elif current_time_digit == 2:
                    bcd2led(sev_seg_digit, time_mins10)
                elif current_time_digit == 3:
                    bcd2led(sev_seg_digit, time_mins1)
                elif current_time_digit == 4:
                    bcd2led(sev_seg_digit, time_secs10)
                elif current_time_digit == 5:
                    bcd2led(sev_seg_digit, time_secs1)
                select_digit.next = signalToPlainBV(current_time_digit)

    return multiplex
