from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from pos.models import Base64ImageField
from .models import Account
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class AccountUserSerializer(serializers.ModelSerializer):

    image = Base64ImageField(required = False)
    class Meta:
        model = Account
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "image",
        ]

class AccountUserNameEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = [
            "username",
            "email",
        ]

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

class AccountUserRegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=Account.objects.all())]
    )

    password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])

    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = ('username', 'password', 'password2',
            'email', 'first_name', 'last_name')
        extra_kwargs = {
        'first_name': {'required': True},
        'last_name': {'required': True}
        }
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
            {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = Account.objects.create(
        username=validated_data['username'],
        email=validated_data['email'],
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
