import simpy

def process(env, name, cpu, io):
    with cpu.request() as req:
        yield req
        print(f"{env.now} | {name} CPU")
        yield env.timeout(2)

    with io.request() as req:
        yield req
        print(f"{env.now} | {name} I/O")
        yield env.timeout(3)

env = simpy.Environment()
cpu = simpy.Resource(env, capacity=1)
io = simpy.Resource(env, capacity=1)

env.process(process(env, "P1", cpu, io))
env.process(process(env, "P2", cpu, io))
env.process(process(env, "P3", cpu, io))

env.run()