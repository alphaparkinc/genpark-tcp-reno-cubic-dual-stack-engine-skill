from client import TCPCubicEngine

def main():
    print("=== Testing TCP Reno vs CUBIC Dual-Stack Engine ===")
    cubic = TCPCubicEngine()
    for t in [0.01 * i for i in range(1, 10)]:
        cwnd = cubic.on_ack(now_time=t, rtt=0.05)
    print("CWND after ACKs:", cwnd)
    assert cwnd > 1.0

    cubic.on_loss(now_time=1.0)
    print("CWND after loss event:", cubic.cwnd)
    assert cubic.cwnd < 20.0
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
