from rest_framework import serializers

class CardLookupSerializer(serializers.Serializer):
    card_ext_rid = serializers.CharField(max_length=25)
