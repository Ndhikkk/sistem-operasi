import simpy

def process(env, name, printer):
    with printer.request() as req:
        yield req
        print(f"{env.now} | {name} pakai printer")
        yield env.timeout(4)

env = simpy.Environment()
printer = simpy.Resource(env, capacity=1)

env.process(process(env, "P1", printer))
env.process(process(env, "P2", printer))

env.run()