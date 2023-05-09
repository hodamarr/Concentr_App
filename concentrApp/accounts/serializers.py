from rest_framework import serializers
from .models import User
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token


class SignUpSerializers(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        """ check if the mail is unique """
        email_exists = User.objects.filter(email=attrs['email']).exists()

        if email_exists:
            raise ValidationError('this email already used')

        return super().validate(attrs)

    def create(self, validated_data):
        """ hashing the password """
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)

        return user


class CurrentUserExperimentsSerializer(serializers.ModelSerializer):
    Experiments = serializers.StringRelatedField(
        many=True
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email']
