import simpy

def process(env, name, cpu, burst):
    yield env.timeout(0)
    with cpu.request(priority=burst) as req:
        yield req
        print(f"{env.now} | {name} (burst={burst}) mulai")
        yield env.timeout(burst)
        print(f"{env.now} | {name} selesai")

env = simpy.Environment()
cpu = simpy.PriorityResource(env, capacity=1)

env.process(process(env, "P1", cpu, 5))
env.process(process(env, "P2", cpu, 3))
env.process(process(env, "P3", cpu, 2))

env.run()