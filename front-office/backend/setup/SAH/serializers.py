from SAH.models import *
from rest_framework import serializers
import base64
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError

class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField('get_token')
    def get_token(self, obj):
        return self.context.get("token")
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_superuser','date_joined', 'token')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfilee
        fields = ('id', 'username', 'first_name', 'last_name', 'id_card')
    

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)
    class Meta:
        model = User
        fields = ["email", "username", "password"]
    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs["email"]).exists()
        if email_exists:
            raise ValidationError("Email has already been used")
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user

class ConsultReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultReservation
        fields = ('id', 'scheduled_date', 'consult_date', 'pacient_id_card', 'doctor_id_card', 'status', 'description')
    