import simpy

def process(env, name):
    print(f"{env.now} | {name} READY")
    yield env.timeout(1)
    print(f"{env.now} | {name} RUNNING")
    yield env.timeout(2)
    print(f"{env.now} | {name} TERMINATED")

env = simpy.Environment()
env.process(process(env, "P1"))
env.run()