from rest_framework import serializers
from deals.models import Deal
from django.contrib.auth.models import User
from items.models import Item


class GemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name']
        queryset = Item.objects.all()


class TopUsersSerializers(serializers.ModelSerializer):
    total_spent = serializers.IntegerField(read_only=True, required=False)
    gems = GemSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'total_spent', 'gems']


class DealSerializer(serializers.ModelSerializer):
    # deals = serializers.FileField(required=False)
    class Meta:
        model = Deal
        fields = '__all__'
