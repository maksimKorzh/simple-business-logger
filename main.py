import tkinter as tk
from tkinter import ttk

import database
import inventory
import history
import sales_day
import reports

database.create_database()

window = tk.Tk()
window.title("Business Logger")
window.geometry("200x225")
buttons = tk.Frame(window)
buttons.pack(pady=10)
ttk.Button(
  buttons,
  text="Inventory",
  width=20,
  command=inventory.open_inventory
).grid(row=0, column=0, pady=10)
ttk.Button(
  buttons,
  text="Sales Day",
  command=sales_day.open_sales_day,
  width=20).grid(row=1, column=0, pady=10)
ttk.Button(
  buttons,
  text="Recharges",
  command=history.open_history,
  width=20).grid(row=2, column=0, pady=10)
ttk.Button(
  buttons,
  text="Reports",
  width=20,
  command=reports.open_reports
).grid(row=3, column=0, pady=10)
window.mainloop()
