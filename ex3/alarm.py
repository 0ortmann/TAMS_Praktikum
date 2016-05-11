from myhdl import delay, always, instance, Signal, intbv, always_seq
from incrementor import increment


def Alarm(alarm_mins1, alarm_mins10, alarm_hrs1, alarm_hrs10, clk500ms, set_alarm, set_hrs, set_mins, reset):
    """
    General Alarm Block
    :param alarm_mins1: alarm minute output
    :param alarm_mins10: alarm 10th-minute output
    :param alarm_hrs1: alarm hour output
    :param alarm_hrs10: alarm 10th-hour output
    :param clk500ms: 500ms Clock Input
    :param set_alarm: alarm set input
    :param set_mins: alarm minute input
    :param set_hrs: alarm hour input
    :param reset: Reset input
    :return:
    """


    @instance
    def clock():
        while True:
            if not reset:
                print "reset"
                alarm_hrs1.next = 0
                alarm_hrs10.next = 0
                alarm_mins1.next = 0
                alarm_mins10.next = 0
            if set_alarm:
                print "set alarm"
                yield clk500ms.posedge, reset
                print "increment alarm "
                if set_hrs:
                    print "hrs"
                    increment(alarm_hrs1, alarm_hrs10, intbv(2), intbv(3))
                elif set_mins:
                    print "min"
                    increment(alarm_mins1, alarm_mins10, intbv(6), intbv(9))
            else:
                yield set_alarm.posedge, reset
    return clock
