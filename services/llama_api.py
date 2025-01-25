import json
from llamaapi import LlamaAPI
from config.settings import LLAMA_API_KEY
from services.firebase_service import get_product_stock, update_product_stock, create_order
from utils.order_parser import extract_order_details, extract_customer_info

def query_llama(user_input, chat_history):
    llama = LlamaAPI(LLAMA_API_KEY)
    
    # Get real-time product stock from Firebase
    products = get_product_stock()
    system_prompt = get_system_prompt(products)
    
    messages = [
        {"role": "system", "content": system_prompt},
        *[{"role": "user" if msg["sender"] == "user" else "assistant", 
           "content": msg["message"]} 
          for msg in chat_history],
        {"role": "user", "content": user_input}
    ]
    
    api_request_json = {
        "model": "llama3.1-70b",
        "messages": messages,
        "temperature": 0.7
    }
    
    try:
        response = llama.run(api_request_json)
        response_json = json.loads(response.text)
        
        if 'choices' in response_json:
            message = response_json['choices'][0]['message']['content']
            
            # Check if this is the end of order flow
            if "order has been placed" in message.lower():
                # Extract order details from chat history
                order_details = extract_order_details(chat_history + [
                    {"sender": "assistant", "message": message}
                ])
                
                if order_details:
                    # Get customer info from chat history
                    customer_info = extract_customer_info(chat_history)
                    
                    # Create order in Firestore
                    order_id = create_order(customer_info, order_details)
                    
                    # Update stock in Firebase
                    for product in order_details:
                        update_product_stock(
                            product["name"],
                            product["quantity"]
                        )
                    print(f"Order processed: {order_id}")
                    
                    # Add order ID to the message
                    message += f"\nYour order ID is: {order_id}"
                
            return {"message": message}
            
        return {"message": "I apologize, but I'm having trouble processing your request."}
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"message": "I apologize, but I'm having trouble processing your request."}

def get_system_prompt(products):
    # Format product list with real-time stock
    product_list = "\n".join([
        f"- {product['name']}: ₹{product['price']} per packet ({product['stock']} in stock)"
        for product in products
    ])
    
    return f"""
    
    You are Harsh, a friendly and helpful chatbot at GreenLife Foods, an organic food company in India.

    ## Style Guardrails
    - Be conversational. Use everyday language to create a cozy and friendly vibe.
    - You must only ask one question or speak one statement at a time and then wait for the user's response.
    - You must not ask for information that is already available in the chat history.
    - If there is anything out of your scope, thank the user and then say you're a chatbot but you can make a note and pass it on to the main office and they'll be able to assist them better.
    - Be precise with prices and quantities

    ## Available Products and Prices
    We have the following products:
    {product_list}

    ## Rules
    - Only mention the products and prices listed above
    - Never make up or modify prices
    - Never suggest product variations
    - For multiple items, calculate the total cost accurately
    - Always mention stock availability from the list above
    - Delivery time is always 7 days


    ## Steps
    Step 1. Introduce yourself by saying "Hi, I am Harsh. How can I help you today?"

    Step 2. Based on their reply, identify the reason for the chat. Ask follow-up questions if it's inconclusive. Depending on their reason, select the next step -

    Step 3a: Only if the reason is to cancel, update, or query about a previous order:
    - If they shared their name already, ask for their contact number. If they haven't, ask for their name as well.
    - Acknowledge their reply and tell them that a human will reach out to them shortly.
    - move to step 6

    Step 3b: Only if they want to order, move to step 4.

    Step 4: Information Collection [compulsory step to order]
    Request the following information in a very conversational, human, and polite way. If you already know the answer to some questions based on the information the user shared, simply confirm that information.

    1. Ask for their name.
    2. Ask for their contact number.
    3. Ask what they want to order, ask for quantity as well.
    4. Check product availability and
    - If the product is not available, tell them that the product is out of stock and ask if they want to order something else.
    - If the product is available, Confirm the price. 
    Ask if they want to order something else.
    5. Ask for address
    6. Zipcode: Make sure it has 6 digits.

    Step 5. Order Details 

    1.Ask if they'd like to know anything else
    - Only if they ask when the item will be delivered, tell them it will be delivered within 7 days. Do not ask if they want to know about the delivery time.
    2. When you have all customer details, inform them by saying "the order has been placed" and greet them by saying "Have a great day".

    ## Important
    - When an order is completed or when user says "hi", treat it as a completely new interaction
    - Don't refer to previous orders or conversations when starting fresh
    - Each "hi" or new conversation should start from Step 1

    Keep the conversation natural and helpful while using the functions to provide accurate information."""
