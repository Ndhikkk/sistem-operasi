import simpy
import tkinter as tk
import random

# ======================
# GLOBAL
# ======================
timeline = []
SCALE = 50

entries = []

# ======================
# PROCESS STATE
# ======================
def process(env, name, ready_time, run_time, y):
    # READY
    start_ready = env.now
    yield env.timeout(ready_time)
    end_ready = env.now
    timeline.append((name, "READY", start_ready, end_ready, y))

    # RUNNING
    start_run = env.now
    yield env.timeout(run_time)
    end_run = env.now
    timeline.append((name, "RUN", start_run, end_run, y))

    # TERMINATED (point)
    timeline.append((name, "DONE", end_run, end_run, y))

# ======================
# RUN
# ======================
def run_simulation():
    global timeline
    timeline = []

    canvas.delete("all")

    env = simpy.Environment()

    for i, row in enumerate(entries):
        try:
            name = row[0].get()
            ready_time = int(row[1].get())
            run_time = int(row[2].get())

            env.process(process(
                env, name,
                ready_time, run_time,
                50 + i*60
            ))
        except:
            continue

    env.run()
    draw_timeline()

# ======================
# DRAW
# ======================
def draw_timeline():
    colors = {
        "READY": "orange",
        "RUN": "green",
        "DONE": "red"
    }

    max_time = 0
    max_y = 0

    for name, state, start, end, y in timeline:
        x1 = start * SCALE
        x2 = end * SCALE

        if state == "DONE":
            canvas.create_oval(x1-3, y+10, x1+3, y+16, fill="red")
            canvas.create_text(x1, y+30, text="END")
        else:
            canvas.create_rectangle(x1, y, x2, y+25, fill=colors[state])
            canvas.create_text((x1+x2)//2, y+12, text=f"{name}-{state}")

        max_time = max(max_time, end)
        max_y = max(max_y, y)

    canvas.config(scrollregion=(0, 0, max_time*SCALE+200, max_y+100))

# ======================
# INPUT
# ======================
def add_row(pid="", ready="", run=""):
    r = len(entries) + 1

    e1 = tk.Entry(frame, width=10)
    e1.insert(0, pid if pid else f"P{r}")
    e1.grid(row=r, column=0)

    e2 = tk.Entry(frame, width=10)
    e2.insert(0, ready)
    e2.grid(row=r, column=1)

    e3 = tk.Entry(frame, width=10)
    e3.insert(0, run)
    e3.grid(row=r, column=2)

    entries.append([e1, e2, e3])

def generate_random():
    clear_table()
    n = int(input_n.get()) if input_n.get().isdigit() else 3

    for i in range(n):
        add_row(
            f"P{i+1}",
            random.randint(1,3),
            random.randint(2,6)
        )

def clear_table():
    for widget in frame.winfo_children():
        widget.destroy()

    headers = ["Process ID", "READY Time", "RUN Time"]
    for i,h in enumerate(headers):
        tk.Label(frame, text=h, font=("Arial", 10, "bold")).grid(row=0, column=i)

    entries.clear()

# ======================
# GUI
# ======================
root = tk.Tk()
root.title("Process State Simulator")
root.geometry("950x600")

tk.Label(root, text="Process State (READY → RUNNING → TERMINATED)", font=("Arial", 16)).pack(pady=5)

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