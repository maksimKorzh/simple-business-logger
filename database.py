import sqlite3
from datetime import date

DB_NAME = "business.db"

def connect():
  return sqlite3.connect(DB_NAME)

def create_database():
  conn = connect()
  cur = conn.cursor()

  cur.execute("""
    CREATE TABLE IF NOT EXISTS products(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT UNIQUE NOT NULL,
      quantity INTEGER NOT NULL,
      buy_price REAL NOT NULL,
      sell_price REAL NOT NULL
    )
  """)

  cur.execute("""
    CREATE TABLE IF NOT EXISTS sales_days(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      date TEXT NOT NULL
    )
  """)

  cur.execute("""
    CREATE TABLE IF NOT EXISTS day_inventory(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      sales_day_id INTEGER,
      product_id INTEGER,
      start_qty INTEGER,
      sold_qty INTEGER,
      end_qty INTEGER,
      buy_price REAL,
      sell_price REAL,
      FOREIGN KEY(sales_day_id) REFERENCES sales_days(id),
      FOREIGN KEY(product_id) REFERENCES products(id)
    )
  """)

  cur.execute("""
    CREATE TABLE IF NOT EXISTS recharges(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      product_id INTEGER,
      date TEXT,
      quantity INTEGER,
      buy_price REAL,
      sell_price REAL,
      FOREIGN KEY(product_id) REFERENCES products(id)
    )
  """)

  conn.commit()
  cur.execute("SELECT COUNT(*) FROM products")

  if cur.fetchone()[0] == 0:
    products = [
      ("Claw Hammer", 24, 6.50, 11.90),
      ("Rubber Mallet", 18, 5.00, 9.50),
      ("Phillips Screwdriver", 35, 2.10, 5.00),
      ("Flat Screwdriver", 28, 2.00, 4.80),
      ("Adjustable Wrench", 14, 7.00, 13.50),
      ("Combination Pliers", 22, 5.20, 10.50),
      ("Needle Nose Pliers", 16, 5.80, 11.20),
      ("Bench Vice", 6, 28.00, 49.00),
      ("Tape Measure 5m", 40, 2.80, 6.50),
      ("Spirit Level 60cm", 11, 8.00, 15.00),
      ("Utility Knife", 30, 1.50, 3.90),
      ("Hand Saw", 10, 9.50, 18.50),
      ("Hacksaw", 9, 10.20, 19.90),
      ("Wood Chisel", 20, 3.20, 7.20),
      ("Socket Set", 8, 24.00, 45.00),
      ("Hex Key Set", 19, 4.20, 8.90),
      ("Pipe Wrench", 12, 11.50, 22.00),
      ("Paint Brush", 33, 1.10, 3.20),
      ("Silicone Gun", 13, 4.80, 9.50),
      ("Box of Nails", 50, 1.40, 3.80),
      ("Wood Screws", 60, 1.90, 4.50),
      ("Wall Anchors", 45, 1.60, 3.90)
    ]

    cur.executemany("""
      INSERT INTO products(
        name,
        quantity,
        buy_price,
        sell_price
      )
      VALUES(?,?,?,?)
    """, products)

    conn.commit()
  conn.close()


def get_products():
  conn = connect()
  cur = conn.cursor()

  cur.execute("""
    SELECT *
    FROM products
    ORDER BY name
  """)

  rows = cur.fetchall()
  conn.close()
  return rows


def product_exists(name):
  conn = connect()
  cur = conn.cursor()

  cur.execute(
    "SELECT COUNT(*) FROM products WHERE LOWER(name)=LOWER(?)",
    (name,)
  )

  exists = cur.fetchone()[0] > 0
  conn.close()
  return exists


def add_product(name, quantity, buy_price, sell_price):
  conn = connect()
  cur = conn.cursor()

  cur.execute("""
    INSERT INTO products(
      name,
      quantity,
      buy_price,
      sell_price
    )
    VALUES(?,?,?,?)
  """, (
    name,
    quantity,
    buy_price,
    sell_price
  ))

  conn.commit()
  conn.close()


