from mcp_sqlite_client import MCPSQLiteClient
def analyze_users_with_ollama():
    """
    Pull all user data from USER_INFO table using MCPSQLiteClient and analyze results with Ollama.
    """
    sqlite_client = MCPSQLiteClient()
    users = sqlite_client.get_all_users()
    if isinstance(users, dict) and "error" in users:
        return f"Error fetching users: {users['error']}"
    user_text = "\n".join([str(user) for user in users])
    prompt = f"Analyze the following user data and provide insights, patterns, and recommendations:\n{user_text}"
    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['message']['content'].strip()
# agent.py

import ollama
import os
from mcp_client import MCPClient
from dotenv import load_dotenv





def summarize_with_ollama(products):
    product_text = "\n".join([f"{p['name']} (${p['price']})" for p in products])
    prompt = f"Summarize the following products:\n{product_text}"
    response = ollama.chat(
        model="mistral",  # Small, fast model for local use
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['message']['content'].strip()

def read_logs_and_analyze_with_ollama(log_path):
    """
    Reads logs from the given file path and analyzes them using Ollama (Mistral).
    """
    try:
        with open(log_path, 'r') as f:
            logs = f.read()
        prompt = f"Analyze the following application logs and provide insights, errors, and recommendations:\n{logs}"
        response = ollama.chat(
            model="mistral",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"Error reading or analyzing logs: {e}"



def main():
    load_dotenv()
    mcp = MCPClient(server_url="http://127.0.0.1:5000")
    print("MCP Client initialized. Ready for requests.")

    # Example usage:
    # summarize_products(mcp)
    # analyze_logs()

def summarize_products(mcp):
    products = mcp.get_all_products()
    print("All products:", products)
    summary = summarize_with_ollama(products)
    print("Ollama (Mistral) Summary:", summary)

def analyze_logs():
    log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../sre-ai-app/logs/app.log'))
    print(f"\nAnalyzing logs from: {log_path}")
    log_insights = read_logs_and_analyze_with_ollama(log_path)
    print("\nLog Insights from Ollama (Mistral):\n", log_insights)


# Chainlit integration
import chainlit as cl



@cl.on_message
async def handle_message(message):

    load_dotenv()
    mcp = MCPClient(server_url="http://127.0.0.1:5000")
    user_input = message.content.strip().lower()

    results = []

    await cl.Message(content="Step 1: Detecting intent from prompt...").send()

    intent_detected = False

    if any(kw in user_input for kw in ["product", "products", "list products", "show products", "get products"]):
        await cl.Message(content="Step 2: Fetching products from MCP client...").send()
        products = mcp.get_all_products()
        await cl.Message(content="Step 3: Summarizing products with Ollama...").send()
        summary = summarize_with_ollama(products)
        results.append(f"Product Summary:\n{summary}")
        intent_detected = True

    if any(kw in user_input for kw in ["log", "logs", "analyze logs", "show logs", "get logs"]):
        await cl.Message(content="Step 2: Fetching logs from local file...").send()
        log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../sre-ai-app/logs/app.log'))
        await cl.Message(content="Step 3: Analyzing logs with Ollama...").send()
        log_insights = read_logs_and_analyze_with_ollama(log_path)
        results.append(f"Log Insights:\n{log_insights}")
        intent_detected = True

    if any(kw in user_input for kw in ["user", "users", "user info", "list users", "show users", "get users"]):
        await cl.Message(content="Step 2: Fetching user data from SQLite MCP client...").send()
        await cl.Message(content="Step 3: Analyzing user data with Ollama...").send()
        user_insights = analyze_users_with_ollama()
        results.append(f"User Insights:\n{user_insights}")
        intent_detected = True

    # Order details intent detection
    if any(kw in user_input for kw in ["order", "orders", "order id", "fetch order", "list orders", "channel"]):
        await cl.Message(content="Step 2: Fetching order details from SQLite MCP client...").send()
        sqlite_client = MCPSQLiteClient()
        order_details = sqlite_client.get_order_details(message.content)
        await cl.Message(content="Step 3: Summarizing order details with Ollama...").send()
        order_text = "\n".join([str(order) for order in order_details]) if isinstance(order_details, list) else str(order_details)
        prompt = f"Summarize the following order details and provide insights, patterns, and recommendations:\n{order_text}"
        response = ollama.chat(
            model="mistral",
            messages=[{"role": "user", "content": prompt}]
        )
        results.append(f"Order Summary:\n{response['message']['content'].strip()}")
        intent_detected = True

    # If no known keywords, treat as custom prompt for Ollama
    if not intent_detected:
        await cl.Message(content="Step 2: Sending custom prompt to Ollama...").send()
        response = ollama.chat(
            model="mistral",
            messages=[
                {"role": "user", "content": message.content.strip()}
            ]
        )
        results.append(f"Ollama Response:\n{response['message']['content'].strip()}")

    # Send all results
    await cl.Message(content="\n\n".join(results)).send()
