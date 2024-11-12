import requests
import base64
import uuid

def store_credit_card(shop_id, shop_password, merchant_info, card_info, member_id, create_new_member, url="https://stg.openapi.mul-pay.jp/credit/storeCard"):

    auth_value = base64.b64encode(f'{shop_id}:{shop_password}'.encode()).decode('utf-8')

    headers = {
        'Authorization': f'Basic {auth_value}',
        'Content-Type': 'application/json',
        'Idempotency-Key': str(uuid.uuid4())
    }

    data = {
        "merchant": merchant_info,
        "creditStoringInformation": {
            "card": card_info,
            "onfileCardOptions": {
                "memberId": member_id,
                "createNewMember": create_new_member
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)

    return response.status_code, response.text

shop_id = 'your_shop_id'
shop_password = 'your_shop_password'
merchant_info = {
    "name": "default_name",
    "nameKana": "de",
    "nameAlphabet": "defaultstore",
    "nameShort": "ds",
    "contactName": "サポート窓口",
    "contactEmail": "support@example.com",
    "contactPhone": "0120-123-456",
    "contactOpeningHours": "10:00-18:00"
}
card_info = {
    "cardNumber": "4211111111111111",
    "expiryMonth": 12,
    "expiryYear": 2025,
    "cardholdName": "",
}
member_id = ""
create_new_member = True

status_code, response_text = store_credit_card(shop_id, shop_password, merchant_info, card_info, member_id, create_new_member)
print(status_code)
print(response_text)
