import requests
import uuid
import base64

def charge_credit_on_file(
    shop_id, shop_password,
    merchant_info, order_info, payer_info,
    credit_onfile_info, fraud_detection_info,
    url="https://stg.openapi.mul-pay.jp/credit/on-file/charge"
):

    auth_value = base64.b64encode(f'{shop_id}:{shop_password}'.encode()).decode('utf-8')

    headers = {
        'Authorization': f'Basic {auth_value}',
        'Content-Type': 'application/json',
        'Idempotency-Key': str(uuid.uuid4())
    }

    data = {
        "merchant": merchant_info,
        "order": order_info,
        "payer": payer_info,
        "creditOnfileInformation": credit_onfile_info,
        "fraudDetectionData": fraud_detection_info
    }

    response = requests.post(url, headers=headers, json=data)

    return response.status_code, response.text

shop_id = 'your_shop_id'
shop_password = 'shop_password'
merchant_info = {
    "name":"default",
    "nameKana":"デフォルト",
    "nameAlphabet":"default",
    "nameShort":"d",
    "contactName":"サポート窓口",
    "contactEmail":"support@example.com",
    "contactPhone":"0120-123-456",
    "contactOpeningHours":"10:00-18:00",
    "callbackUrl": "https://merchant.example.com/callback"
}
order_info = {
    "orderId": "order-003",
    "transactionType": "CIT",
    "amount": 50000  
}
payer_info = {
    "name": "your_test_name"
}
credit_onfile_info = {
    "onfileCard": {
        "memberId": "your_memberId",
        "type": "CREDIT_CARD",
        "cardId": "1",
    },
    "creditChargeOptions": {
        "authorizationMode": "AUTH",
        "useTds2": False
    }
}
fraud_detection_info = {
    "userId": "your_userId"
}

status_code, response_text = charge_credit_on_file(
    shop_id, shop_password,
    merchant_info, order_info, payer_info,
    credit_onfile_info, fraud_detection_info
)
print(status_code)
print(response_text)
