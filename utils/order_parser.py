import json
from llamaapi import LlamaAPI
from config.settings import LLAMA_API_KEY

def extract_order_details(chat_history):
    """Extract ordered products and quantities using LLM"""
    llama = LlamaAPI(LLAMA_API_KEY)
    
    # Join chat history into a conversation format
    conversation = "\n".join([
        f"{'Customer' if msg['sender'] == 'user' else 'Assistant'}: {msg['message']}"
        for msg in chat_history
    ])
    
    messages = [
        {
            "role": "system",
            "content": """You are an order parser. Extract product names and quantities from the conversation.
Return ONLY a JSON array of orders with this exact format:
[
    {"name": "product name in lowercase", "quantity": number},
    ...
]
Include only these products if mentioned:
- organic almond butter
- cold-pressed juice
- organic granola
- herbal tea

If no valid orders found, return empty array []."""
        },
        {
            "role": "user",
            "content": f"Extract orders from this conversation:\n{conversation}"
        }
    ]
    
    api_request = {
        "model": "llama3.1-70b",
        "messages": messages,
        "temperature": 0.1,  # Low temperature for consistent formatting
        "response_format": { "type": "json_object" }  # Force JSON response
    }
    
    try:
        response = llama.run(api_request)
        response_json = json.loads(response.text)
        
        if 'choices' in response_json:
            content = response_json['choices'][0]['message']['content']
            # Parse the JSON string from the content
            orders = json.loads(content)
            
            # Validate the response format
            if isinstance(orders, list):
                valid_orders = []
                valid_products = {'organic almond butter', 'cold-pressed juice', 
                                'organic granola', 'herbal tea'}
                
                for order in orders:
                    if (isinstance(order, dict) and 
                        'name' in order and 
                        'quantity' in order and
                        order['name'].lower() in valid_products and
                        isinstance(order['quantity'], int) and
                        order['quantity'] > 0):
                        valid_orders.append(order)
                
                return valid_orders
                
        return []
        
    except Exception as e:
        print(f"Error parsing order details: {str(e)}")
        return [] 

def extract_customer_info(chat_history):
    """Extract customer information using LLM"""
    llama = LlamaAPI(LLAMA_API_KEY)
    
    conversation = "\n".join([
        f"{'Customer' if msg['sender'] == 'user' else 'Assistant'}: {msg['message']}"
        for msg in chat_history
    ])
    
    messages = [
        {
            "role": "system",
            "content": """Extract customer information from the conversation.
Return ONLY a JSON object with this format:
{
    "name": "full name",
    "phone": "phone number",
    "address": "full address",
    "zipcode": "6-digit code"
}
If any field is not found, use empty string."""
        },
        {
            "role": "user",
            "content": f"Extract customer info from this conversation:\n{conversation}"
        }
    ]
    
    api_request = {
        "model": "llama3.1-70b",
        "messages": messages,
        "temperature": 0.1,
        "response_format": { "type": "json_object" }
    }
    
    try:
        response = llama.run(api_request)
        response_json = json.loads(response.text)
        
        if 'choices' in response_json:
            content = response_json['choices'][0]['message']['content']
            customer_info = json.loads(content)
            return customer_info
            
    except Exception as e:
        print(f"Error extracting customer info: {str(e)}")
    
    return {
        "name": "",
        "phone": "",
        "address": "",
        "zipcode": ""
    } 