import asyncio
import statistics
import time

import httpx


async def _one(client: httpx.AsyncClient, url: str) -> tuple[float, bool]:
    start = time.perf_counter()

    r = await client.post(
        url,
        json={
            "prompt": "Explain what is KV cache.",
            "max_tokens": 80,
            "temperature": 0.7,
        },
    )

    return time.perf_counter() - start, r.status_code == 200


async def _scenario(client: httpx.AsyncClient, url: str, n: int) -> dict:
    start = time.perf_counter()
    rows = await asyncio.gather(*[_one(client, url) for _ in range(n)])
    end = time.perf_counter() - start 

    latencies = [lat for lat, _ in rows]
    ok = sum(1 for _, good in rows if good)

    return {
        "n": n,
        "avg_ms": statistics.mean(latencies) * 1000,
        "rps": ok / end if end else 0.0,
        "ok": ok,
    }


async def main():
    url = "http://127.0.0.1:8000/generate"

    async with httpx.AsyncClient(timeout=120.0) as client:

        for n in (1, 5, 10):
            row = await _scenario(client, url, n)

            print(
                f"{n} concurrent: avg {row['avg_ms']:.1f} ms, "
                f"{row['rps']:.2f} req/s, ok {row['ok']}/{n}"
            )

if __name__ == "__main__":
    asyncio.run(main())
