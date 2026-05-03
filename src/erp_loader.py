import sqlite3
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, "data", "erp.db")

def load_all_documents():
    conn = sqlite3.connect(DB_PATH)
    docs = []

    # Invoices
    rows = conn.execute("SELECT * FROM invoices").fetchall()
    for r in rows:
        docs.append({
            "text": f"Invoice #{r[0]} from vendor '{r[1]}' for amount {r[2]:,.2f} is '{r[3]}', due on {r[4]}, department: {r[5]}.",
            "source": "invoices",
            "id": f"invoice_{r[0]}"
        })

    # Stock items
    rows = conn.execute("SELECT * FROM stock_items").fetchall()
    for r in rows:
        status = "BELOW reorder level" if r[2] < r[3] else "sufficient"
        docs.append({
            "text": f"Stock item '{r[1]}' (ID {r[0]}) has {r[2]} units in {r[4]} warehouse. Reorder level is {r[3]}. Stock is {status}. Unit cost: {r[5]:,.2f}.",
            "source": "stock_items",
            "id": f"stock_{r[0]}"
        })

    # Employees
    rows = conn.execute("SELECT * FROM employees").fetchall()
    for r in rows:
        docs.append({
            "text": f"Employee {r[1]} (ID {r[0]}) works in {r[2]} department with salary {r[3]:,.2f}. Joined on {r[4]}. Status: {r[5]}.",
            "source": "employees",
            "id": f"emp_{r[0]}"
        })

    # Sales orders
    rows = conn.execute("SELECT * FROM sales_orders").fetchall()
    for r in rows:
        docs.append({
            "text": f"Sales order #{r[0]} for customer '{r[1]}', product: '{r[2]}', revenue: {r[3]:,.2f}, region: {r[4]}, date: {r[5]}.",
            "source": "sales_orders",
            "id": f"order_{r[0]}"
        })

    # KPIs
    rows = conn.execute("SELECT * FROM kpi_snapshots").fetchall()
    for r in rows:
        docs.append({
            "text": f"KPI '{r[1]}' for {r[4]} department in {r[3]}: value = {r[2]}.",
            "source": "kpi_snapshots",
            "id": f"kpi_{r[0]}"
        })

    conn.close()
    print(f"Loaded {len(docs)} ERP documents")
    return docs

if __name__ == "__main__":
    docs = load_all_documents()
    print("\nSample document:")
    print(docs[0])