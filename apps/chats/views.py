from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response

from .models import Conversation, Message
from .paginaters import MessagePagination

from .serializers import MessageSerializer, ConversationSerializer
from apps.accounts.models import UserProfile
from apps.accounts.serializers import UserProfileSerializer


class ConversationViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.none()
    lookup_field = "name"

    def get_queryset(self):
        queryset = Conversation.objects.filter(
            name__contains=self.request.user.username
        ).order_by()
        return queryset

    def get_serializer_context(self):
        return {"request": self.request, "user": self.request.user}


class MessageViewSet(ListModelMixin, GenericViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.none()
    pagination_class = MessagePagination
    permission_classes= [IsAuthenticated]


    def get_queryset(self):
        conversation_name = self.request.GET.get("conversation")
        queryset = (
            Message.objects.filter(
                conversation__name__contains=self.request.user.username,
            )
            .filter(conversation__name=conversation_name)
            .order_by("-timestamp")
        )
        return queryset



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    query = request.GET['q']
    users = UserProfile.objects.filter(username__icontains=query)

    serilizer = UserProfileSerializer(users, many=True)

    return Response(serilizer.data)
