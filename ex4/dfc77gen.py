from myhdl import delay, always, instance, Signal, intbv, always_seq


def dfc_time_gen(clk1s, time_secs1, time_secs10, time_min1, time_min10, time_hrs1, time_hrs10, dfc_bit, reset):

    sekunde = Signal(0, min=0, max=60)

    @instance
    def gen():
        while True:
            if reset:
                dfc_bit.next = 2
            yield clk1s, reset
            if sekunde == 0:
                dfc_bit.next = 0
            if 1 < sekunde <= 14:  # unused
                dfc_bit.next = 0

            if sekunde == 15:
                dfc_bit.next = 0
            if sekunde == 16:
                dfc_bit.next = 0 # zeitsprung
            if sekunde == 17:
                dfc_bit.next = 1 # bit 2 + utc
            if sekunde == 18:
                dfc_bit.next = 0 # bit 1 + utc
            if sekunde == 19:
                dfc_bit.next = 0  # schaltsekunde
            if sekunde == 20:
                dfc_bit.next = 1  # start zeitkodirung
            if sekunde == 21:
                dfc_bit.next = time_min1 & 0b0001
            if sekunde == 22:
                dfc_bit.next = time_min1 & 0b0010
            if sekunde == 23:
                dfc_bit.next = time_min1 & 0b0100
            if sekunde == 24:
                dfc_bit.next = time_min1 & 0b1000
            if sekunde == 25:
                dfc_bit.next = time_min10 & 0b001
            if sekunde == 26:
                dfc_bit.next = time_min10 & 0b010
            if sekunde == 27:
                dfc_bit.next = time_min10 & 0b100
            if sekunde == 28:
                dfc_bit.next = (time_min1 & 0b0001 + time_min1 & 0b0010 + time_min1 & 0b0100 + time_min1 & 0b1000 +
                                    time_min10 & 0b001 + time_min10 & 0b010 + time_min10 & 0b100) % 2
            if sekunde == 29:
                dfc_bit.next = time_hrs1 & 0b0001
            if sekunde == 30:
                dfc_bit.next = time_hrs1 & 0b0010
            if sekunde == 31:
                dfc_bit.next = time_hrs1 & 0b0100
            if sekunde == 32:
                dfc_bit.next = time_hrs1 & 0b1000
            if sekunde == 33:
                dfc_bit.next = time_hrs10 & 0b01
            if sekunde == 34:
                dfc_bit.next = time_hrs10 & 0b10
            if sekunde == 35:
                dfc_bit.next = (time_hrs1 & 0b0001 + time_hrs1 & 0b0010 + time_hrs1 & 0b0100 + time_hrs1 & 0b1000 + time_hrs10 & 0b01 + time_hrs10 & 0b10) % 2
            if sekunde == 36:
                dfc_bit.next = 0
            if sekunde == 37:
                dfc_bit.next = 0
            if sekunde == 38:
                dfc_bit.next = 0
            if sekunde == 39:
                dfc_bit.next = 0
            if sekunde == 40:
                dfc_bit.next = 0
            if sekunde == 41:
                dfc_bit.next = 0
            if sekunde == 42:
                dfc_bit.next = 0
            if sekunde == 43:
                dfc_bit.next = 0
            if sekunde == 44:
                dfc_bit.next = 0
            if sekunde == 45:
                dfc_bit.next = 0
            if sekunde == 46:
                dfc_bit.next = 0
            if sekunde == 047:
                dfc_bit.next = 0
            if sekunde == 48:
                dfc_bit.next = 0
            if sekunde == 49:
                dfc_bit.next = 0
            if sekunde == 50:
                dfc_bit.next = 0
            if sekunde == 51:
                dfc_bit.next = 0
            if sekunde == 52:
                dfc_bit.next = 0
            if sekunde == 53:
                dfc_bit.next = 0
            if sekunde == 54:
                dfc_bit.next = 0
            if sekunde == 55:
                dfc_bit.next = 0
            if sekunde == 56:
                dfc_bit.next = 0
            if sekunde == 57:
                dfc_bit.next = 0
            if sekunde == 58:
                dfc_bit.next = 0
            if sekunde == 59:
                dfc_bit.next = 2


def dfc_signal_gen(clk1ms, dfcsing, dfcout, reset):

    count = Signal(56, min=0, max=1000)

    @always_seq(clk1ms, reset)
    def gen():
        if count < 100 and dfcsing == 0 or count < 200 and dfcsing == 1:
            dfcout.next = 0
        else:
            dfcout.next = 1
        count.next = count + 1 if count < 1000-1 else 0

    return gen
