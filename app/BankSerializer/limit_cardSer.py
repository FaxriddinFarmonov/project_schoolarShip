# app/serializers/limit_card.py
from rest_framework import serializers

class CardRestrictionSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16)
    max_value = serializers.DecimalField(max_digits=18, decimal_places=2)
    currency = serializers.CharField(max_length=5)
