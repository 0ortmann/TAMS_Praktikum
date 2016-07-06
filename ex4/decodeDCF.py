from myhdl import delay, always, instance, Signal, intbv, always_seq

def DCFDecoder(dcf_load, dcf_signal_ok, dcf_hrs1, dcf_hrs10, dcf_mins1, dcf_mins10,
        dcf_begin, dcf_state, clk1s, reset):

    """
    :param dcf_load: boolean: overwrite existing state with dcf values output
    :param dcf_signal_ok: boolean signal ok output
    :param dcf_mins1: time minute output
    :param dcf_mins10: time 10th-minute output
    :param dcf_hrs1: time hour output
    :param dcf_hrs10: time 10th-hour output

    :param dcf_begin: is 1 if a new minute starts, else 0
    :param dcf_state: determined state of the dcf-signal (0 or 1)

    :param clk1s: 1s clock input
    :param reset: Reset input
    """

    second = Signal(intbv(0, min=0, max=60))

    @instance
    def decode():
        while True:
            dcf_load.next = 0
            dcf_signal_ok.next = 0
            
            print('wait dfc_begin')
            yield dcf_begin.negedge, reset
            print('got dfc_begin')

            second.next = 57
            
            while True:
                yield clk1s.posedge, reset
                if not reset:
                    second.next = 0

                second.next = second + 1 if second < second.max - 1 else 0
                if second == 21:
                    mask = 0b1111 ^ (~dcf_state << 0)
                    dcf_mins1.next = dcf_mins1 & mask
                elif second == 22:
                    mask = 0b1111 ^ (~dcf_state << 1)
                    dcf_mins1.next = dcf_mins1 & mask
                elif second == 23:
                    mask = 0b1111 ^ (~dcf_state << 2)
                    dcf_mins1.next = dcf_mins1 & mask
                elif second == 24:
                    mask = 0b1111 ^ (~dcf_state << 3)
                    dcf_mins1.next = dcf_mins1 & mask
                elif second == 25:
                    mask = 0b1111 ^ (~dcf_state << 0)
                    dcf_mins10.next = dcf_mins10 & mask
                elif second == 26:
                    mask = 0b1111 ^ (~dcf_state << 1)
                    dcf_mins10.next = dcf_mins10 & mask
                elif second == 27:
                    mask = 0b1111 ^ (~dcf_state << 2)
                    dcf_mins10.next = dcf_mins10 & mask

                elif second == 29:
                    mask = 0b1111 ^ (~dcf_state << 0)
                    dcf_hrs1.next = dcf_hrs1 & mask
                elif second == 30:
                    mask = 0b1111 ^ (~dcf_state << 1)
                    dcf_hrs1.next = dcf_hrs1 & mask                
                elif second == 31:
                    mask = 0b1111 ^ (~dcf_state << 2)
                    dcf_hrs1.next = dcf_hrs1 & mask                
                elif second == 32:
                    mask = 0b1111 ^ (~dcf_state << 3)
                    dcf_hrs1.next = dcf_hrs1 & mask                
                elif second == 33:
                    mask = 0b1111 ^ (~dcf_state << 0)
                    dcf_hrs10.next = dcf_hrs10 & mask
                elif second == 34:
                    mask = 0b1111 ^ (~dcf_state << 1)
                    dcf_hrs10.next = dcf_hrs10 & mask

                elif second == 58:
                    dcf_load.next = 1
                    dcf_signal_ok.next = 1
                
                elif second == 59:
                    break
            
    return decode
    