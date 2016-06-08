from myhdl import delay, always, instance, Signal, intbv, always_seq

def DCFDecoder(dcf_load, dcf_signal_ok, dcf_hrs1, dcf_hrs_10, dcf_mins1, dcf_mins10,
		dcf_sig, clk1ms, reset):

	"""
    :param dcf_load: boolean: overwrite existing state with dcf values output
    :param dcf_signal_ok: boolean signal ok output
    :param dcf_mins1: time minute output
    :param dcf_mins10: time 10th-minute output
    :param dcf_hrs1: time hour output
    :param dcf_hrs10: time 10th-hour output

    :param clk1ms: 1ms clock input
    :param dcf_sig: dcf signal input
    :param reset: Reset input
    """
    dfc_state = Signal(intbv(0, min=0, max=2))

    @instance
    def decode():
    	while True:
    		yield clk1ms.posedge, reset

    		if !dfc_state:
    			yield dcf_sig.negedge


    return decode