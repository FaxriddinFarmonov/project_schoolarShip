from rest_framework import serializers

class CardActivationSerializer(serializers.Serializer):
    card_pan = serializers.CharField(max_length=16, required=True)
