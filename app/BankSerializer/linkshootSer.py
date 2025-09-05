from rest_framework import serializers

class ContractUpdateSerializer(serializers.Serializer):
    Rid = serializers.CharField(max_length=100)
    ClientRid = serializers.CharField(max_length=100)
    TypeRid = serializers.CharField(max_length=100)
    BranchCode = serializers.CharField(max_length=50)
