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
# PROCESS (RESOURCE)
# ======================
def process(env, name, printer, duration, label, y):
    label.config(text="WAITING")

    with printer.request() as req:
        yield req

        label.config(text="USING")

        start = env.now
        yield env.timeout(duration)
        end = env.now

        timeline.append((name, start, end, y))

        label.config(text="DONE")

# ======================
# RUN
# ======================
def run_simulation():
    global timeline
    timeline = []

    canvas.delete("all")

    env = simpy.Environment()
    printer = simpy.Resource(env, capacity=1)

    for i, row in enumerate(entries):
        try:
            name = row[0].get()
            duration = int(row[1].get())
            label = status_labels[i]

            env.process(process(
                env, name, printer,
                duration, label,
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
def add_row(pid="", duration=""):
    r = len(entries) + 1

    e1 = tk.Entry(frame, width=10)
    e1.insert(0, pid if pid else f"P{r}")
    e1.grid(row=r, column=0)

    e2 = tk.Entry(frame, width=10)
    e2.insert(0, duration)
    e2.grid(row=r, column=1)

    status = tk.Label(frame, text="READY")
    status.grid(row=r, column=2)

    entries.append([e1, e2])
    status_labels.append(status)

def generate_random():
    clear_table()
    n = int(input_n.get()) if input_n.get().isdigit() else 3

    for i in range(n):
        add_row(f"P{i+1}", random.randint(2,6))

def clear_table():
    for widget in frame.winfo_children():
        widget.destroy()

    headers = ["Process ID", "Print Time", "Status"]
    for i,h in enumerate(headers):
        tk.Label(frame, text=h, font=("Arial", 10, "bold")).grid(row=0, column=i)

    entries.clear()
    status_labels.clear()

# ======================
# GUI
# ======================
root = tk.Tk()
root.title("Printer Resource Simulator")
root.geometry("950x650")

tk.Label(root, text="Resource Sharing - Printer (SimPy)", font=("Arial", 16)).pack(pady=5)

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