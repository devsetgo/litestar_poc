import asyncio
from ctypes import cdll, c_char_p, c_long
import time
from statistics import mean, median

def call_code():
    # Load the shared library
    lib = cdll.LoadLibrary('./http_request.so')

    # Set the argument types and return type
    lib.http_get.argtypes = [c_char_p]
    lib.http_get.restype = c_long

    # Call the function
    url = "http://localhost:5000/status".encode('utf-8')
    status_code = lib.http_get(url)

    return status_code

async def run(n):
    loop = asyncio.get_event_loop()
    futures = [loop.run_in_executor(None, call_code) for _ in range(n)]
    return await asyncio.gather(*futures)

if __name__ == "__main__":
    n = 10000
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

    ave = mean(req_list)
    med = median(req_list)
    t1 = time.time() - t0
    total_req = n*loops
    print("")
    print(f"Mean: {ave:,.2f}, Median: {med:,.2f}, Total Requests:{total_req:,} in {t1:.2f} seconds, Process Mean Requests: {total_req/t1:,.2f}")
