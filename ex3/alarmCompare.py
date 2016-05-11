from myhdl import delay, always, instance, Signal, intbv, always_seq


def AlarmCompare(time_mins1, time_mins10, time_hrs1, time_hrs10, alarm_mins1, alarm_mins10, alarm_hrs1, alarm_hrs10, compare):
    """
    AlarmCompare Block
    :param time_mins1: time minute input
    :param time_mins10: time 10th-minute input
    :param time_hrs1: time hour input
    :param time_hrs10: time 10th-hour input
    :param alarm_mins1: alarm minute input
    :param alarm_mins10: alarm 10th-minute input
    :param alarm_hrs1: alarm hour input
    :param alarm_hrs10: alarm 10th-hour input
    :param compare: output (high) if time==alarm-time
    :return:
    """

    #@always(time_mins1.posedge, time_mins10.posedge, time_hrs1.posedge, time_hrs10.posedge, alarm_mins1.posedge, alarm_mins10.posedge, alarm_hrs1.posedge, alarm_hrs10.posedge)
    @always(delay(500000))
    def alarmCompare():
            #print "Compare"
            if time_mins1 == alarm_mins1 and time_mins10 == alarm_mins10 and time_hrs1 == alarm_hrs1 and time_hrs10 == alarm_hrs10:
                print "enable"
                compare.next = 1
            else:
                compare.next = 0
    return alarmCompare