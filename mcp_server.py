import sys
import json
from client import TCPCubicEngine

def main():
    engine = TCPCubicEngine()
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        if method == "on_ack":
            w = engine.on_ack(params.get("now_time", 0.1), params.get("rtt", 0.05))
            res = {"cwnd": w}
        elif method == "on_loss":
            engine.on_loss(params.get("now_time", 1.0))
            res = {"cwnd": engine.cwnd, "ssthresh": engine.ssthresh}
        else:
            res = {"error": "unknown method"}
        sys.stdout.write(json.dumps({"id": req.get("id"), "result": res}) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
