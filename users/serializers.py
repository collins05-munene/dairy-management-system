from rest_framework import serializers

from .models import Admin, Clerk, Collector, Farmer, Route

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


class BaseUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = [
            'id', 'first_name', 'middle_name', 'last_name', 'phone_number', 'password', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    
class FarmerSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = Farmer
        fields = BaseUserSerializer.Meta.fields + ['number_of_cows', 'route_or_location']


class CollectorSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = Collector
        fields = BaseUserSerializer.Meta.fields + ['collection_area']


class ClerkSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = Clerk


class AdminSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = Admin


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=['farmer', 'collector', 'clerk', 'admin'])