import sqlite3

def create_sample_database():
    conn = sqlite3.connect("company.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            department TEXT,
            salary REAL,
            years_experience INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            employee_id INTEGER,
            product TEXT,
            amount REAL,
            month TEXT
        )
    """)

    cursor.execute("DELETE FROM employees")
    cursor.execute("DELETE FROM sales")

    employees = [
        (1, "Alice", "Engineering", 95000, 5),
        (2, "Bob", "Marketing", 72000, 3),
        (3, "Carol", "Engineering", 105000, 8),
        (4, "David", "Sales", 68000, 2),
        (5, "Eve", "Marketing", 78000, 4),
        (6, "Frank", "Sales", 82000, 6),
        (7, "Grace", "Engineering", 115000, 10),
        (8, "Henry", "HR", 65000, 1),
    ]

    sales = [
        (1, 1, "Software", 45000, "January"),
        (2, 3, "Hardware", 62000, "January"),
        (3, 4, "Software", 38000, "February"),
        (4, 6, "Services", 29000, "February"),
        (5, 1, "Software", 51000, "March"),
        (6, 3, "Hardware", 71000, "March"),
        (7, 4, "Services", 43000, "April"),
        (8, 6, "Software", 55000, "April"),
    ]

    cursor.executemany(
        "INSERT INTO employees VALUES (?,?,?,?,?)", employees
    )
    cursor.executemany(
        "INSERT INTO sales VALUES (?,?,?,?,?)", sales
    )

    conn.commit()
    conn.close()
    print("Database created!")

if __name__ == "__main__":
    create_sample_database()