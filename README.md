# litestar_poc
Trying out Litestar to see how it compares to FastAPI


## Speed Test
via HTTPX only
python3 loop.py

via calling C code
compile first
gcc -shared -o http_request.so http_request.c -lcurl -fPIC

run

python3 loop_c.py
