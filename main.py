import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
# 1. Setup your API Key
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Error: API Key not found. Make sure you created the .env file!")
genai.configure(api_key=API_KEY)

# Select the model (Gemini 1.5 Flash is fast and free-tier friendly)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- THE TOOL (Concept 1) ---
# This simulates a database lookup. In a real company, this would connect to Shopify/Salesforce.
def lookup_order_tool(order_id):
    # Mock database
    mock_db = {
        "ORD-123": "Shipped - Arriving Tuesday",
        "ORD-456": "Processing - Out of Stock",
        "ORD-789": "Delivered - Left on Porch"
    }
    return mock_db.get(order_id, "Order Not Found")

# --- CONTEXT ENGINEERING (Concept 2) ---
# This is the "brain" or policy we give the agent so it sounds professional.
COMPANY_POLICY = """
You are a support agent for 'TechGadget Inc.'
1. Always be polite and empathetic.
2. If the customer is angry, apologize first.
3. Never promise a refund without manager approval.
4. Sign off with 'Best, TechGadget Support Team'.
"""

# --- MULTI-AGENT SYSTEM (Concept 3) ---

def run_triage_system(incoming_email):
    print("------------------------------------------------------")
    print(f"📥 INCOMING EMAIL:\n'{incoming_email}'")
    
    # === AGENT 1: THE MANAGER (Categorizer) ===
    print("\n🕵️  Agent 1 (Manager) is analyzing...")
    
    triage_prompt = f"""
    Analyze this email: "{incoming_email}"
    
    1. Identify the Category (Billing, Technical, Order Status, or General).
    2. Identify the Sentiment (Happy, Neutral, Frustrated, Angry).
    3. Extract any Order ID (starts with ORD-). If none, say "None".
    
    Return the answer in this format:
    Category: [Value]
    Sentiment: [Value]
    OrderID: [Value]
    """
    
    response_1 = model.generate_content(triage_prompt)
    triage_result = response_1.text.strip()
    print(f"📋 Analysis Result:\n{triage_result}")
    
    # Parse the result (simple string extraction for this demo)
    order_id = "None"
    lines = triage_result.split('\n')
    for line in lines:
        if "OrderID:" in line:
            order_id = line.split(":")[1].strip()

    # === THE TOOL EXECUTION ===
    order_status_info = ""
    if order_id != "None" and order_id != "[Value]":
        print(f"\n🔧 Tool Activated: Looking up {order_id}...")
        status = lookup_order_tool(order_id)
        order_status_info = f"Current Order Status for {order_id}: {status}"
        print(f"✅ Tool Result: {status}")
    else:
        print("\n🚫 No tool needed (no order ID found).")

    # === AGENT 2: THE WRITER (Responder) ===
    print("\n✍️  Agent 2 (Writer) is drafting response...")
    
    writer_prompt = f"""
    {COMPANY_POLICY}
    
    TASK: Write a reply to the customer email below.
    
    CONTEXT from Agent 1:
    {triage_result}
    
    DATA from Tool:
    {order_status_info}
    
    Original Email: "{incoming_email}"
    """
    
    response_2 = model.generate_content(writer_prompt)
    final_email = response_2.text
    
    print("\n🚀 FINAL DRAFT RESPONSE:")
    print(final_email)
    print("------------------------------------------------------")

# --- TEST RUN ---
# Let's test it with a fake angry customer email
test_email = "I am so mad! Where is my stuff? My order number is ORD-456 and I've been waiting for weeks!"
run_triage_system(test_email)