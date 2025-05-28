from lib.db.connection import get_connection

class Customer:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<Customer {self.id}: {self.name}>"

    @classmethod
    def create(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO customers (name) VALUES (?)", (name,))
        conn.commit()
        return cls(cursor.lastrowid, name)

    @classmethod
    def get_all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM customers").fetchall()
        return [cls(id=row[0], name=row[1]) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM customers WHERE name = ?", (name,)).fetchone()
        if row:
            return cls(id=row[0], name=row[1])
        return None
