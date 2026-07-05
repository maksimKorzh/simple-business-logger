import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import database

def refresh_tree(tree):
  for row in tree.get_children(): tree.delete(row)
  products = database.get_products()
  for product in products:
    pid, name, qty, buy, sell = product
    tree.insert(
      "",
      "end",
      values=(
        pid,
        name,
        qty,
        f"{buy:.2f}",
        f"{sell:.2f}"
      )
    )

def add_product_window(tree):
  win = tk.Toplevel()
  win.title("Add Product")
  win.geometry("350x300")
  tk.Label(win, text="Product Name").pack(pady=(10, 0))
  name_entry = tk.Entry(win)
  name_entry.pack()
  tk.Label(win, text="Quantity").pack(pady=(10, 0))
  qty_entry = tk.Entry(win)
  qty_entry.pack()
  tk.Label(win, text="Buy Price").pack(pady=(10, 0))
  buy_entry = tk.Entry(win)
  buy_entry.pack()
  tk.Label(win, text="Sell Price").pack(pady=(10, 0))
  sell_entry = tk.Entry(win)
  sell_entry.pack()

  def save():
    name = name_entry.get().strip()
    if name == "":
      messagebox.showerror("Error", "Product name cannot be empty.")
      return
    if database.product_exists(name):
      messagebox.showerror("Error", "This product already exists.")
      return
    try:
      qty = int(qty_entry.get())
      buy = float(buy_entry.get())
      sell = float(sell_entry.get())
    except ValueError:
      messagebox.showerror(
        "Error",
        "Quantity must be integer.\nPrices must be numbers."
      )
      return

    database.add_product(name, qty, buy, sell)
    refresh_tree(tree)
    win.destroy()

  ttk.Button(
    win,
    text="Save Product",
    command=save
  ).pack(pady=20)

def delete_product_window(tree):
  selected = tree.selection()
  if not selected:
    messagebox.showwarning(
      "No selection",
      "Please select a product."
    )
    return

  values = tree.item(selected[0])["values"]
  product_id = values[0]
  product_name = values[1]

  answer = messagebox.askyesno(
    "Delete Product",
    f"Delete '{product_name}'?"
  )

  if not answer: return
  database.delete_product(product_id)
  refresh_tree(tree)

def recharge_product_window(tree):
  selected = tree.selection()
  if not selected:
    messagebox.showwarning(
      "No selection",
      "Please select a product."
    )
    return
  values = tree.item(selected[0])["values"]
  product_id = values[0]
  product_name = values[1]
  current_qty = values[2]
  buy_price = values[3]
  sell_price = values[3]
  win = tk.Toplevel()
  win.title("Recharge Stock")
  win.geometry("300x300")

  tk.Label(
    win,
    text=product_name,
    font=("Arial", 11, "bold")
  ).pack(pady=(10, 5))

  tk.Label(
    win,
    text=f"Current quantity: {current_qty}"
  ).pack()

  tk.Label(
    win,
    text="Quantity to add"
  ).pack(pady=(10, 0))

  amount_entry = tk.Entry(win)
  amount_entry.pack()
  amount_entry.focus()

  tk.Label(
    win,
    text="Buy price"
  ).pack(pady=(10, 0))

  price_entry = tk.Entry(win)
  price_entry.pack()

  tk.Label(
    win,
    text="Sell price"
  ).pack(pady=(10, 0))

  sell_entry = tk.Entry(win)
  sell_entry.pack()
  
  def save():
    try:
      amount = int(amount_entry.get())
      buy_price = float(price_entry.get())
      sell_price = float(sell_entry.get())
    except ValueError:
      messagebox.showerror(
        "Error",
        "Enter a valid integer."
      )
      return

    if amount <= 0:
      messagebox.showerror(
        "Error",
        "Quantity must be greater than zero."
      )
      return

    database.recharge_product(
      product_id,
      amount,
      buy_price,
      sell_price
    )
    refresh_tree(tree)
    win.destroy()

  ttk.Button(
    win,
    text="Recharge",
    command=save
  ).pack(pady=15)

def open_inventory():
  win = tk.Toplevel()
  win.title("Inventory")
  win.geometry("900x550")
  columns = (
    "ID",
    "Name",
    "Quantity",
    "Buy Price",
    "Sell Price"
  )

  tree = ttk.Treeview(
    win,
    columns=columns,
    show="headings",
    height=18
  )

  for col in columns:
    tree.heading(col, text=col)
  
  tree.column("ID", width=60, anchor="center")
  tree.column("Name", width=300)
  tree.column("Quantity", width=100, anchor="center")
  tree.column("Buy Price", width=120, anchor="e")
  tree.column("Sell Price", width=120, anchor="e")
  tree.pack(fill="both", expand=True, padx=10, pady=10)
  button_frame = tk.Frame(win)
  button_frame.pack(pady=10)
    
  ttk.Button(
    button_frame,
    text="Add Product",
      command=lambda: add_product_window(tree)
  ).grid(row=0, column=0, padx=5)
    
  ttk.Button(
    button_frame,
    text="Delete Product",
    command=lambda: delete_product_window(tree)
  ).grid(row=0, column=2, padx=5)

  ttk.Button(
    button_frame,
    text="Recharge Stock",
    command=lambda: recharge_product_window(tree)
  ).grid(row=0, column=3, padx=5)

  refresh_tree(tree)
