import requests
import base64
import uuid

def create_member(member_id, member_name, shop_id, shop_password, url="https://stg.openapi.mul-pay.jp/member/create"):
    auth_value = base64.b64encode(f'{shop_id}:{shop_password}'.encode()).decode('utf-8')

    headers = {
        'Authorization': f'Basic {auth_value}',
        'Content-Type': 'application/json',
        'Idempotency-Key': str(uuid.uuid4())
    }

    data = {
        "memberId": member_id,
        "memberName": member_name,
        "additionalOptions": {}
    }

    response = requests.post(url, headers=headers, json=data)

    return response.status_code, response.text

shop_id = 'your_shopid'
shop_password = 'your_shoppassword'
status_code, response_text = create_member("your_memberId", "your_memberName", shop_id, shop_password)
print(status_code)
print(response_text)
