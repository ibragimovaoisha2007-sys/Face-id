import argparse
import json
from datetime import datetime

import httpx


def build_payload(index: int):
    return {
        "terminalUserId": f"S{1000 + index}",
        "timestamp": datetime.utcnow().isoformat(),
        "deviceId": "DEVICE-001",
        "eventType": "IN" if index % 2 == 0 else "OUT",
        "sourceEventId": f"evt-{index}",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()

    for i in range(args.count):
        payload = build_payload(i)
        response = httpx.post(args.url, json=payload)
        print(response.status_code, json.dumps(response.json()))


if __name__ == "__main__":
    main()
