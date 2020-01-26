from rest_framework import serializers
from .models import AccountBasic


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBasic
        fields = '__all__'
