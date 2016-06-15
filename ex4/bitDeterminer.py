from myhdl import delay, always, instance, Signal, intbv, always_seq

def SignalValue(dcf_state, dcf_begin, dcf_sig, clk1ms, reset):

    counter_ms = Signal(intbv(0, min=0, max=1000))
    counter_overdue_ms = Signal(intbv(0, min=0, max=1000))
    counter_zeros = Signal(intbv(0, min=0, max=250))

    @instance
    def decode():
        while True:
            yield clk1ms.posedge, reset
            if not reset:
                counter_zeros.next = 0
                counter_ms.next = 0

            counter_ms.next = counter_ms + 1 if counter_ms < counter_ms.max -1 else 0
            
            if dcf_sig == 1:
                if counter_zeros < 50:
                    counter_overdue_ms.next = counter_overdue_ms + 1 if counter_overdue_ms < counter_overdue_ms.max -1 else 0
                    print "overdue counter:", counter_overdue_ms
                    if counter_overdue_ms > 800:
                        dcf_begin.next = 1
                        print "reset, 2s signal 1"
                else:
                    if counter_zeros < 150:
                        print "DCF: 0"
                        dcf_state.next = 0
                    else:
                        print "DCF: 1"
                        dcf_state.next = 1

            else:
                dcf_begin.next = 0
                counter_zeros.next = counter_zeros + 1 if counter_zeros < counter_zeros.max -1 else 0
                print counter_zeros
                dcf_state.next = dcf_state

            if counter_ms == counter_ms.max -1:
                print "ms counter full, resetting zero counter"
                counter_zeros.next = 0

    return decode