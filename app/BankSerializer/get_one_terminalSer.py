from rest_framework import serializers

class TerminalReadSerializer(serializers.Serializer):
    terminal_name = serializers.CharField(max_length=100)
