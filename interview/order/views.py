from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer

class DeactivateOrderView(APIView):
    def post(self, request, pk, format=None):
        try:
            order = Order.objects.get(pk=pk)
            order.deactivate(pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmbargoedOrderView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, format=None):
        date = request.query_params.get('date')
        
        if not date:
            return Response({"error": "date is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            orders = Order.objects.filter(start_date__lte=date, embargo_date__gte=date)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)