import requests
import json

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjQwOTEsInJvbGUiOm51bGwsImRhdGEiOnsiaWQiOjQwOTEsIm5hbWUiOiJGYXJtb25vdiBGYXhyaWRkaW4gRmFyeG9kIG8nZydsaSIsImVtYWlsIjoiZmF4cmlkZGluLmZhcm1vbm92LmRldkBnbWFpbC5jb20iLCJyb2xlIjpudWxsLCJhcGlfdG9rZW4iOm51bGwsInN0YXR1cyI6ImFjdGl2ZSIsInNtc19hcGlfbG9naW4iOiJlc2tpejIiLCJzbXNfYXBpX3Bhc3N3b3JkIjoiZSQkayF6IiwidXpfcHJpY2UiOjUwLCJ1Y2VsbF9wcmljZSI6MTE1LCJ0ZXN0X3VjZWxsX3ByaWNlIjpudWxsLCJiYWxhbmNlIjoyNTIwLCJpc192aXAiOjAsImhvc3QiOiJzZXJ2ZXIxIiwiY3JlYXRlZF9hdCI6IjIwMjMtMDUtMjdUMTE6MjI6NTQuMDAwMDAwWiIsInVwZGF0ZWRfYXQiOiIyMDIzLTA3LTE5VDA2OjU1OjAzLjAwMDAwMFoiLCJ3aGl0ZWxpc3QiOm51bGwsImhhc19wZXJmZWN0dW0iOjB9LCJpYXQiOjE2ODk3NTE5ODAsImV4cCI6MTY5MjM0Mzk4MH0.fV6DFDFEGRQ9zZRnJvapImCRruDzWHIsIfLZLIXKN3k"
def send_sms(phone,otp):
    url = "https://notify.eskiz.uz/api/message/sms/send"
    msg = f"maxfiy kod  {otp}"
    print(otp,phone)
    data = {
            "mobile_phone" : str(phone),
            "message" :msg,
            "from" : "4546",
            "callback_url" : "http://0000.uz/test.php"
    }
    print(data)
    headers = {
        "Authorization" : f"Bearer {token}"
    }

    response = requests.post(url,data=data,headers=headers)
    print(response)
    return response.json()


