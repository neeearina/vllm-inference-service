import statistics
import time

import httpx

URL = "http://127.0.0.1:8000/generate"
PAYLOAD = {
    "prompt": "Explain what is KV cache.",
    "max_tokens": 80,
    "temperature": 0.7,
}
WARM_COUNT = 5


def main():
    with httpx.Client(timeout=300.0) as client:
        t0 = time.perf_counter()
        r0 = client.post(URL, json=PAYLOAD)
        ok0 = r0.status_code == 200
        cold_ms = (time.perf_counter() - t0) * 1000

        warm_ms: list[float] = []
        for _ in range(WARM_COUNT):
            t0 = time.perf_counter()
            r = client.post(URL, json=PAYLOAD)
            warm_ms.append((time.perf_counter() - t0) * 1000)

            if r.status_code != 200:
                print(f"warn: HTTP {r.status_code}")

    
    avg_warm = statistics.mean(warm_ms) if warm_ms else 0.0

    print(f"cold (1st request):     {cold_ms:.1f} ms  HTTP {r0.status_code} ok={ok0}")

    for i, ms in enumerate(warm_ms, start=1):
        print(f"warm #{i}:               {ms:.1f} ms")

    print(f"warm avg ({WARM_COUNT}):    {avg_warm:.1f} ms")

    if cold_ms > 0:
        print(f"cold / warm_avg: {cold_ms / avg_warm:.2f}x")


if __name__ == "__main__":
    main()
