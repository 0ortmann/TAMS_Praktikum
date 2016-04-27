from myhdl import delay, always, instance, Signal, intbv, always_seq

def ClkDriver(clk1us):
    """
    Clock Source for 1us Clock
    :param clk1us: Output
    :return:
    """
    half_period = delay(500)

    @always(half_period)
    def drive_clk():
        clk1us.next = not clk1us

    return drive_clk

def Clock(clk1s, clk500ms, clk1ms, clk1us, reset):
    """
    General Clock Driver
    :param clk1s: 1s Clock Output
    :param clk500ms: 500ms Clock Output
    :param clk1ms:  1ms Clock Output
    :param clk1us: Clock input (1us)
    :param reset: Reset input
    :return:
    """
    counter_us = Signal(intbv(0, min=0, max=500))
    counter_ms = Signal(intbv(0, min=0, max=1000))
    print len(counter_ms)
    print len(counter_us)

    @always_seq(clk1us.posedge, reset)
    def clock():
        counter_us.next = counter_us + 1 if counter_us < counter_us.max -1 else 0
        #print counter_us, counter_us.max, counter_us == 0, counter_us.next

        if counter_us == 0:
            #print counter_us.next, counter_us
            clk1ms.next = not clk1ms

            counter_ms.next = counter_ms + 1 if counter_ms < counter_ms.max -1 else 0
            #print counter_ms, counter_ms.next
            if counter_ms == 0 or counter_ms == counter_ms.max // 2:
                clk500ms.next = not clk500ms

            if counter_ms == 0:
                clk1s.next = not clk1s
                print "0.5s"
        #print counter_us.next, counter_us, reset, reset.posedge
    return clock
