# app/BankSerializer/limit_cardSer.py
from rest_framework import serializers

class CardLimitRemoveSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16)  # 16-19 raqamli karta raqami
