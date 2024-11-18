from django.shortcuts import render
from rest_framework import generics

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'tag_name' in self.kwargs:
            queryset = queryset.filter(tags__name__iexact=self.kwargs['tag_name'])
        elif 'tag_id' in self.kwargs:
            queryset = queryset.filter(tags__id=self.kwargs['tag_id'])
        return queryset
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer
