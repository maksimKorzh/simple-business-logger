import tkinter as tk
from tkinter import ttk, messagebox

import database


def open_reports():

  win = tk.Toplevel()

  win.title("Sales Reports")
  win.geometry("850x500")

  columns = (
    "ID",
    "Date",
    "Revenue",
    "Profit",
    "Items Sold"
  )

  tree = ttk.Treeview(
    win,
    columns=columns,
    show="headings"
  )

  for col in columns:
    tree.heading(col, text=col)

  tree.column("ID", width=60, anchor="center")
  tree.column("Date", width=120, anchor="center")
  tree.column("Revenue", width=120, anchor="e")
  tree.column("Profit", width=120, anchor="e")
  tree.column("Items Sold", width=120, anchor="center")

  tree.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
  )

  for row in database.get_sales_days():

    day_id, day, revenue, profit, items = row

    tree.insert(
      "",
      "end",
      values=(
        day_id,
        day,
        f"{revenue:.2f}",
        f"{profit:.2f}",
        items
      )
    )

  def details():

    selected = tree.selection()

    if not selected:
      messagebox.showwarning(
        "Reports",
        "Select a sales day."
      )
      return

    sales_day_id = tree.item(selected[0])["values"][0]

    open_day_details(sales_day_id)

  ttk.Button(
    win,
    text="View Details",
    command=details
  ).pack(pady=10)

def open_day_details(sales_day_id):
  rows = database.get_sales_day_details(sales_day_id)
  win = tk.Toplevel()
  win.title(f"Sales Day #{sales_day_id}")
  win.geometry("1700x550")

  columns = (
    "Product",
    "Start Qty",
    "Sold",
    "End Qty",
    "Buy price",
    "Sell price",
    "Revenue",
    "Profit"
  )

  tree = ttk.Treeview(
    win,
    columns=columns,
    show="headings"
  )

  for col in columns:
    tree.heading(col, text=col)

  tree.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
  )

  total_revenue = 0
  total_profit = 0
  
  for row in rows:
    tree.insert(
      "",
      "end",
      values=(
        row[0],
        row[1],
        row[2],
        row[3],
        f"{row[4]:.2f}",
        f"{row[5]:.2f}",
        f"{row[6]:.2f}",
        f"{row[7]:.2f}"
      )
    )

    total_revenue += row[6]
    total_profit += row[7]

  tk.Label(
    win,
    text=f"Revenue: {total_revenue:.2f}    Profit: {total_profit:.2f}",
    font=("Arial", 11, "bold")
  ).pack(pady=10)
