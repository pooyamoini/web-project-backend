from rest_framework import serializers
from .models import AccountGeneric


class AccountGenericSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountGeneric
        fields = '__all__'
