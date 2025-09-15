import sqlite3

import os

class MCPSQLiteClient:
    def __init__(self, db_path=None):
        if db_path is None:
            self.db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../sre-ai-app/instance/ecommerce.db'))
        else:
            self.db_path = db_path

    def get_all_products(self):
        """
        Fetch all products from the 'products' table in the SQLite database.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, price FROM products")
            rows = cursor.fetchall()
            products = [
                {"id": row[0], "name": row[1], "price": row[2]} for row in rows
            ]
            conn.close()
            return products
        except Exception as e:
            return {"error": str(e)}


    def get_all_users(self):
        """
        Fetch all user data from the 'USER_INFO' table in the SQLite database.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM USER_INFO")
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            users = [dict(zip(columns, row)) for row in rows]
            conn.close()
            return users
        except Exception as e:
            return {"error": str(e)}
