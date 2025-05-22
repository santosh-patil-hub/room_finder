from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from .models import Room
from .serializers import RoomSerializer

from .serializers import (
    OwnerDashboardSerializer,
    TenantDashboardSerializer,
)


class OwnerDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_type != 'owner':
            return Response({'detail': 'Unauthorized'}, status=403)
        serializer = OwnerDashboardSerializer(request.user)
        return Response(serializer.data)

class TenantDashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_type != 'tenant':
            return Response({'detail': 'Unauthorized'}, status=403)
        serializer = TenantDashboardSerializer(request.user)
        return Response(serializer.data)






# Create Room (only owner can create)
class RoomCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.user_type != 'owner':
            raise PermissionDenied("Only owners can create rooms.")

        serializer = RoomSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            room = serializer.save(owner=request.user)  # Ensure owner is set from request user
            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List all rooms (anyone can view)
class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all().order_by('-created_at')
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]


# Retrieve room detail (anyone can view)
class RoomDetailAPIView(generics.RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]


# Update room (only owner of room can update)
class RoomUpdateAPIView(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        room = self.get_object()
        if self.request.user != room.owner or self.request.user.user_type != 'owner':
            raise PermissionDenied("Only the room owner can update this room.")
        serializer.save()


# Delete room (only owner of room can delete)
class RoomDeleteAPIView(generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if self.request.user != instance.owner or self.request.user.user_type != 'owner':
            raise PermissionDenied("Only the room owner can delete this room.")
        instance.delete()
