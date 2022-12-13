from rest_framework.decorators import api_view, APIView, authentication_classes, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import viewsets
from apps.accounts.models import CustomUser
from apps.accounts.serializers import UserSerializer

# Create your views here.

class GetUserView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.filter(is_superuser=False).order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes= [IsAuthenticated]