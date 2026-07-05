import tkinter as tk
from tkinter import ttk, messagebox

import database

def refresh_tree(tree):
  for row in tree.get_children(): tree.delete(row)
  rows = database.get_recharges()
  for row in rows:
    rid, product, date, qty, buy_price, sell_price = row
    tree.insert(
      "",
      "end",
      values=(
        rid,
        date,
        product,
        qty,
        buy_price,
        sell_price
      )
    )

def open_history():
  win = tk.Toplevel()
  win.title("Recharge History")
  win.geometry("1000x700")

  columns = (
    "ID",
    "Date",
    "Product",
    "Quantity",
    "Buy price",
    "Sell price"
  )

  tree = ttk.Treeview(
    win,
    columns=columns,
    show="headings"
  )

  for col in columns: tree.heading(col, text=col)
  tree.column("ID", width=60, anchor="center")
  tree.column("Date", width=120, anchor="center")
  tree.column("Product", width=300)
  tree.column("Quantity", width=120, anchor="center")
  tree.column("Buy price", width=120, anchor="e")
  tree.column("Sell price", width=120, anchor="e")
  tree.pack(fill="both", expand=True, padx=10, pady=10)
  button_frame = tk.Frame(win)
  button_frame.pack(pady=10)
  
  def clear_history():
    answer = messagebox.askyesno(
      "Clear History",
      "Delete all recharge history?"
    )
  
    if not answer: return
    database.clear_recharge_history()
    refresh_tree(tree)
  
  ttk.Button(
    button_frame,
    text="Clear History",
    command=clear_history
  ).pack()
  refresh_tree(tree)
