from myhdl import delay, always, instance, Signal, intbv, always_seq


def Timer(time_secs1, time_secs10, time_mins1, time_mins10, time_hrs1, time_hrs10, clk1s, clk500ms, set_time, set_hrs, set_mins, reset):
    """
    General Clock Driver
    :param clk1s: 1s Clock Output
    :param clk500ms: 500ms Clock Output
    :param clk1ms:  1ms Clock Output
    :param clk1us: Clock input (1us)
    :param reset: Reset input
    :return:
    """

    def increment(lower, upper, max_upper, max_lower_on_upper):
        """
        Increments a two secment timer, with lower and upper the counters
        :param lower: the lower counter
        :param upper: the upper counter
        :param max_upper: the max value for the upper register
        :param max_lower_on_upper: the max value for the lower register if the upper register is max
        :return: bool if the counter as had an overflow in the last counting step
        """
        #a = intbv(9,min=0,max=10)
        #a = intbv(9 if upper != max_upper else max_lower_on_upper, min=0, max=10)
        if 9 == lower or (upper == max_upper and lower == max_lower_on_upper):
            upper.next = upper + 1 if upper < max_upper else 0
        if upper == max_upper:
            lower.next = lower + 1 if lower < max_lower_on_upper else 0
        else:
            lower.next = lower + 1 if lower < 9 else 0

    """ def is_overflow(lower, upper, max_upper, max_lower_on_upper):
        a = intbv(9 if upper != max_upper else max_lower_on_upper, min=0, max=10)
        return upper == max_upper and lower == a"""

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
                elif set_mins:
                    increment(time_mins1, time_mins10, intbv(6), intbv(9))
            else:
                print "wait clock"
                yield clk1s.posedge, reset, set_time
                print "Inc 1 s"
                increment(time_secs1, time_secs10, intbv(5), intbv(9))
                if time_secs1 == 9 and time_secs10 == 5:
                    increment(time_mins1, time_mins10, intbv(5), intbv(9))
                    if time_mins1 == 9 and time_mins10 == 5:
                        increment(time_hrs1, time_hrs10, intbv(2), intbv(3))
            #print counter_us.next, counter_us, reset, reset.posedge
    return clock
