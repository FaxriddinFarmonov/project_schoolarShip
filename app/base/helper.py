import requests
import json

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjQwOTEsInJvbGUiOm51bGwsImRhdGEiOnsiaWQiOjQwOTEsIm5hbWUiOiJGYXJtb25vdiBGYXhyaWRkaW4gRmFyeG9kIG8nZydsaSIsImVtYWlsIjoiZmF4cmlkZGluLmZhcm1vbm92LmRldkBnbWFpbC5jb20iLCJyb2xlIjpudWxsLCJhcGlfdG9rZW4iOm51bGwsInN0YXR1cyI6ImFjdGl2ZSIsInNtc19hcGlfbG9naW4iOiJlc2tpejIiLCJzbXNfYXBpX3Bhc3N3b3JkIjoiZSQkayF6IiwidXpfcHJpY2UiOjUwLCJ1Y2VsbF9wcmljZSI6MTE1LCJ0ZXN0X3VjZWxsX3ByaWNlIjpudWxsLCJiYWxhbmNlIjoyNDcwLCJpc192aXAiOjAsImhvc3QiOiJzZXJ2ZXIxIiwiY3JlYXRlZF9hdCI6IjIwMjMtMDUtMjdUMTE6MjI6NTQuMDAwMDAwWiIsInVwZGF0ZWRfYXQiOiIyMDIzLTA3LTE5VDA3OjM3OjAzLjAwMDAwMFoiLCJ3aGl0ZWxpc3QiOm51bGwsImhhc19wZXJmZWN0dW0iOjAsImJlZWxpbmVfcHJpY2UiOjUwfSwiaWF0IjoxNjk0OTUwNDE0LCJleHAiOjE2OTc1NDI0MTR9.QEn_EBhqbVFNlJgIZbYlHYU-9YCbh1ei6-8tH10FJgw"
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
    print(response.content)
    return response.json()


