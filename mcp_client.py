# mcp_client.py
import requests


class MCPClient:
    def __init__(self, server_url):
        self.server_url = server_url


    def get_products_price_gt_100(self):
        """
        Fetch products whose price is greater than $100 from the /api/products endpoint.
        """
        try:
            url = f"{self.server_url}/api/products"
            response = requests.get(url)
            response.raise_for_status()
            products = response.json()
            filtered = [p for p in products if p.get('price', 0) > 100]
            return filtered
        except Exception as e:
            return {"error": str(e)}

    def get_all_products(self):
        url = f"{self.server_url}/api/products"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching products: {e}")
            return []

    def query(self, prompt):
        # Placeholder for MCP query logic
        return f"Simulated response for: {prompt}"

