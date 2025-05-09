from pwn import *
import time

io = remote("0.0.0.0",9007)

def findCounterfeit(N,C):
    low = 0
    high = N - 1
    for _ in range(C):
        # Si se halla la moneda con menos pesadas enviar pesadas de relleno hasta llegar a C
        if low == high:
            io.sendline(str(low).encode())
            io.recvline()
            break
        mid = (low + high) // 2
        weight_coins = " ".join(str(i) for i in range(low,mid+1))
        io.sendline(weight_coins.encode())
        weight = int(io.recvline().decode().strip())
        expected_weight = 10 * (mid - low + 1)
        if weight < expected_weight:
            high = mid
        else:
            low = mid + 1
    return low

time.sleep(5)
for i in range(100):
	line = io.recvline().decode().strip()
	while not line.startswith("N="):
    		line = io.recvline().decode().strip()
	N = int(line.split("N=")[1].split()[0])
	C = int(line.split("C=")[1].split()[0])

	counterfeit_coin= findCounterfeit(N,C)
	io.sendline(str(counterfeit_coin).encode())
	print(io.recvline().decode())
io.interactive()
