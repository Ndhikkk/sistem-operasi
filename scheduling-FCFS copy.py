import simpy

def process(env, name, cpu, burst):
    yield env.timeout(0)  # arrival

    print(f"{env.now:.2f} | {name} datang")

    with cpu.request() as req:
        yield req

        print(f"{env.now:.2f} | {name} mulai")
        yield env.timeout(burst)

        print(f"{env.now:.2f} | {name} selesai")

# 🔥 pakai realtime environment
env = simpy.RealtimeEnvironment(factor=1.0, strict=False)

cpu = simpy.Resource(env, capacity=3    )

env.process(process(env, "P1", cpu, 5))
env.process(process(env, "P2", cpu, 3))
env.process(process(env, "P3", cpu, 2))

env.run()