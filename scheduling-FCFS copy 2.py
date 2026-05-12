processes = [
    ["P1", 5],
    ["P2", 3],
    ["P3", 2]
]

time = 0

for process in processes:
    name = process[0]
    burst = process[1]

    print(f"{time} | {name} mulai")

    time = time + burst

    print(f"{time} | {name} selesai")