from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Notification

from .serializers import NotificationSerializer

# Create your views here.
class NotificationViewSet(ListModelMixin, GenericViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.none()
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        queryset = (
            Notification.objects.filter(
                to_user=self.request.user
            )
            .order_by("-created")
        )
        return queryset