def delete_product(product_id):
  conn = connect()
  cur = conn.cursor()

  cur.execute(
    "DELETE FROM products WHERE id=?",
    (product_id,)
  )

  conn.commit()
  conn.close()


def recharge_product(product_id, amount, buy_price, sell_price):
  conn = connect()
  cur = conn.cursor()

  cur.execute("""
    UPDATE products
    SET
      quantity = quantity + ?,
      buy_price = ?,
      sell_price = ?
    WHERE id = ?
  """, (
    amount,
    buy_price,
    sell_price,
    product_id
  ))

  cur.execute("""
    INSERT INTO recharges(
      product_id,
      date,
      quantity,
      buy_price,
      sell_price
    )
    VALUES(?,?,?,?,?)
  """, (
    product_id,
    date.today().isoformat(),
    amount,
    buy_price,
    sell_price
  ))

  conn.commit()
  conn.close()

def get_recharges():
  conn = connect()
  cur = conn.cursor()

  cur.execute("""
    SELECT
      r.id,
      p.name,
      r.date,
      r.quantity,
      r.buy_price,
      r.sell_price
    FROM recharges r
    JOIN products p
      ON p.id = r.product_id
    ORDER BY r.id DESC
  """)

  rows = cur.fetchall()
  conn.close()
  return rows

def clear_recharge_history():
  conn = connect()
  cur = conn.cursor()
  cur.execute("DELETE FROM recharges")
  conn.commit()
  conn.close()

def create_sales_day():
  conn = connect()
  cur = conn.cursor()

  cur.execute(
    "INSERT INTO sales_days(date) VALUES(?)",
    (date.today().isoformat(),)
  )

  sales_day_id = cur.lastrowid
  conn.commit()
  conn.close()
  return sales_day_id

def save_day_inventory(
  sales_day_id,
  product_id,
  start_qty,
  sold_qty,
  end_qty,
  buy_price,
  sell_price
):
  conn = connect()
  cur = conn.cursor()

  cur.execute("""
    INSERT INTO day_inventory(
      sales_day_id,
      product_id,
      start_qty,
      sold_qty,
      end_qty,
      buy_price,
      sell_price
    )
    VALUES(?,?,?,?,?,?,?)
  """, (
    sales_day_id,
    product_id,
    start_qty,
    sold_qty,
    end_qty,
    buy_price,
    sell_price
  ))

  conn.commit()
  conn.close()

def update_quantity(product_id, quantity):
  conn = connect()
  cur = conn.cursor()
  cur.execute(
    "UPDATE products SET quantity=? WHERE id=?",
    (quantity, product_id)
  )
  conn.commit()
  conn.close()

def get_sales_days():
  conn = connect()
  cur = conn.cursor()
  cur.execute("""
    SELECT
      sd.id,
      sd.date,
      SUM(di.sold_qty * di.sell_price),
      SUM(di.sold_qty * (di.sell_price - di.buy_price)),
      SUM(di.sold_qty)
    FROM sales_days sd
    JOIN day_inventory di
      ON sd.id = di.sales_day_id
    GROUP BY sd.id
    ORDER BY sd.id DESC
  """)

  rows = cur.fetchall()
  conn.close()
  return rows


def get_sales_day_details(sales_day_id):
  conn = connect()
  cur = conn.cursor()

  cur.execute("""
    SELECT
      p.name,
      di.start_qty,
      di.sold_qty,
      di.end_qty,
      di.buy_price,
      di.sell_price,
      di.sold_qty * di.sell_price,
      di.sold_qty * (di.sell_price - di.buy_price)
    FROM day_inventory di
    JOIN products p
      ON p.id = di.product_id
    WHERE di.sales_day_id = ?
    ORDER BY p.name
  """, (sales_day_id,))

  rows = cur.fetchall()
  conn.close()
  return rows
