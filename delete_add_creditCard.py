import base64
import requests
import uuid

def get_card_details(shop_id, shop_password, member_id):
    auth_value = base64.b64encode(f'{shop_id}:{shop_password}'.encode()).decode('utf-8')
    headers = {
        'Authorization': f'Basic {auth_value}',
        'Content-Type': 'application/json',
    }

    url = 'https://stg.openapi.mul-pay.jp/credit/getCardDetails' #api
    data = {
        "cardInformation": {
            "onfileCard": {
                "memberId": member_id,
                "type": "CREDIT_CARD",
                # "cardId": "1",
            },
    }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        card_data = response.json()
        return card_data.get('cards', [])
    else:
        print(f"Error fetching card details: {response.status_code}")
        try:
            print("Error details:", response.json())
        except ValueError:
            print("Error response is not in JSON format.")
        return None

def delete_card(shop_id, shop_password, member_id, card_id):
    auth_value = base64.b64encode(f'{shop_id}:{shop_password}'.encode()).decode('utf-8')
    headers = {'Authorization': f'Basic {auth_value}'}

    url = f'https://stg.openapi.mul-pay.jp/credit/on-file/card/{member_id}/{card_id}'
    response = requests.delete(url, headers=headers)

    return response.status_code == 204

def add_card(shop_id, shop_password, member_id, card_data):
    auth_value = base64.b64encode(f'{shop_id}:{shop_password}'.encode()).decode('utf-8')
    idempotency_key = str(uuid.uuid4())

    headers = {
        'Authorization': f'Basic {auth_value}',
        'Content-Type': 'application/json',
        'Idempotency-Key': idempotency_key,
    }

    url = 'https://stg.openapi.mul-pay.jp/credit/storeCard' #api
    data = {
        "merchant":{
        "name":"default",
        "nameKana":"デフォルト",
        "nameAlphabet":"default",
        "nameShort":"d",
        "contactName":"サポート窓口",
        "contactEmail":"support@example.com",
        "contactPhone":"0120-123-456",
        "contactOpeningHours":"10:00-18:00",
    },
        "creditStoringInformation":{
                "card":{
                    "cardNumber": card_data["cardNumber"],
                    "expiryMonth": card_data["expiryMonth"],
                    "expiryYear": card_data["expiryYear"],
                    "holderName": card_data["holderName"]
            },
                "onfileCardOptions": {
                    "memberId": member_id,
            },
            }
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        return response.json()
    else:
        print(f"Failed to add new card. Status Code: {response.status_code}")
        try:
            error_details = response.json()
            print(f"Error Title: {error_details.get('title')}")
            print(f"Error Detail: {error_details.get('detail')}")
            print(f"Error Instance: {error_details.get('instance')}")
        except ValueError:
            print("Error response is not in JSON format.")
            print(response.text)
        return None

def manage_card(shop_id, shop_password, member_id, new_card_data):
    cards = get_card_details(shop_id, shop_password, member_id)

    if cards:
        for card in cards:
            delete_card(shop_id, shop_password, member_id, card['cardId'])

    result = add_card(shop_id, shop_password, member_id, new_card_data)
    if result:
        print("New card added successfully.")
    else:
        print("Failed to add new card.")

shop_id = 'your_shop_id'
shop_password = 'your_shop_password'
member_id = 'your_member_id'
new_card_data = {
    "cardNumber": "4111111111111111",
    "expiryMonth": "12",
    "expiryYear": "2025",
    "holderName": "test01"
}

manage_card(shop_id, shop_password, member_id, new_card_data)
