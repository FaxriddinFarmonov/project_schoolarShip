from rest_framework import serializers

class SubjectUpdateSerializer(serializers.Serializer):
    rid = serializers.CharField(max_length=50)
    inn = serializers.CharField(max_length=50)
    passport = serializers.CharField(max_length=50)

    last_name = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=100)

    gender = serializers.CharField(max_length=10)
    marital_status = serializers.CharField(max_length=20)
    birth_date = serializers.DateField()

    home_flat = serializers.CharField(max_length=20, required=False, allow_blank=True)
    home_building = serializers.CharField(max_length=20, required=False, allow_blank=True)
    home_house = serializers.CharField(max_length=20, required=False, allow_blank=True)
    home_street = serializers.CharField(max_length=100, required=False, allow_blank=True)
    home_city = serializers.CharField(max_length=100, required=False, allow_blank=True)

    email = serializers.EmailField()
    mobile = serializers.CharField(max_length=20)

    income = serializers.DecimalField(max_digits=12, decimal_places=2)
    question = serializers.CharField(max_length=200)
    answer = serializers.CharField(max_length=200)
