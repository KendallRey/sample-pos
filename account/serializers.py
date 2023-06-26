from rest_framework import serializers

from .models import Account

class AccountUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
        ]

class AccountUserNameEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = [
            "username",
            "email",
        ]