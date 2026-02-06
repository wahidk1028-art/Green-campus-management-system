import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

# ------------------ FETCH DATA ------------------
conn = sqlite3.connect("waste_log.db")
df = pd.read_sql_query("SELECT * FROM waste_log", conn)
conn.close()

if df.empty:
    print("No waste data found. Run camera detection first.")
    exit()

# ------------------ MAIN WINDOW ------------------
root = tk.Tk()
root.title("Green Campus – AI Waste Dashboard")
root.geometry("900x600")

title = tk.Label(root, text="♻️ AI Waste Segregation Dashboard",
                 font=("Arial", 22, "bold"))
title.pack(pady=10)

# ------------------ TABLE ------------------
frame = tk.Frame(root)
frame.pack(pady=10)

tree = ttk.Treeview(frame, columns=list(df.columns), show='headings')
for col in df.columns:
    tree.heading(col, text=col)
    tree.column(col, width=200)

for _, row in df.iterrows():
    tree.insert("", tk.END, values=list(row))

tree.pack()

# ------------------ GRAPHS ------------------
waste_counts = df['waste_type'].value_counts()

plt.figure(figsize=(10,4))

plt.subplot(1,2,1)
waste_counts.plot(kind='bar')
plt.title("Waste Distribution")
plt.xlabel("Waste Type")
plt.ylabel("Count")

plt.subplot(1,2,2)
waste_counts.plot(kind='pie', autopct='%1.1f%%')
plt.title("Waste Percentage")
plt.ylabel("")

plt.tight_layout()
plt.show()

root.mainloop()
