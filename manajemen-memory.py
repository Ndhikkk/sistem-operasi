import simpy

def process(env, name, memory):
    print(f"{env.now} | {name} request memori")
    yield memory.get(10)
    print(f"{env.now} | {name} dapat memori")

    yield env.timeout(3)

    yield memory.put(10)
    print(f"{env.now} | {name} release memori")

env = simpy.Environment()
memory = simpy.Container(env, capacity=50, init=50)

env.process(process(env, "P1", memory))
env.process(process(env, "P2", memory))
env.process(process(env, "P3", memory))

env.run()