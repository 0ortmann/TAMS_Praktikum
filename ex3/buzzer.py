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

    # local memory for alarm toggle
    #buzzer_enabled = Signal(bool(0))

    @instance
    def buzzz():
        while True:
            if not reset:
                alarm_out.next = 0
                alarm_act.next = 0
            yield clk1ms.posedge, reset, compare, alarm_toggle
            if compare == 1 and alarm_toggle == 1:
                print "buzz buzz buzz"
                alarm_act.next = 1
                alarm_out.next = not alarm_out
            else:
                alarm_out.next = 0
                alarm_act.next = 0
    return buzzz
