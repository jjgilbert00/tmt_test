
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView


urlpatterns = [
    path('<int:order_id>/tags/', OrderTagListCreateView.as_view(), name='order-tags'),
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('', OrderListCreateView.as_view(), name='order-list'),
]