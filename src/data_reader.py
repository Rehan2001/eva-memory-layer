import sqlite3

DB_PATH = "data/erp.db"

def preview():
    conn = sqlite3.connect(DB_PATH)
    tables = ["invoices", "stock_items", "employees", "sales_orders", "kpi_snapshots"]

    for table in tables:
        rows = conn.execute(f"SELECT * FROM {table} LIMIT 2").fetchall()
        print(f"\n--- {table.upper()} (first 2 rows) ---")
        for row in rows:
            print(row)

    conn.close()

if __name__ == "__main__":
    preview()