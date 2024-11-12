import base64
import requests
import uuid

def verify_card(shop_id, shop_password, order_id, member_id, card_number, expiry_month, expiry_year, payer_name):
    # Generate the Authorization header using base64 encoding
    auth_value = base64.b64encode(f'{shop_id}:{shop_password}'.encode()).decode('utf-8')
    # Generate a unique Idempotency-Key to ensure the request is idempotent
    idempotency_key = str(uuid.uuid4())

    # Set up the headers with the Authorization and Content-Type
    headers = {
        'Authorization': f'Basic {auth_value}',
        'Content-Type': 'application/json',
        'Idempotency-Key': idempotency_key,
    }

    # API endpoint for card verification
    url = 'https://stg.openapi.mul-pay.jp/credit/verifyCard'

    # The request payload with necessary information
    data = {
        "merchant": {
            "name": "default",
            "nameKana": "デフォルト",
            "nameAlphabet": "default",
            "nameShort": "d",
            "contactName": "サポート窓口",
            "contactEmail": "support@example.com",
            "contactPhone": "0120-123-456",
            "contactOpeningHours": "10:00-18:00",
            "callbackUrl": "https://merchant.example.com/callback",
        },
        "order": {
            "orderId": order_id,  # Change the orderId when executing the request
            "transactionType": "CIT",  
            "addressMatch": True,
        },
        "payer": {
            "name": payer_name  
        },
        "creditVerificationInformation": {
            "card": {
                "cardNumber": card_number,  # Card number to be verified
                "expiryMonth": expiry_month, 
                "expiryYear": expiry_year, 
            },
            "creditVerificationOptions": {
                "authorizationMode": "AUTH", 
                "useTds2": False,
                "itemCode": "0000990", 
            },
            "onfileCardOptions": {
                "memberId": member_id,  # Member ID associated with the card
            },
        },
        "additionalOptions": {},
    }

    # Send the POST request to the API
    response = requests.post(url, headers=headers, json=data)

    # Output the status code of the response
    print(f"Status Code: {response.status_code}")
    try:
        # If the response is in JSON format, parse and print error details
        error_details = response.json()
        print(f"Error Title: {error_details.get('title')}")
        print(f"Error Detail: {error_details.get('detail')}")
        print(f"Error Type: {error_details.get('type')}")
        print(f"Error Instance: {error_details.get('instance')}")
    except ValueError:
        # If the response is not in JSON format, print the raw response text
        print("Error response is not in JSON format.")
        print(response.text)

    # Return the status code and response text for further processing
    return response.status_code, response.text


# Example usage of the function
shop_id = 'your_shop_id'
shop_password = 'your_shop_password'
order_id = 'order-001'
member_id = 'your_member_id'
card_number = '4211111111111111'
expiry_month = '12'
expiry_year = '2025'
payer_name = 'testName'

# Call the verify_card function to process the card verification
status_code, response_text = verify_card(shop_id, shop_password, order_id, member_id, card_number, expiry_month, expiry_year, payer_name)

# Print the response details
print(f"Response Code: {status_code}")
print(f"Response Text: {response_text}")
