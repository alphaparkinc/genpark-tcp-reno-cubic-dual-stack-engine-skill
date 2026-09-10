class TCPCubicEngine:
    """
    TCP CUBIC Congestion Control Engine calculating window growth
    using cubic polynomial functions independent of RTT.
    """
    def __init__(self, ssthresh=64.0, c=0.4, beta=0.7):
        self.cwnd = 1.0
        self.ssthresh = ssthresh
        self.c = c
        self.beta = beta
        self.w_max = 0.0
        self.epoch_start = 0.0

    def on_loss(self, now_time):
        self.w_max = self.cwnd
        self.ssthresh = max(2.0, self.cwnd * self.beta)
        self.cwnd = self.ssthresh
        self.epoch_start = now_time

    def on_ack(self, now_time, rtt):
        if self.cwnd < self.ssthresh:
            self.cwnd += 1.0
        else:
            k = (self.w_max * (1.0 - self.beta) / self.c) ** (1.0 / 3.0) if self.w_max > 0 else 0.0
            t = now_time - self.epoch_start
            w_cubic = self.c * ((t - k) ** 3) + self.w_max
            target = max(w_cubic, self.cwnd + (1.0 / self.cwnd))
            self.cwnd = target
        return self.cwnd
