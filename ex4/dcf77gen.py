from myhdl import delay, always, instance, Signal, intbv, always_seq


def dcf_time_gen(clk1s, time_secs1, time_secs10, time_min1, time_min10, time_hrs1, time_hrs10, dcf_bit, reset):

    sekunde = Signal(intbv(57, min=0, max=60))

    @instance
    def gen():
        while True:
            if not reset:
                dcf_bit.next = 2
            yield clk1s, reset
            sekunde.next = sekunde +1 if sekunde < sekunde.max -1 else 0
            if sekunde == 0:
                dcf_bit.next = 0
            if sekunde == 1:
                dcf_bit.next = 1
            if sekunde == 0:
                dcf_bit.next = 0
            if sekunde == 1:
                dcf_bit.next = 1
            if sekunde == 1:
                dcf_bit.next = 1
            if 4 < sekunde <= 14:  # unused
                dcf_bit.next = 0

            if sekunde == 15:
                dcf_bit.next = 0
            if sekunde == 16:
                dcf_bit.next = 0 # zeitsprung
            if sekunde == 17:
                dcf_bit.next = 1 # bit 2 + utc
            if sekunde == 18:
                dcf_bit.next = 0 # bit 1 + utc
            if sekunde == 19:
                dcf_bit.next = 0  # schaltsekunde
            if sekunde == 20:
                dcf_bit.next = 1  # start zeitkodirung
            if sekunde == 21:
                dcf_bit.next = time_min1 & 0b0001
            if sekunde == 22:
                dcf_bit.next = time_min1 & 0b0010
            if sekunde == 23:
                dcf_bit.next = time_min1 & 0b0100
            if sekunde == 24:
                dcf_bit.next = time_min1 & 0b1000
            if sekunde == 25:
                dcf_bit.next = time_min10 & 0b001
            if sekunde == 26:
                dcf_bit.next = time_min10 & 0b010
            if sekunde == 27:
                dcf_bit.next = time_min10 & 0b100
            if sekunde == 28:
                dcf_bit.next = (time_min1 & 0b0001 + time_min1 & 0b0010 + time_min1 & 0b0100 + time_min1 & 0b1000 +
                                    time_min10 & 0b001 + time_min10 & 0b010 + time_min10 & 0b100) % 2
            if sekunde == 29:
                dcf_bit.next = time_hrs1 & 0b0001
            if sekunde == 30:
                dcf_bit.next = time_hrs1 & 0b0010
            if sekunde == 31:
                dcf_bit.next = time_hrs1 & 0b0100
            if sekunde == 32:
                dcf_bit.next = time_hrs1 & 0b1000
            if sekunde == 33:
                dcf_bit.next = time_hrs10 & 0b01
            if sekunde == 34:
                dcf_bit.next = time_hrs10 & 0b10
            if sekunde == 35:
                dcf_bit.next = (time_hrs1 & 0b0001 + time_hrs1 & 0b0010 + time_hrs1 & 0b0100 + time_hrs1 & 0b1000 + time_hrs10 & 0b01 + time_hrs10 & 0b10) % 2
            if sekunde == 36:
                dcf_bit.next = 0
            if sekunde == 37:
                dcf_bit.next = 0
            if sekunde == 38:
                dcf_bit.next = 0
            if sekunde == 39:
                dcf_bit.next = 0
            if sekunde == 40:
                dcf_bit.next = 0
            if sekunde == 41:
                dcf_bit.next = 0
            if sekunde == 42:
                dcf_bit.next = 0
            if sekunde == 43:
                dcf_bit.next = 0
            if sekunde == 44:
                dcf_bit.next = 0
            if sekunde == 45:
                dcf_bit.next = 0
            if sekunde == 46:
                dcf_bit.next = 0
            if sekunde == 047:
                dcf_bit.next = 0
            if sekunde == 48:
                dcf_bit.next = 0
            if sekunde == 49:
                dcf_bit.next = 0
            if sekunde == 50:
                dcf_bit.next = 0
            if sekunde == 51:
                dcf_bit.next = 0
            if sekunde == 52:
                dcf_bit.next = 0
            if sekunde == 53:
                dcf_bit.next = 0
            if sekunde == 54:
                dcf_bit.next = 0
            if sekunde == 55:
                dcf_bit.next = 0
            if sekunde == 56:
                dcf_bit.next = 0
            if sekunde == 57:
                dcf_bit.next = 0
            if sekunde == 58:
                dcf_bit.next = 0
            if sekunde == 59:
                dcf_bit.next = 2
    return gen


def dcf_signal_gen(clk1ms, dcfsing, dcfout, reset):

    count = Signal(intbv(0, min=0, max=1000))

    @always_seq(clk1ms.posedge, reset)
    def gen():
        if (count < 100 and dcfsing == 0) or (count < 200 and dcfsing == 1):
            dcfout.next = 0
        else:
            dcfout.next = 1
        count.next = count + 1 if count < 1000-1 else 0

    return gen
