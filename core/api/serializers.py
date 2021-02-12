from rest_framework import serializers
from core.models import Item, OrderItem, Order, UserProfile
from django.conf import settings

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={ 'input_type': 'password'}, write_only=True)

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['password', 'password2', 'email', 'username']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'