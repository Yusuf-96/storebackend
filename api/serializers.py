from rest_framework import serializers
from .models import (Product, OrderItem, Order, Sale, Room, Message)
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'code', 'name', 'description', 'price', 'image', 'stock', 'created_at', 'remaining', 'is_active']
        
        
class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    final_price = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ['id', 'code', 'item', 'quantity', 'final_price', 'ordered', 'created_at', ]
        
    # def get_item(self, obj):
    #     return ItemSerializer(obj.item).data
    
    def get_final_price(self, obj):
        return obj.get_final_price()
    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total= serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['id', 'total', 'code', 'ordered_date', 'items']
        
        
    # def get_order_items(self, obj):
    #     return OrderItemSerializer(obj.items.all(), many=True).data
    
    def get_total(self, obj):
        return obj.get_total()

class SaleSerializer(serializers.ModelSerializer):
    sale = OrderSerializer(many=True)
    class Meta:
        model = Sale
        fields = ['id',  'sale', 'amount', 'sales_date'] 
    

class MessageSerializer(serializers.ModelSerializer):
    # sender = serializers.IntegerField(read_only=True)
    # room = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'code', 'msg', 'sender', 'room']
        
    # def create(self, validated_data):
    #     return Message.objects.create(**validated_data)


class RoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)
    class Meta:
        model = Room
        fields = ['id', 'code', 'group_name', 'members', 'messages']
        
    # def create(self, validated_data):
    #     messages_data = validated_data.pop('messages')
        
    #     room = Room.objects.create(**validated_data)
        
    #     for message_data in messages_data:
    #         Message.objects.create(room=room, **track_data)
            
    #     return room
        