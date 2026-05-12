import simpy
import tkinter as tk
import random

# ======================
# GLOBAL
# ======================
timeline = []
SCALE = 40

entries = []

# ======================
# PROCESS (RR)
# ======================
def process(env, name, cpu, burst, arrival, time_slice, y):
    yield env.timeout(arrival)

    remaining = burst

    while remaining > 0:
        with cpu.request() as req:
            yield req

            start = env.now
            exec_time = min(time_slice, remaining)

            yield env.timeout(exec_time)

            end = env.now
            timeline.append((name, start, end, y))

            remaining -= exec_time

# ======================
# RUN
# ======================
def run_simulation():
    global timeline
    timeline = []

    canvas.delete("all")

    try:
        time_slice = int(input_ts.get())
    except:
        time_slice = 2

    env = simpy.Environment()
    cpu = simpy.Resource(env, capacity=1)

    for i, row in enumerate(entries):
        try:
            name = row[0].get()
            burst = int(row[1].get())
            arrival = int(row[2].get())
            priority = int(row[3].get())  # belum dipakai di RR

            env.process(process(
                env, name, cpu,
                burst, arrival,
                time_slice,
                50 + i*60
            ))
        except:
            continue

    env.run()
    draw_gantt()

# ======================
# GANTT
# ======================
def draw_gantt():
    max_time = 0
    max_y = 0

    for name, start, end, y in timeline:
        x1 = start * SCALE
        x2 = end * SCALE

        color = random.choice(["skyblue", "lightgreen", "orange", "pink", "violet"])

        canvas.create_rectangle(x1, y, x2, y+30, fill=color)
        canvas.create_text((x1+x2)//2, y+15, text=name)

        canvas.create_text(x1, y+40, text=str(start))
        canvas.create_text(x2, y+40, text=str(end))

        max_time = max(max_time, end)
        max_y = max(max_y, y)

    canvas.config(scrollregion=(0, 0, max_time * SCALE + 200, max_y + 100))

# ======================
# INPUT
# ======================
def add_row(pid="", burst="", arrival="", priority=""):
    r = len(entries) + 1

    e1 = tk.Entry(frame, width=10)
    e1.insert(0, pid if pid else f"P{r}")
    e1.grid(row=r, column=0)

    e2 = tk.Entry(frame, width=10)
    e2.insert(0, burst)
    e2.grid(row=r, column=1)

    e3 = tk.Entry(frame, width=10)
    e3.insert(0, arrival)
    e3.grid(row=r, column=2)

    e4 = tk.Entry(frame, width=10)
    e4.insert(0, priority)
    e4.grid(row=r, column=3)

    entries.append([e1, e2, e3, e4])

def generate_random():
    clear_table()
    n = int(input_n.get()) if input_n.get().isdigit() else 3

    for i in range(n):
        add_row(
            f"P{i+1}",
            random.randint(1,10),
            random.randint(0,5),
            random.randint(1,5)
        )

def clear_table():
    for widget in frame.winfo_children():
        widget.destroy()

    headers = ["Process ID", "Burst Time", "Arrival Time", "Priority"]
    for i,h in enumerate(headers):
        tk.Label(frame, text=h, font=("Arial", 10, "bold")).grid(row=0, column=i)

    entries.clear()

# ======================
# GUI
# ======================
root = tk.Tk()
root.title("Round Robin Simulator (SimPy + Full Input)")
root.geometry("950x650")

tk.Label(root, text="CPU Scheduling - Round Robin", font=("Arial", 16)).pack(pady=5)

# CONTROL
top = tk.Frame(root)
top.pack()

tk.Label(top, text="Jumlah:").pack(side="left")
input_n = tk.Entry(top, width=5)
input_n.pack(side="left")

tk.Button(top, text="Random", command=generate_random).pack(side="left", padx=5)
tk.Button(top, text="Tambah", command=add_row).pack(side="left", padx=5)
tk.Button(top, text="Clear", command=clear_table).pack(side="left", padx=5)

tk.Label(top, text="Time Slice:").pack(side="left", padx=10)
input_ts = tk.Entry(top, width=5)
input_ts.pack(side="left")

# TABEL
frame = tk.Frame(root)
frame.pack()
clear_table()

# RUN
tk.Button(root, text="Run Simulation", command=run_simulation).pack(pady=10)

# CANVAS
canvas_frame = tk.Frame(root)
canvas_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(canvas_frame, bg="white")

scroll_x = tk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
scroll_y = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)

canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

scroll_x.pack(side="bottom", fill="x")
scroll_y.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

root.mainloop()