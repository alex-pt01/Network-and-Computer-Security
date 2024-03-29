

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

class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfilee
        fields = ('id', 'username', 'specialization', 'first_name', 'last_name', 'id_card')
    
class ExternalLabProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalLabProfilee
        fields = ('id', 'username', 'lab_name', 'phone_number', 'address')

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


class ConsultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consult
        fields = ('id', 'scheduled_date', 'consult_date', 'pacient_id_card', 'doctor_id_card', 'status', 'description')
    
class ConsultRoomReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultRoomReservation
        fields = ('id', 'floor', 'room', 'consult_id')

class ExternalLabsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalLabs
        fields = ('id', 'pacient_id_card', 'doctor_id_card', 'lab_name', 'consult_lab_date', 'form_update_date', 'intro', 'materials', 'procedure', 'results', 'hash')
    