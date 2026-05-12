import simpy

def process(env, name, cpu, burst, time_slice):
    remaining = burst
    while remaining > 0:
        with cpu.request() as req:
            yield req
            exec_time = min(time_slice, remaining)
            print(f"{env.now} | {name} jalan {exec_time}")
            yield env.timeout(exec_time)
            remaining -= exec_time

# 🔥 input time slice
TIME_SLICE = int(input("Masukkan Time Slice: "))

env = simpy.Environment()
cpu = simpy.Resource(env, capacity=1)

env.process(process(env, "P1", cpu, 5, TIME_SLICE))
env.process(process(env, "P2", cpu, 4, TIME_SLICE))

env.run()