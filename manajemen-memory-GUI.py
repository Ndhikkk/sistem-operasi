import simpy
import tkinter as tk
import random

# ======================
# GLOBAL
# ======================
timeline = []
memory_usage = []
SCALE = 40

entries = []
status_labels = []

TOTAL_MEMORY = 50
colors = {}

# ======================
# PROCESS
# ======================
def process(env, name, memory, amount, duration, label, y):
    label.config(text="REQUEST")

    yield memory.get(amount)

    start = env.now
    label.config(text="ALLOCATED")

    memory_usage.append((env.now, memory.level))

    yield env.timeout(duration)

    yield memory.put(amount)
    end = env.now

    memory_usage.append((env.now, memory.level))

    timeline.append((name, start, end))

    label.config(text="RELEASED")

# ======================
# RUN
# ======================
def run_simulation():
    global timeline, memory_usage, colors
    timeline = []
    memory_usage = []
    colors = {}

    canvas.delete("all")

    env = simpy.Environment()
    memory = simpy.Container(env, capacity=TOTAL_MEMORY, init=TOTAL_MEMORY)

    for i, row in enumerate(entries):
        try:
            name = row[0].get()
            amount = int(row[1].get())
            duration = int(row[2].get())

            label = status_labels[i]

            # warna tetap
            colors[name] = random.choice(
                ["skyblue", "lightgreen", "orange", "pink", "violet"]
            )

            env.process(process(
                env, name, memory,
                amount, duration,
                label, 50 + i*50
            ))
        except:
            continue

    env.run()
    draw_all()

# ======================
# DRAW MEMORY (FIX)
# ======================
def draw_memory(max_time):
    y = 30
    canvas.create_text(10, y-10, text="Memory Usage", anchor="w")

    for i in range(len(memory_usage)-1):
        t1, m1 = memory_usage[i]
        t2, m2 = memory_usage[i+1]

        x1 = t1 * SCALE
        x2 = t2 * SCALE

        used = TOTAL_MEMORY - m1

        canvas.create_rectangle(x1, y, x2, y+20, outline="black")

        used_width = (used / TOTAL_MEMORY) * (x2 - x1)

        canvas.create_rectangle(
            x1, y,
            x1 + used_width, y+20,
            fill="red"
        )

        canvas.create_text(x1, y+35, text=str(m1))

# ======================
# DRAW GANTT (FIX)
# ======================
def draw_gantt():
    base_y = 100

    for i, (name, start, end) in enumerate(timeline):
        y = base_y + i * 40

        x1 = start * SCALE
        x2 = end * SCALE

        canvas.create_rectangle(x1, y, x2, y+25, fill=colors[name])
        canvas.create_text((x1+x2)//2, y+12, text=name)

        canvas.create_text(x1, y+35, text=str(start))
        canvas.create_text(x2, y+35, text=str(end))

# ======================
# AXIS
# ======================
def draw_axis(max_time):
    y = 80
    canvas.create_line(0, y, max_time * SCALE, y)

    for t in range(max_time + 1):
        x = t * SCALE
        canvas.create_text(x, y-10, text=str(t))

# ======================
# DRAW ALL
# ======================
def draw_all():
    if not timeline:
        return

    max_time = max(end for _, _, end in timeline)

    draw_memory(max_time)
    draw_axis(max_time)
    draw_gantt()

    canvas.config(scrollregion=(0, 0, max_time * SCALE + 200, 600))

# ======================
# INPUT
# ======================
def add_row(pid="", mem="", dur=""):
    r = len(entries) + 1

    e1 = tk.Entry(frame, width=10)
    e1.insert(0, pid if pid else f"P{r}")
    e1.grid(row=r, column=0)

    e2 = tk.Entry(frame, width=10)
    e2.insert(0, mem)
    e2.grid(row=r, column=1)

    e3 = tk.Entry(frame, width=10)
    e3.insert(0, dur)
    e3.grid(row=r, column=2)

    status = tk.Label(frame, text="READY")
    status.grid(row=r, column=3)

    entries.append([e1, e2, e3])
    status_labels.append(status)

def generate_random():
    clear_table()
    n = int(input_n.get()) if input_n.get().isdigit() else 3

    for i in range(n):
        add_row(
            f"P{i+1}",
            random.randint(5,20),
            random.randint(2,6)
        )

def clear_table():
    for widget in frame.winfo_children():
        widget.destroy()

    headers = ["Process ID", "Memory", "Duration", "Status"]
    for i,h in enumerate(headers):
        tk.Label(frame, text=h, font=("Arial", 10, "bold")).grid(row=0, column=i)

    entries.clear()
    status_labels.clear()

# ======================
# GUI
# ======================
root = tk.Tk()
root.title("Memory Management Simulator")
root.geometry("1000x650")

tk.Label(root, text="Memory Management - SimPy", font=("Arial", 16)).pack(pady=5)

top = tk.Frame(root)
top.pack()

tk.Label(top, text="Jumlah:").pack(side="left")
input_n = tk.Entry(top, width=5)
input_n.pack(side="left")

tk.Button(top, text="Random", command=generate_random).pack(side="left", padx=5)
tk.Button(top, text="Tambah", command=add_row).pack(side="left", padx=5)
tk.Button(top, text="Clear", command=clear_table).pack(side="left", padx=5)

frame = tk.Frame(root)
frame.pack()

clear_table()

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