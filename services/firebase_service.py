import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os

# Initialize Firebase with the service account file
cred = credentials.Certificate("sarvam-c2476-firebase-adminsdk-fbsvc-dc5492ca25.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def initialize_products():
    """Initialize products in Firestore if they don't exist"""
    products_ref = db.collection('products')
    
    initial_products = [
        {
            "name": "Organic Almond Butter",
            "price": 200,
            "stock": 50
        },
        {
            "name": "Cold-Pressed Juice",
            "price": 50,
            "stock": 100
        },
        {
            "name": "Organic Granola",
            "price": 150,
            "stock": 30
        },
        {
            "name": "Herbal Tea",
            "price": 120,
            "stock": 20
        }
    ]
    
    # Add products if they don't exist (case-insensitive check)
    for product in initial_products:
        product_name_lower = product['name'].lower()
        existing_products = [doc for doc in products_ref.get() 
                           if doc.to_dict()['name'].lower() == product_name_lower]
        
        if not existing_products:
            products_ref.add(product)
            print(f"Added product: {product['name']}")

def get_product_stock():
    """Get real-time product stock from Firestore"""
    products_ref = db.collection('products')
    products = products_ref.get()
    return [doc.to_dict() for doc in products]

def update_product_stock(product_name: str, quantity: int):
    """Update product stock in Firestore"""
    products_ref = db.collection('products')
    # Convert product name to lowercase for comparison
    product_name_lower = product_name.lower()
    
    # Get all products and find match with case-insensitive comparison
    all_products = products_ref.get()
    matching_products = [doc for doc in all_products 
                        if doc.to_dict()['name'].lower() == product_name_lower]
    
    if not matching_products:
        print(f"Product not found: {product_name}")
        return False
        
    product_doc = matching_products[0]
    current_stock = product_doc.to_dict()['stock']
    new_stock = current_stock - quantity
    
    if new_stock >= 0:
        product_doc.reference.update({'stock': new_stock})
        print(f"Updated stock for {product_name}: {current_stock} -> {new_stock}")
        return True
    
    print(f"Insufficient stock for {product_name}: requested {quantity}, available {current_stock}")
    return False

def create_order(customer_info: dict, order_details: list):
    """Create a new order in Firestore"""
    orders_ref = db.collection('orders')
    
    order_data = {
        "customer_name": customer_info.get("name", ""),
        "phone": customer_info.get("phone", ""),
        "address": customer_info.get("address", ""),
        "zipcode": customer_info.get("zipcode", ""),
        "products": order_details,  # Array of {name, quantity}
        "order_date": datetime.now(),
        "status": "placed"
    }
    
    # Add order to Firestore
    order_doc = orders_ref.add(order_data)
    order_id = order_doc[1].id  # Get the auto-generated document ID
    
    # Update the document with its ID
    orders_ref.document(order_id).update({
        "order_id": order_id
    })
    
    print(f"Created order: {order_id}")
    return order_id

def get_order(order_id: str):
    """Retrieve order details from Firestore"""
    order_ref = db.collection('orders').document(order_id)
    order = order_ref.get()
    if order.exists:
        return order.to_dict()
    return None 