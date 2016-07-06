from myhdl import delay, always, instance, Signal, intbv, always_seq
from incrementor import increment

def Timer(time_secs1, time_secs10, time_mins1, time_mins10, time_hrs1, time_hrs10, clk1s, clk500ms, set_time, set_hrs, set_mins, dcf_load, dcf_hrs1, dcf_hrs10, dcf_mins1, dcf_mins10, reset):
    """
    General Clock Driver
    :param time_secs1: time seconds output
    :param time_secs10: time seconds output
    :param time_mins1: time minute output
    :param time_mins10: time 10th-minute output
    :param time_hrs1: time hour output
    :param time_hrs10: time 10th-hour output
    :param clk1s: 1s Clock Output
    :param clk500ms: 500ms Clock Output
    :param reset: Reset input
    :return:
    """

    @instance
    def clock():
        while True:
            if not reset:
                print "reset"
                time_hrs1.next = 0
                time_hrs10.next = 0
                time_mins1.next = 0
                time_mins10.next = 0
                time_secs1.next = 0
                time_secs10.next = 0
            if set_time:
                print "set time"
                yield clk500ms.posedge, reset
                if set_hrs:
                    increment(time_hrs1, time_hrs10, intbv(2), intbv(3))
                    time_mins10.next = time_mins10
                    time_mins1.next = time_mins1
                elif set_mins:
                    increment(time_mins1, time_mins10, intbv(6), intbv(9))
                    time_hrs10.next = time_hrs10
                    time_hrs1.next = time_hrs1
                time_secs10.next = 0
                time_secs1.next = 0
            if dcf_load:
                yield clk1s.posedge, reset, set_time
                print "load time values from DCF sender"
                time_hrs1.next = dcf_hrs1
                time_hrs10.next = dcf_hrs10
                time_mins1.next = dcf_mins1
                time_mins10.next = dcf_mins10
            else:
                print "wait clock"
                yield clk1s.posedge, reset, set_time
                print "Inc 1 s"
                increment(time_secs1, time_secs10, intbv(5), intbv(9))
                if time_secs1 == 9 and time_secs10 == 5:
                    increment(time_mins1, time_mins10, intbv(5), intbv(9))
                    if time_mins1 == 9 and time_mins10 == 5:
                        increment(time_hrs1, time_hrs10, intbv(2), intbv(3))
                    else:
                        time_hrs10.next = time_hrs10
                        time_hrs1.next = time_hrs1
                else:
                    time_mins10.next = time_mins10
                    time_mins1.next = time_mins1
                    time_hrs10.next = time_hrs10
                    time_hrs1.next = time_hrs1
            #print counter_us.next, counter_us, reset, reset.posedge
    return clock
