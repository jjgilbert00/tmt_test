
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, DeactivateOrderView, EmbargoedOrderView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('<int:pk>/deactivate/', DeactivateOrderView.as_view(), name='deactivate-order'),
    path('embargoed/', EmbargoedOrderView.as_view(), name='embargoed-order'),
    path('', OrderListCreateView.as_view(), name='order-list'),

]