from django.contrib import admin
from .models import (Product, Order, OrderItem, Sale, Room, Message)

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
   list_display = ['code', 'name', 'description', 'image', 'is_active', 'price', 'stock', 'remaining' ]
class OrderAdmin(admin.ModelAdmin):
    list_display = ['code', 'ordered_date', 'ordered']
    
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['code', 'created_at', 'item', 'quantity', 'ordered']
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id',  'amount',  'sales_date']
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id',  'group_name',]
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id',  'msg', 'room', 'sender']
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)

    
