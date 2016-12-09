# coding=utf-8
from django.contrib.auth import authenticate
from rest_framework import serializers
from accounts.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'gender')


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'password','email', 'gender')
        write_only_fields = ('password',)

    def clean_password(self):
        if len(self.cleaned_data.get('password')) < 6:
            raise serializers.ValidationError(u"Mínimo 6 caracteres")
        else:
            return self.cleaned_data.get('password')

    def create(self, validated_data):
        user = User(first_name=validated_data.get('first_name'),
                    last_name=validated_data.get('last_name'), email=validated_data.get('email'),
                    gender=validated_data.get('gender'))
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(error_messages={"blank": "Este campo es obligatorio"})
    password = serializers.CharField(error_messages={"blank": "Este campo es obligatorio"})

    def validate(self, attrs):
        self.user_cache = authenticate(email=attrs["email"], password=attrs["password"])
        if not self.user_cache:
            raise serializers.ValidationError("Invalid login")
        return attrs

    def get_user(self):
        return self.user_cache
