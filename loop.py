import time
from httpx import AsyncClient, Timeout
from tqdm import tqdm
import asyncio
import secrets


CONCURRENT_REQUEST_LIMIT = 3000  # Increased limit
REQUEST_TIMEOUT = 10.0

async def run(n):
    semaphore = asyncio.Semaphore(
        CONCURRENT_REQUEST_LIMIT
    )

    timeout = Timeout(REQUEST_TIMEOUT)
    # Enable HTTP/2 and reuse connection for multiple requests
    async with AsyncClient(http2=True, timeout=timeout) as client:
        tasks = []
        for i in tqdm(range(n), ascii=True):
            data = {"name": f"user-{i}-{secrets.token_hex(4)}"}
            task = send_request(
                client, semaphore, "http://localhost:5000/status"
            )
            tasks.append(task)

        resp = await asyncio.gather(*tasks)

        return resp

async def send_request(client, semaphore, *args, **kwargs):
    async with semaphore:
        return await client.get(*args, **kwargs)


if __name__ == "__main__":
    n = 1000
    loops = 10
    req_list = []
    t0 = time.time()
    for l in range(loops):
        start_time = time.time()
        responses = asyncio.run(run(n))
        end_time = time.time()
        elapsed_time = end_time - start_time
        requests_per_second = n / elapsed_time

        req_list.append(requests_per_second)

    from statistics import mean, median
    ave = mean(req_list)
    med = median(req_list)
    t1 = time.time() - t0
    total_req = n*loops
    print(F"Mean: {ave:.2f}, Median: {med:.2f}, TotalRequests:{n*loops} in {t1:.2f} seconds, Process Mean Reqests: {total_req/t1:.2f}")
