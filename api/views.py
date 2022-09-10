from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .serializers import (ItemSerializer, OrderSerializer, SaleSerializer, OrderItemSerializer, RoomSerializer, MessageSerializer)
from .models import (Product, Order, OrderItem, Sale, Room, Message)

# Create your views here.

class ItemsAPIView(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ItemSerializer(products, many=True)
        
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ItemSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
    
class ItemAPIView(APIView):
    def get(self, request, code, format = None):
        if request.method == 'GET':
            item = Product.objects.get(code=code)
            serializer = ItemSerializer(item)
            
            return Response(serializer.data)
        
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
    
    def put(self, request, format=None):
        code = self.code is None
        if request.method == 'PUT':
            item = Product.objects.filter(code=code)
            serializer = ItemSerializer(instance = item, data = request.data)
            
            serializer.is_valid(raise_exception = True)
            serializer.save()
            
            return Response(serializer.data, {'message':'success'})
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
    def delete(self, request, format=None):
        code = self.code is None
        if request.method == 'DELETE':
            item = Product.objects.filter(code=code)
            item.delete()
            
            return Response(status=status.HTTP_200_OK)
        
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
    
class OrderAPI(APIView):
    def get(self, request, format=None):
        if request.method == 'GET':
            order = Order.objects.filter( ordered=False).first()
           
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(status = status.HTTP_400_BAD_REQUEST)
                
        
    def post(self, request, format=None):
        code = request.data.get('code', None)
        if code is None:
            return Response({'error':'Invalid data'})
        item = get_object_or_404(Product, code=code)
        order_qs = Order.objects.filter(ordered=False)
        
        if order_qs.exists():
            order = order_qs[0]
            
            #check if order item is in th order
            if order.items.filter(item__code=item.code).exists():
                order_item = OrderItem.objects.filter(item=item, ordered=False)[0]
                if order_item.quantity > 1:
                    order_item.quantity-=1
                   
                    new_stock = order_item.item.remaining
                    new_stock += 1   
                    Product.objects.filter(code=code).update(remaining=new_stock)
                    order_item.save()
                                        
                else:
                    new_stock = order_item.item.remaining
                    new_stock += 1   
                    Product.objects.filter(code=code).update(remaining=new_stock, is_active=True)
                    order.items.remove(order_item)
                return Response(status=status.HTTP_200_OK)
            return Response({'massage':'the item is not on your cart'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'You do not have any active order'}, status=status.HTTP_400_BAD_REQUEST)
                
    def delete(self, request, code, format=None):
        if request.method=='DELETE':
            order_item_qs = OrderItem.objects.filter(code=code)
            item_id = order_item_qs[0].item.code
            item_rm = order_item_qs[0].item.remaining
            old_stock = order_item_qs[0].quantity + item_rm
            Product.objects.filter(code=item_id).update(remaining= old_stock, is_active=True)
            order_item_qs.delete()
            return Response({'message':'order item deleted'}, status=status.HTTP_200_OK)
         
        return Response({'message':'You cant delete this item'}, status=status.HTTP_400_BAD_REQUEST)
        


class AddToCartAPI(APIView):
    def post(self, request, fomart=None):
        code = request.data.get('code', None)
        
        if code is None:
            return Response({'message':'Invalid data'}, status = status.HTTP_400_BAD_REQUEST)
        
        item = get_object_or_404(Product, code=code)
        
        order_item_qs = OrderItem.objects.filter(item=item,  ordered =False)
        if order_item_qs.exists():
            order_item = order_item_qs[0]
            if order_item.item.remaining > 0:
                order_item.quantity +=1
                new_stock = order_item.item.remaining
                new_stock -= 1
                Product.objects.filter(code=code).update(remaining=new_stock)
                order_item.save()
            else:
                Product.objects.filter(code=code).update(is_active=False)
                print('Out of Stock')
        elif item.remaining > 0:
            new_stock = item.remaining
            new_stock -= 1
            Product.objects.filter(code=code).update(remaining=new_stock)
            order_item = OrderItem.objects.create(item=item,  ordered=False)
            order_item.save()
        else:
           Product.objects.filter(code=code).update(is_active=False)
           print('Out of Stock') 
            
        order_qs = Order.objects.filter( ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if not order.items.filter(item__id = order_item.id).exists():
                order.items.add(order_item)
                return Response(status = status.HTTP_200_OK)
        
        ordered_date = timezone.now()
        order = Order.objects.create( ordered_date=ordered_date)
        order.items.add(order_item)
        return Response(status = status.HTTP_200_OK)
    

class SaleItemAPI(APIView):
    def get(slef, request, format=None):
        if request.method=='GET':
            
            sale = Sale.objects.all()
            serializer = SaleSerializer(sale, many=True)
            return Response(serializer.data)
            
            sales = user.sale_set.all()
            serializer = SaleSerializer(sales, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response({'message':'no sales yet'})
      
       
    def post(self, request, foramt=None):
        order = Order.objects.get(user=request.user, ordered=False)
        try:
            amount = order.get_total()

            # create sales
            sales = Sale()
            sales.user = self.request.user
            sales.amount = amount
            sales.save()

            # asseign sale to order

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.order = sales
            order.save()

            return Response({'message':'saled'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message':'Unable to sale'})


class GroupsApiView(APIView):
    def get(self, request, format=None):
        if request.method == 'GET':
            
            rooms =  Room.objects.all()
            
            serializer = RoomSerializer(rooms, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(status = status.HTTP_400_BAD_REQUEST)
        
    
    
class GroupApiView(APIView):
    def get(self, request, code,  fomart=None):
        # code = request.data.get('code', None)
        if request.method == 'GET':
            
            room = Room.objects.get(code=code)
            
            serializer = RoomSerializer(room)
            
            return Response(serializer.data, status= status.HTTP_200_OK)
        
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
    
class MessageAPiView(APIView):
    def post(self, request,  fomart=None):
        serializer = MessageSerializer(data = request.data)
        
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_200_OK)
          
        
    

            
        
    
