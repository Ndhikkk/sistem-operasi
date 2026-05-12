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
# RUN (PRIORITY NON PREEMPTIVE)
# ======================
def run_simulation():
    global timeline
    timeline = []

    canvas.delete("all")

    processes = []

    # ambil data dari tabel
    for i, row in enumerate(entries):
        try:
            name = row[0].get()
            burst = int(row[1].get())
            arrival = int(row[2].get())
            priority = int(row[3].get())
            label = status_labels[i]

            label.config(text="READY")

            processes.append({
                "name": name,
                "burst": burst,
                "arrival": arrival,
                "priority": priority,
                "label": label
            })
        except:
            continue

    # sort awal berdasarkan arrival
    processes.sort(key=lambda x: x["arrival"])

    time = 0
    ready_queue = []
    completed = []

    while processes or ready_queue:

        # masukkan proses yang sudah datang
        while processes and processes[0]["arrival"] <= time:
            p = processes.pop(0)
            p["label"].config(text=f"WAIT ({p['priority']})")
            ready_queue.append(p)

        if ready_queue:
            # pilih priority terkecil
            ready_queue.sort(key=lambda x: x["priority"])
            p = ready_queue.pop(0)

            p["label"].config(text=f"RUN ({p['priority']})")

            start = time
            end = time + p["burst"]

            timeline.append((p["name"], start, end, 50 + len(completed)*60))

            time = end
            p["label"].config(text="DONE")

            completed.append(p)

        else:
            time += 1  # idle

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

    canvas.create_line(0, 30, max_time * SCALE, 30)

    canvas.config(scrollregion=(0, 0, max_time * SCALE + 200, max_y + 100))

# ======================
# TAMBAH ROW
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
root.title("Priority Scheduling Simulator (Correct)")
root.geometry("950x650")

tk.Label(root, text="CPU Scheduling - Priority (Non Preemptive)", font=("Arial", 16)).pack(pady=5)

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

# CANVAS SCROLL
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