from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from core.models import Item, Order, UserProfile


from core.api.serializers import ItemSerializer, OrderSerializer, UserProfileSerializer



@api_view(['GET',])
def hello(request):
    
    return Response({
        'hello' : "From the Keval"
    })


class HomeView(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializers = ItemSerializer(items, many=True)
        return Response(serializers.data)    

class ProductDetail(APIView):
    def get(self, request, slug):
        try:
            item = Item.objects.get(slug=slug)
            serializers = ItemSerializer(item)
            return Response(serializers.data)    
        except Exception as e:
            content = {'please move along': 'nothing to see here'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

class OrderSummary(APIView):
    permission_classes = [IsAuthenticated,]
    authentication = [TokenAuthentication,]

    def get(self, request, format=None):
        content = {}
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            serializer = OrderSerializer(order)
            content = serializer.data
            return Response(content)
        except ObjectDoesNotExist:
            return Response({"Empty":"You Don't Have Items in Your Cart"}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated,]
    authentication = [TokenAuthentication,]

    def get(self, request, format=None):
        try:
            order = Order.objects.filter(user=request.user, ordered=True)
            order_Serializer = OrderSerializer(order, many=True)
            # print(order_Serializer.data)

            user_profile = UserProfile.objects.get(user=request.user)
            user_profile_Serializer = UserProfileSerializer(user_profile)

            context = {
                "user_profile" : user_profile_Serializer.data, 
                "orders": order_Serializer.data,
            }
            return Response(context, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"AuthenticationError":"You are not Authenticated"}, status=status.HTTP_400_BAD_REQUEST)
