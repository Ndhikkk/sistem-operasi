import simpy
import tkinter as tk
import random

# ======================
# GLOBAL
# ======================
timeline = []
SCALE = 40

entries = []
status_labels = []

# ======================
# SIMULASI
# ======================
def process(env, name, cpu, burst, arrival, label, y_pos):
    yield env.timeout(arrival)

    with cpu.request() as req:
        label.config(text="WAITING")
        yield req

        start = env.now
        label.config(text="RUNNING")

        yield env.timeout(burst)

        end = env.now
        timeline.append((name, start, end, y_pos))

        label.config(text="DONE")

# ======================
# RUN
# ======================
def run_simulation():
    global timeline
    timeline = []

    canvas.delete("all")

    env = simpy.Environment()
    cpu = simpy.Resource(env, capacity=1)

    for i, row in enumerate(entries):
        try:
            name = row[0].get()
            burst = int(row[1].get())
            arrival = int(row[2].get())

            label = status_labels[i]

            env.process(process(env, name, cpu, burst, arrival, label, 50 + i*60))
        except:
            continue

    env.run()
    draw_gantt()

# ======================
# GANTT (FULL FIX)
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

    # garis timeline
    canvas.create_line(0, 30, max_time * SCALE, 30)

    # scroll area FULL
    canvas.config(scrollregion=(0, 0, max_time * SCALE + 200, max_y + 100))

# ======================
# TAMBAH BARIS
# ======================
def add_row(pid="", burst="", arrival="", priority=""):
    row = []
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

    status = tk.Label(frame, text="READY")
    status.grid(row=r, column=4)

    row.extend([e1, e2, e3, e4])
    entries.append(row)
    status_labels.append(status)

# ======================
# RANDOM
# ======================
def generate_random():
    clear_table()

    try:
        n = int(input_n.get())
    except:
        n = 3

    for i in range(n):
        add_row(
            pid=f"P{i+1}",
            burst=random.randint(1, 10),
            arrival=random.randint(0, 5),
            priority=random.randint(1, 5)
        )

# ======================
# CLEAR
# ======================
def clear_table():
    for widget in frame.winfo_children():
        widget.destroy()

    headers = ["Process ID", "Burst Time", "Arrival Time", "Priority", "Status"]
    for i, h in enumerate(headers):
        tk.Label(frame, text=h, font=("Arial", 10, "bold")).grid(row=0, column=i)

    entries.clear()
    status_labels.clear()

# ======================
# SCROLL MOUSE
# ======================
def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# ======================
# GUI
# ======================
root = tk.Tk()
root.title("CPU Scheduling Simulator")
root.geometry("950x650")

tk.Label(root, text="CPU Scheduling (FCFS)", font=("Arial", 16)).pack(pady=5)

# CONTROL
top_frame = tk.Frame(root)
top_frame.pack()

tk.Label(top_frame, text="Jumlah Proses:").pack(side="left")
input_n = tk.Entry(top_frame, width=5)
input_n.pack(side="left")

tk.Button(top_frame, text="Random", command=generate_random).pack(side="left", padx=5)
tk.Button(top_frame, text="Tambah", command=lambda: add_row()).pack(side="left", padx=5)
tk.Button(top_frame, text="Clear", command=clear_table).pack(side="left", padx=5)

# TABEL
frame = tk.Frame(root)
frame.pack()

clear_table()

# RUN
tk.Button(root, text="Run Simulation", command=run_simulation).pack(pady=10)

# ======================
# CANVAS SCROLL FULL
# ======================
canvas_frame = tk.Frame(root)
canvas_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(canvas_frame, bg="white")

scroll_x = tk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
scroll_y = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)

canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

scroll_x.pack(side="bottom", fill="x")
scroll_y.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

canvas.bind_all("<MouseWheel>", on_mousewheel)

root.mainloop()