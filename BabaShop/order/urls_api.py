from django.urls import path
from .views_api import CreateOrderView, DeleteOrderView, PaidOrderView, PayOrderView, UnpaidOrderView


urlpatterns = [
    path('shop/<slug:slug>/order/', CreateOrderView.as_view(), name='create_order_api'),
    path('shop/<slug:slug>/order/<int:pk>/', DeleteOrderView.as_view(), name='delete_order_api'),
    path('shop/<slug:slug>/order/<int:pk>/pay/', PayOrderView.as_view(), name='pay_order_api'),
    path('open/order/', UnpaidOrderView.as_view(), name='open_order_api'),
    path('closed/order/', PaidOrderView.as_view(), name='closed_order_api'),

]