
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('by-tag/<int:tag_id>/', OrderListCreateView.as_view(), name='orders-by-tag-id'),
    path('by-tag/<str:tag_name>/', OrderListCreateView.as_view(), name='orders-by-tag-name'),
    path('', OrderListCreateView.as_view(), name='order-list'),

]