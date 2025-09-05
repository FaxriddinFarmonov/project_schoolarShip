from rest_framework import serializers

class PaymentSerializer(serializers.Serializer):
    extrid = serializers.CharField(max_length=100)   # Token ExtRid
    pan = serializers.CharField(max_length=19)       # Karta raqami
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    currency = serializers.CharField(max_length=3)   # 840 = USD, 860 = UZS
