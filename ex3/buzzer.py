from myhdl import delay, always, instance, Signal, intbv, always_seq


def Buzzer(alarm_act, alarm_out, clk1ms, alarm_toggle, compare, reset):
    """
    General Alarm Block
    :param alarm_act: alarm action output
    :param alarm_out: alarm output
    :param compare: alarm compare input
    :param alarm_toggle: alarm toggle input
    :param clk1ms: 1ms Clock Input
    :param reset: Reset input
    :return:
    """


    @instance
    def buzzz():
        while True:
            if not reset:
                print "reset"
                alarm_out.next = 0
                alarm_act.next = 0
            yield clk1ms.posedge, reset
            if alarm_toggle:
                if compare:
                    print "buzz buzz buzz"
                    alarm_act.next = 1
                    alarm_out.next = not alarm_out
            else:
                alarm_out.next = 0
                alarm_act.next = 0
    return buzzz
