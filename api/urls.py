from django.urls import path
from .import views

urlpatterns = [
    path('products/', views.ItemsAPIView.as_view()),
    path('product/detail/<str:code>/', views.ItemAPIView.as_view()),
    path('order/', views.OrderAPI.as_view()),
    path('order/<str:code>/delete/', views.OrderAPI.as_view()),
    path('cart/', views.AddToCartAPI.as_view()),
    path('sale-items/', views.SaleItemAPI.as_view()),
    path('rooms/', views.GroupsApiView.as_view()),
    path('room/', views.GroupApiView.as_view()),
    path('room/<str:code>/', views.GroupApiView.as_view()),
    path('messages/', views.MessageAPiView.as_view()),
]