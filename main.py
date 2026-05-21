import math
import tkinter as tk
from tkinter import messagebox


def average_highest_reversal_floor(N, avg_passenger_carried):
    tot_sum = 0
    for i in range(1, N):
        tot_sum += i ** avg_passenger_carried
    return N - (tot_sum / (N ** avg_passenger_carried))


def calculate():
    try:
        N = int(inputs["N"].get())
        m = float(inputs["m"].get())
        total_people = int(inputs["total_people"].get())
        absentee_percentage = float(inputs["absentee_percentage"].get())
        no_lifts = int(inputs["no_lifts"].get())
        lift_capacity = int(inputs["lift_capacity"].get())
        lift_speed = float(inputs["lift_speed"].get())
        lift_capacity_demand = float(inputs["lift_capacity_demand"].get())
        acc = float(inputs["acc"].get())
        to = float(inputs["to"].get())
        tc = float(inputs["tc"].get())
        tp = float(inputs["tp"].get())
    except ValueError:
        messagebox.showerror("Input error", "Please enter valid numeric values in all fields.")
        return

    absentee_value = absentee_percentage / 100
    population_with_absentees = math.ceil(total_people * (1 - absentee_value))
    avg_passenger_carried = (lift_capacity_demand / 100) * lift_capacity
    result = average_highest_reversal_floor(N, avg_passenger_carried)
    tf = 2 * (m / acc) ** 0.5
    tv = m / lift_speed
    total_time = tf + to + tc
    P = 0.8 * lift_capacity
    S = N * (1 - (1 - (1 / N)) ** P)
    RTT = 2 * result * tv + (S + 1) * (total_time - tv) + 2 * P * tp
    interval = RTT / no_lifts
    avg_waiting_time = (0.4 + ((((1.8 * P) / lift_capacity) - 0.77) ** 2)) * interval
    handling_capacity = (300 * avg_passenger_carried * 100) / (interval * population_with_absentees)

    outputs_text.delete("1.0", tk.END)
    outputs_text.insert(tk.END, f"Population with Absentees: {population_with_absentees}\n\n")
    outputs_text.insert(tk.END, f"1. Average passengers carried = {avg_passenger_carried:.2f}\n")
    outputs_text.insert(tk.END, f"2. Average Highest Reversal Floor = {result:.2f}\n")
    outputs_text.insert(tk.END, f"3. Flight time per floor (tf) = {tf:.2f}\n")
    outputs_text.insert(tk.END, f"4. Transit time per floor (tv) = {tv:.2f}\n")
    outputs_text.insert(tk.END, f"5. Total single-floor time = {total_time:.2f}\n")
    outputs_text.insert(tk.END, f"6. Average waiting time = {avg_waiting_time:.1f} sec\n", "highlight")
    outputs_text.insert(tk.END, f"7. Handling capacity = {handling_capacity:.1f}\n", "highlight")


root = tk.Tk()
root.title("Lift Traffic Calculator")
root.geometry("1400x850")
root.resizable(True, True)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

heading = tk.Label(root, text="LIFT TRAFFIC ANALYSIS", font=(None, 24, "bold"), fg="#1E88E5")
heading.grid(row=0, column=0, columnspan=3, pady=20)

fields = [
    ("N (number of floors)", "N"),
    ("Floor-to-floor height (m)", "m"),
    ("Total population", "total_people"),
    ("Absentee percentage (%)", "absentee_percentage"),
    ("Number of lifts", "no_lifts"),
    ("Capacity per lift", "lift_capacity"),
    ("Lift speed (m/s)", "lift_speed"),
    ("Lift capacity demand (%)", "lift_capacity_demand"),
    ("Acceleration (m/s^2)", "acc"),
    ("Door opening time (s)", "to"),
    ("Door closing time (s)", "tc"),
    ("Passenger transfer time (s)", "tp"),
]

inputs = {}
for row, (label_text, key) in enumerate(fields, start=1):
    label = tk.Label(root, text=label_text, anchor="w")
    label.grid(row=row, column=0, padx=10, pady=6, sticky="w")
    entry = tk.Entry(root, width=20)
    entry.grid(row=row, column=1, padx=10, pady=6)
    
    inputs[key] = entry

calculate_button = tk.Button(root, text="Calculate", command=calculate, width=18, bg="#4CAF50", fg="white")
calculate_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=16)

formula_text = tk.Text(root, width=40, wrap="word", state="normal", bg="#E3F2FD", bd=2, relief="ridge", font=(None, 11), highlightthickness=1, highlightbackground="#90CAF9")
formula_text.grid(row=1, column=2, rowspan=len(fields) + 1, padx=10, pady=10, sticky="nsew")
formula_text.insert(tk.END, "Key formulas used for results:\n\n")
formula_text.insert(tk.END, "1. Average passengers carried per lift:\n")
formula_text.insert(tk.END, "   = (Lift capacity demand / 100) * Lift capacity\n\n")
formula_text.insert(tk.END, "2. Average Highest Reversal Floor:\n")
formula_text.insert(tk.END, "   = Number of floors - (sum of i^average_passengers_carried for i = 1..N) / N^average_passengers_carried\n\n")
formula_text.insert(tk.END, "3. Flight time per floor:\n")
formula_text.insert(tk.END, "   = 2 * sqrt(Floor height / Acceleration)\n\n")
formula_text.insert(tk.END, "4. Transit time per floor:\n")
formula_text.insert(tk.END, "   = Floor height / Lift speed\n\n")
formula_text.insert(tk.END, "5. Total single-floor time:\n")
formula_text.insert(tk.END, "   = Flight time per floor + Door opening time + Door closing time\n\n")
formula_text.insert(tk.END, "6. Average waiting time:\n")
formula_text.insert(tk.END, "   = (0.4 + ( (1.8 * Effective passengers / Lift capacity - 0.77)^2 )) * Interval\n")
formula_text.insert(tk.END, "     Effective passengers = 0.8 * Lift capacity\n\n")
formula_text.insert(tk.END, "7. Handling capacity for 5 minutes:\n")
formula_text.insert(tk.END, "   = (300 * Average passengers carried per lift * 100) / (Interval * Population with absentees)\n")
formula_text.config(state="disabled")

outputs_label = tk.Label(root, text="Results:", anchor="w", font=(None, 10, "bold"))
outputs_label.grid(row=len(fields) + 2, column=0, columnspan=2, sticky="w", padx=10)

outputs_text = tk.Text(root, width=60, height=14, wrap="word", state="normal")
outputs_text.grid(row=len(fields) + 3, column=0, columnspan=2, padx=10, pady=4, sticky="nsew")
root.rowconfigure(len(fields) + 3, weight=1)
outputs_text.tag_configure("highlight", foreground="#D32F2F", font=(None, 10, "bold"), background="#FFF3E0")
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

root.mainloop()