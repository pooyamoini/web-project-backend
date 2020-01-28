from rest_framework import serializers
from .models import AccountBasic
from .models import LoggInBasic


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBasic
        fields = '__all__'


class LogginSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoggInBasic
        fields = '__all__'
