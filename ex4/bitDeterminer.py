from myhdl import delay, always, instance, Signal, intbv, always_seq

def SignalValue(dfc_state, dcf_sig, clk1ms, reset):

    counter_ms = Signal(intbv(0, min=0, max=1000))
    counter_overdue_ms = Signal(intbv(0, min=0, max=1000))
    counter_zeros = Signal(intbv(0, min=0, max=250))

    @instance
    def decode():
        while True:
            yield clk1ms.posedge, reset
            if reset:
                counter_zeros.next = 0
                counter_ms = 0

            counter_ms.next = counter_ms + 1 if counter_ms < counter_ms.max -1 else 0
            
            if dfc_sig == 1:
                if counter_zeros == 0:
                    counter_overdue_ms.next = counter_overdue_ms + 1 if counter_overdue_ms < counter_overdue_ms.max -1 else 0
                    if counter_overdue_ms > 800:
                        dfc_state.next = 2
                    yield dcf_sig.negedge
                else:
                    if counter_zeros > 150:
                        dfc_state.next = 1

            else:
                counter_zeros.next = counter_zeros + 1 if counter_zeros < counter_zeros.max -1 else 0
                if counter_zeros < 150:
                    dfc_state.next = 0

            if counter_ms == counter_ms.max -1:
                counter_zeros.next = 0

    return decode