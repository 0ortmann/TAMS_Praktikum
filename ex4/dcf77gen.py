from myhdl import delay, always, instance, Signal, intbv, always_seq


def dcf_time_gen(clk1s, time_min1, time_min10, time_hrs1, time_hrs10, dcf_bit, reset):

    sekunde = Signal(intbv(27, min=0, max=60))

    @instance
    def gen():
        while True:
            if not reset:
                dcf_bit.next = 2
            yield clk1s.posedge, reset
            sekunde.next = sekunde +1 if sekunde < sekunde.max -1 else 0
            if sekunde == 0:
                dcf_bit.next = 0
            elif sekunde == 1:
                dcf_bit.next = 1
            elif sekunde == 0:
                dcf_bit.next = 0
            elif sekunde == 1:
                dcf_bit.next = 1
            elif sekunde == 1:
                dcf_bit.next = 1
            elif 4 < sekunde <= 14:  # unused
                dcf_bit.next = 0

            elif sekunde == 15:
                dcf_bit.next = 0
            elif sekunde == 16:
                dcf_bit.next = 0 # zeitsprung
            elif sekunde == 17:
                dcf_bit.next = 1 # bit 2 + utc
            elif sekunde == 18:
                dcf_bit.next = 0 # bit 1 + utc
            elif sekunde == 19:
                dcf_bit.next = 0  # schaltsekunde
            elif sekunde == 20:
                dcf_bit.next = 1  # start zeitkodirung
            elif sekunde == 21:
                dcf_bit.next = (time_min1 >> 0) & 0b01
            elif sekunde == 22:
                dcf_bit.next = (time_min1 >> 1) & 0b01
            elif sekunde == 23:
                dcf_bit.next = (time_min1 >> 2) & 0b01
            elif sekunde == 24:
                dcf_bit.next = (time_min1 >> 3) & 0b01
            elif sekunde == 25:
                dcf_bit.next = (time_min10 >> 0) & 0b01
            elif sekunde == 26:
                dcf_bit.next = (time_min10 >> 1) & 0b01
            elif sekunde == 27:
                dcf_bit.next = (time_min10 >> 2) & 0b01
            elif sekunde == 28:
                dcf_bit.next = ((time_min1 >> 0) & 0b01 + (time_min1 >> 1) & 0b01 + (time_min1 >> 2) & 0b01 + (time_min1 >> 3) & 0b01 +
                                    (time_min10 >> 0) & 0b01 + (time_min10 >> 1) & 0b01 +(time_min10 >> 2) & 0b01) % 2
            elif sekunde == 29:
                dcf_bit.next = (time_hrs1 >> 0) & 0b01
            elif sekunde == 30:
                dcf_bit.next = (time_hrs1 >> 1) & 0b01
            elif sekunde == 31:
                dcf_bit.next = (time_hrs1 >> 2) & 0b01
            elif sekunde == 32:
                dcf_bit.next = (time_hrs1 >> 3) & 0b01
            elif sekunde == 33:
                dcf_bit.next = (time_hrs10 >> 0) & 0b01
            elif sekunde == 34:
                dcf_bit.next = (time_hrs10 >> 1) & 0b01
            elif sekunde == 35:
                dcf_bit.next = ((time_hrs1 >> 0) & 0b01 + (time_hrs1 >> 1) & 0b01 + (time_hrs1 >> 2) & 0b01 + (time_hrs1 >> 3) & 0b01 + (time_hrs10 >> 0) & 0b01 + (time_hrs10 >> 1) & 0b01) % 2
            elif sekunde == 36:
                dcf_bit.next = 0
            elif sekunde == 37:
                dcf_bit.next = 0
            elif sekunde == 38:
                dcf_bit.next = 0
            elif sekunde == 39:
                dcf_bit.next = 0
            elif sekunde == 40:
                dcf_bit.next = 0
            elif sekunde == 41:
                dcf_bit.next = 0
            elif sekunde == 42:
                dcf_bit.next = 0
            elif sekunde == 43:
                dcf_bit.next = 0
            elif sekunde == 44:
                dcf_bit.next = 0
            elif sekunde == 45:
                dcf_bit.next = 0
            elif sekunde == 46:
                dcf_bit.next = 0
            elif sekunde == 047:
                dcf_bit.next = 0
            elif sekunde == 48:
                dcf_bit.next = 0
            elif sekunde == 49:
                dcf_bit.next = 0
            elif sekunde == 50:
                dcf_bit.next = 0
            elif sekunde == 51:
                dcf_bit.next = 0
            elif sekunde == 52:
                dcf_bit.next = 0
            elif sekunde == 53:
                dcf_bit.next = 0
            elif sekunde == 54:
                dcf_bit.next = 0
            elif sekunde == 55:
                dcf_bit.next = 0
            elif sekunde == 56:
                dcf_bit.next = 0
            elif sekunde == 57:
                dcf_bit.next = 0
            elif sekunde == 58:
                dcf_bit.next = 0
            elif sekunde == 59:
                dcf_bit.next = 2
    return gen


def dcf_signal_gen(clk1ms, dcf_bit, dcf_sig, reset):

    count = Signal(intbv(0, min=0, max=1000))

    @always_seq(clk1ms.posedge, reset)
    def gen():
        if (count < 100 and dcf_bit == 0) or (count < 200 and dcf_bit == 1):
            dcf_sig.next = 0
        else:
            dcf_sig.next = 1
        count.next = count + 1 if count < 1000-1 else 0

    return gen
