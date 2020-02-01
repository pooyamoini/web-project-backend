from rest_framework import serializers
from .models import AccountFollowType

class AccountFollowTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = AccountFollowType
        fields = '__all__'
