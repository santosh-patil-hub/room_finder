from rest_framework import serializers
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Room
        exclude = ['owner', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            validated_data['owner'] = request.user
        return super().create(validated_data)


class OwnerDashboardSerializer(serializers.Serializer):
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    owned_rooms = serializers.SerializerMethodField()

    def get_owned_rooms(self, obj):
        rooms = Room.objects.filter(owner=obj)
        return RoomSerializer(rooms, many=True).data
    
class TenantDashboardSerializer(serializers.Serializer):
    tenant_name = serializers.CharField(source='username', read_only=True)
    available_rooms = serializers.SerializerMethodField()

    def get_available_rooms(self, obj):
        rooms = Room.objects.filter(available=True)  # you can add more filters here
        return RoomSerializer(rooms, many=True).data
