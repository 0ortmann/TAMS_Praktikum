def increment(lower, upper, max_upper, max_lower_on_upper):
        """
        Increments a two secment timer, with lower and upper the counters
        :param lower: the lower counter
        :param upper: the upper counter
        :param max_upper: the max value for the upper register
        :param max_lower_on_upper: the max value for the lower register if the upper register is max
        :return: bool if the counter as had an overflow in the last counting step
        """
        #a = intbv(9,min=0,max=10)
        #a = intbv(9 if upper != max_upper else max_lower_on_upper, min=0, max=10)
        if 9 == lower or (upper == max_upper and lower == max_lower_on_upper):
            upper.next = upper + 1 if upper < max_upper else 0
        if upper == max_upper:
            lower.next = lower + 1 if lower < max_lower_on_upper else 0
        else:
            lower.next = lower + 1 if lower < 9 else 0