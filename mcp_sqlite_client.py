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

    def get_order_details(self, prompt):
        """
        Dynamically fetch order details from the 'order' table based on context in the prompt.
        Supported contexts:
        - Fetch by order id
        - Fetch all orders
        - Fetch by channel
        """
        import re
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            print(f"Executing get_order_details with prompt: {prompt}")

            # Check for order id
            order_id_match = re.search(r"order id\s*:?\s*(\d+)", prompt, re.IGNORECASE)
            print(f"Executing order_id_match with match: {order_id_match}")

            if order_id_match:
                order_id = order_id_match.group(1)
                query = "SELECT * FROM 'order' WHERE id = ?"
                print(f"Executing SQL: {query} with order_id={order_id}")
                cursor.execute(query, (order_id,))
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                conn.close()
                return [dict(zip(columns, row)) for row in rows]

            # Check for channel
            # channel_match = re.search(r"channel\s*:?\s*([\w-]+)", prompt, re.IGNORECASE)
            # print(f"Executing channel_match with match: {channel_match}")
            # if channel_match:
            #     channel = channel_match.group(1)
            #     query = "SELECT * FROM 'order' WHERE channel = ?"
            #     print(f"Executing SQL: {query} with channel={channel}")
            #     cursor.execute(query, (channel,))
            #     columns = [desc[0] for desc in cursor.description]
            #     rows = cursor.fetchall()
            #     conn.close()
            #     return [dict(zip(columns, row)) for row in rows]

            # Check for all orders
            if re.search(r"all orders|fetch all|list all", prompt, re.IGNORECASE):
                query = "SELECT * FROM 'order' limit 10"
                print(f"Executing SQL: {query}")
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                print(f"Fetched {len(rows)} orders")
                conn.close()
                return [dict(zip(columns, row)) for row in rows]

            # Default: return nothing or error
            conn.close()
            return {"error": "No valid order context found in prompt."}
        except Exception as e:
            return {"error": str(e)}