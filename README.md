# GreenLife Foods Chatbot

An AI-powered chatbot for handling FMCG product orders and customer service queries. Built with Streamlit, Firebase, and Llama API.

## Features
- Real-time product stock management
- Order tracking with unique IDs
- Customer information management
- Multi-step order validation
- Natural conversation flow
- Order cancellation handling

## Setup Instructions

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/greenlife_chatbot.git
cd greenlife_chatbot
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Set Up Environment Variables**
Create a `.env` file in the root directory:
```env
LLAMA_API_KEY=your_llama_api_key
```

4. **Firebase Setup**
- Create a new Firebase project at [Firebase Console](https://console.firebase.google.com/)
- Generate a new private key from Project Settings > Service Accounts
- Save the JSON file as `sarvam-c2476-firebase-adminsdk-fbsvc-dc5492ca25.json` in the root directory
- Initialize Firestore database with two collections:
  - `products`
  - `orders`

5. **Run the Application**
```bash
streamlit run app.py
```

## Project Structure
```
greenlife_chatbot/
├── app.py                  # Main Streamlit application
├── config/
│   └── settings.py        # Configuration settings
├── services/
│   ├── firebase_service.py # Firebase operations
│   └── llama_api.py       # LLM integration
├── utils/
│   └── order_parser.py    # Order parsing utilities
└── templates/
    └── responses.py       # Response templates
```

## Prompt Engineering Approach

The chatbot uses a structured prompt engineering approach:

1. **Clear Role Definition**
   - Establishes the chatbot's identity and purpose
   - Sets conversational boundaries
   - Maintains consistent personality

2. **Strict Information Flow**
   - Sequential information collection
   - One question at a time policy

3. **Context Awareness**
   - Maintains conversation history
   - Avoids repeating collected information
   - Handles conversation state
   - Remembers customer details within session

4. **Error Prevention**
   - Stock validation before order confirmation
   - PIN code format verification
   - Price calculation accuracy
   - Input validation at each step

5. **Natural Language Processing**
   - Conversational tone while maintaining formality
   - Clear confirmation steps
   - Structured response format
   - Friendly yet professional interactions

## Example Conversation

Bot: Hi, I am Harsh. How can I help you today?

User: i want to cancel my previous order

Bot: Sorry to hear that you want to cancel your previous order. Can you please tell me your name and contact number so I can pass this information to our team and they'll be able to assist you further?

User: harsh 949830291

Bot: Thank you for sharing that information, Harsh. A human from our team will reach out to you shortly to assist with cancelling your previous order.

User: alright, can I place a new order

Bot: I'd be happy to help you with a new order. Before we get started, can you please tell me what you'd like to order and how many packets you'd like to purchase?

User: do you have tea

Bot: We have Herbal Tea available, and it's priced at ₹120 per packet. We currently have 14 packets in stock. Would you like to order some? If yes, how many packets would you like?

User: yeah, 3 packets of that

Bot: So you'd like to order 3 packets of our Herbal Tea, which would come out to be ₹360 (₹120 x 3). We have enough stock to fulfill this order.

Would you like to order anything else along with the Herbal Tea?

User: nah that's it

Bot: So, to confirm, your order is 3 packets of Herbal Tea, and the total comes out to be ₹360.

Can you please share your address where you'd like the order to be delivered?

User: 14th street, bengaluru, 560066

Bot: I've got that noted down. So, your order details are:

3 packets of Herbal Tea (₹360)
Delivery address: 14th street, Bengaluru, 560066
Pincode: 560066 (looks good, 6 digits as required)
Is there anything else you'd like to know or confirm before I place the order?

User: that's it

Bot: The order has been placed. Thank you for shopping with us, Harsh. Have a great day! Your order ID is: ULaz56SFXxasYPdoStWc

## Firebase Collections Structure

### Products Collection
```json
{
    "name": "Product Name",
    "price": 120,
    "stock": 50
}
```

### Orders Collection
```json
{
    "customer_name": "Customer Name",
    "phone": "Contact Number",
    "address": "Delivery Address",
    "zipcode": "6-digit code",
    "products": [
        {
            "name": "Product Name",
            "quantity": 3
        }
    ],
    "order_date": "Timestamp",
    "status": "placed",
    "order_id": "Unique ID"
}
```

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details

## Support
For support, please email shandilyaharsh2001@gmail.com or text 8431263004.
