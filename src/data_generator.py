import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()
random.seed(42)

DB_PATH = "data/erp.db"

def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)

def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_id   INTEGER PRIMARY KEY,
            vendor       TEXT,
            amount       REAL,
            status       TEXT,
            due_date     TEXT,
            department   TEXT
        );

        CREATE TABLE IF NOT EXISTS stock_items (
            item_id       INTEGER PRIMARY KEY,
            item_name     TEXT,
            quantity      INTEGER,
            reorder_level INTEGER,
            warehouse     TEXT,
            unit_cost     REAL
        );

        CREATE TABLE IF NOT EXISTS employees (
            emp_id      INTEGER PRIMARY KEY,
            name        TEXT,
            department  TEXT,
            salary      REAL,
            join_date   TEXT,
            status      TEXT
        );

        CREATE TABLE IF NOT EXISTS sales_orders (
            order_id   INTEGER PRIMARY KEY,
            customer   TEXT,
            product    TEXT,
            revenue    REAL,
            region     TEXT,
            order_date TEXT
        );

        CREATE TABLE IF NOT EXISTS kpi_snapshots (
            kpi_id      INTEGER PRIMARY KEY,
            metric_name TEXT,
            value       REAL,
            month       TEXT,
            department  TEXT
        );
    """)
    conn.commit()

def seed_invoices(conn, n=50):
    statuses = ["Paid", "Pending", "Overdue"]
    departments = ["Finance", "IT", "Operations", "HR", "Sales"]
    rows = []
    for i in range(1, n + 1):
        due = datetime.today() + timedelta(days=random.randint(-30, 60))
        rows.append((
            i,
            fake.company(),
            round(random.uniform(5000, 500000), 2),
            random.choice(statuses),
            due.strftime("%Y-%m-%d"),
            random.choice(departments)
        ))
    conn.executemany(
        "INSERT OR IGNORE INTO invoices VALUES (?,?,?,?,?,?)", rows
    )
    conn.commit()
    print(f"  Inserted {n} invoices")

def seed_stock_items(conn, n=40):
    products = [
        "Steel Rods", "Circuit Boards", "Hydraulic Pumps",
        "Safety Helmets", "Conveyor Belts", "Copper Wires",
        "Ball Bearings", "Sensor Modules", "Cooling Fans", "Power Cables"
    ]
    warehouses = ["Mumbai", "Delhi", "Pune", "Chennai", "Hyderabad"]
    rows = []
    for i in range(1, n + 1):
        rows.append((
            i,
            random.choice(products) + f" (Batch-{i})",
            random.randint(0, 500),
            random.randint(50, 100),
            random.choice(warehouses),
            round(random.uniform(100, 5000), 2)
        ))
    conn.executemany(
        "INSERT OR IGNORE INTO stock_items VALUES (?,?,?,?,?,?)", rows
    )
    conn.commit()
    print(f"  Inserted {n} stock items")

def seed_employees(conn, n=30):
    departments = ["Finance", "IT", "Operations", "HR", "Sales", "Manufacturing"]
    rows = []
    for i in range(1, n + 1):
        join = datetime.today() - timedelta(days=random.randint(30, 3000))
        rows.append((
            i,
            fake.name(),
            random.choice(departments),
            round(random.uniform(30000, 150000), 2),
            join.strftime("%Y-%m-%d"),
            random.choice(["Active", "Active", "Active", "On Leave"])
        ))
    conn.executemany(
        "INSERT OR IGNORE INTO employees VALUES (?,?,?,?,?,?)", rows
    )
    conn.commit()
    print(f"  Inserted {n} employees")

def seed_sales_orders(conn, n=60):
    products = ["ERP License", "Support Package", "Hardware Bundle",
                "Training Module", "Custom Integration"]
    regions = ["North", "South", "East", "West", "Central"]
    rows = []
    for i in range(1, n + 1):
        order_date = datetime.today() - timedelta(days=random.randint(0, 180))
        rows.append((
            i,
            fake.company(),
            random.choice(products),
            round(random.uniform(10000, 800000), 2),
            random.choice(regions),
            order_date.strftime("%Y-%m-%d")
        ))
    conn.executemany(
        "INSERT OR IGNORE INTO sales_orders VALUES (?,?,?,?,?,?)", rows
    )
    conn.commit()
    print(f"  Inserted {n} sales orders")

def seed_kpis(conn):
    metrics = [
        ("Gross Margin %", "Finance"),
        ("Inventory Turnover", "Operations"),
        ("Employee Attrition %", "HR"),
        ("Sales Growth %", "Sales"),
        ("On-Time Delivery %", "Operations"),
        ("Cost Per Hire", "HR"),
        ("Overdue Invoice Count", "Finance"),
    ]
    months = ["2024-10", "2024-11", "2024-12", "2025-01", "2025-02", "2025-03"]
    rows = []
    kpi_id = 1
    for metric, dept in metrics:
        for month in months:
            rows.append((
                kpi_id,
                metric,
                round(random.uniform(10, 95), 2),
                month,
                dept
            ))
            kpi_id += 1
    conn.executemany(
        "INSERT OR IGNORE INTO kpi_snapshots VALUES (?,?,?,?,?)", rows
    )
    conn.commit()
    print(f"  Inserted {len(rows)} KPI snapshots")

def run():
    print("Building ERP database...")
    conn = get_connection()
    create_tables(conn)
    seed_invoices(conn)
    seed_stock_items(conn)
    seed_employees(conn)
    seed_sales_orders(conn)
    seed_kpis(conn)
    conn.close()
    print("\nDone! ERP database ready at data/erp.db")

if __name__ == "__main__":
    run()