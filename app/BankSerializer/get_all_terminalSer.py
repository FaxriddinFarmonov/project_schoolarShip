from rest_framework import serializers

class TerminalLookupSerializer(serializers.Serializer):
    terminal = serializers.CharField(max_length=200,required=True)

