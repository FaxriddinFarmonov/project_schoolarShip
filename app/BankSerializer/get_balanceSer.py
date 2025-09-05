from rest_framework import serializers


class CardBalanceSerializer(serializers.Serializer):
    card_pan = serializers.CharField(max_length=16 )