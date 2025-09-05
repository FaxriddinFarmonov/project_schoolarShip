# app/serializers.py
from rest_framework import serializers

class ModifyCardSerializer(serializers.Serializer):
    extrid = serializers.CharField(required=True, max_length=50)
    contract2rid = serializers.CharField(required=True, max_length=50)
    cur_branch_code = serializers.CharField(required=True, max_length=10)
