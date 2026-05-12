import simpy

def process(env, name, cpu, burst):
    yield env.timeout(0)  # arrival
    with cpu.request() as req:
        yield req
        print(f"{env.now} | {name} mulai")
        yield env.timeout(burst)
        print(f"{env.now} | {name} selesai")

env = simpy.Environment()
cpu = simpy.Resource(env, capacity=1)

env.process(process(env, "P1", cpu, 5))
env.process(process(env, "P2", cpu, 3))
env.process(process(env, "P3", cpu, 2))

env.run()