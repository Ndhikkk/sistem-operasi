import simpy

def process(env, name, cpu, burst, priority):
    yield env.timeout(0)
    with cpu.request(priority=priority) as req:
        yield req
        print(f"{env.now} | {name} (priority={priority}) mulai")
        yield env.timeout(burst)
        print(f"{env.now} | {name} selesai")

env = simpy.Environment()
cpu = simpy.PriorityResource(env, capacity=1)

env.process(process(env, "P1", cpu, 5, priority=2))
env.process(process(env, "P2", cpu, 3, priority=1))
env.process(process(env, "P3", cpu, 2, priority=3))

env.run()