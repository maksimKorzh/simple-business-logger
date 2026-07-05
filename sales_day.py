import tkinter as tk
from tkinter import ttk, messagebox

import database

def open_sales_day():

  products = database.get_products()

  if len(products) == 0:
    messagebox.showinfo(
      "Sales Day",
      "No products in inventory."
    )
    return

  win = tk.Toplevel()

  win.title("Sales Day")
  win.geometry("700x700")

  header = tk.Frame(win)
  header.pack(fill="x", padx=10, pady=10)

  tk.Label(
    header,
    text="Product",
    width=35,
    anchor="w",
    font=("Arial", 10, "bold")
  ).grid(row=0, column=0)

  tk.Label(
    header,
    text="Sold",
    width=10,
    font=("Arial", 10, "bold")
  ).grid(row=0, column=1)

  canvas_frame = tk.Frame(win)
  canvas_frame.pack(
    fill="both",
    expand=True,
    padx=10
  )

  canvas = tk.Canvas(
    canvas_frame,
    highlightthickness=0
  )

  canvas.pack(
    fill="both",
    expand=True
  )

  body = tk.Frame(canvas)

  canvas.create_window(
    (0, 0),
    window=body,
    anchor="nw"
  )

  body.bind(
    "<Configure>",
    lambda e: canvas.configure(
      scrollregion=canvas.bbox("all")
    )
  )

  def wheel(event):

    if event.num == 4:
      canvas.yview_scroll(-1, "units")

    elif event.num == 5:
      canvas.yview_scroll(1, "units")

    else:
      canvas.yview_scroll(
        int(-event.delta / 120),
        "units"
      )

  canvas.bind_all("<MouseWheel>", wheel)
  canvas.bind_all("<Button-4>", wheel)
  canvas.bind_all("<Button-5>", wheel)

  entries = []

  for i, product in enumerate(products):

    pid, name, qty, buy, sell = product

    tk.Label(
      body,
      text=name,
      width=35,
      anchor="w"
    ).grid(
      row=i,
      column=0,
      sticky="w",
      pady=2
    )

    sold_entry = tk.Entry(
      body,
      width=8
    )

    sold_entry.insert(0, "0")

    sold_entry.grid(
      row=i,
      column=1,
      padx=5
    )

    entries.append(
      (
        pid,
        qty,
        buy,
        sell,
        sold_entry
      )
    )

  result = tk.Label(
    win,
    text="Revenue: 0.00    Profit: 0.00",
    font=("Arial", 11, "bold")
  )

  result.pack(pady=10)

  def calculate():

    revenue = 0
    profit = 0

    for pid, start, buy, sell, entry in entries:

      try:
        sold = int(entry.get())

      except ValueError:
        messagebox.showerror(
          "Error",
          "Invalid quantity."
        )
        return False

      if sold < 0 or sold > start:
        messagebox.showerror(
          "Error",
          f"Invalid sold quantity for product."
        )
        return False

      revenue += sold * sell
      profit += sold * (sell - buy)

    result.config(
      text=f"Revenue: {revenue:.2f}    Profit: {profit:.2f}"
    )

    return True

  def save():

    if not calculate():
      return

    sales_day_id = database.create_sales_day()

    for pid, start, buy, sell, entry in entries:

      sold = int(entry.get())

      end = start - sold

      database.save_day_inventory(
        sales_day_id,
        pid,
        start,
        sold,
        end,
        buy,
        sell
      )

      database.update_quantity(
        pid,
        end
      )

    messagebox.showinfo(
      "Done",
      "Sales Day saved."
    )

    win.destroy()

  buttons = tk.Frame(win)
  buttons.pack(pady=10)

  ttk.Button(
    buttons,
    text="Calculate",
    command=calculate
  ).grid(
    row=0,
    column=0,
    padx=5
  )

  ttk.Button(
    buttons,
    text="Save Sales Day",
    command=save
  ).grid(
    row=0,
    column=1,
    padx=5
  )
