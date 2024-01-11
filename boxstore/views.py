from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Avg, Count
from django.utils import timezone
from .models import Box
from .serializers import BoxSerializer
from .permissions import IsStaffOrReadOnly, IsCreatorOrReadOnly
from .filters import BoxFilter

class BoxList(generics.ListCreateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [IsStaffOrReadOnly ]
    filterset_class = BoxFilter

   
    def perform_create(self, serializer):
        # Additional conditions before creating a new box
        # Check average area, average volume, and total boxes added in a week
        # Update these values based on A1, V1, L1, and L2 configurations
    

        # Check average area
        avg_area = Box.objects.all().aggregate(avg_area=Avg('area'))['avg_area'] or 0
        curr_area = self.request.data['length'] * self.request.data['breadth']
        if avg_area + curr_area > 100:
           return Response({"detail": "Average area exceeds the limit A1"}, status=status.HTTP_400_BAD_REQUEST)

        # Check average volume
        avg_volume = Box.objects.all().aggregate(avg_volume=Avg('volume'))['avg_volume'] or 0
        curr_vol = self.request.data['length'] * self.request.data['breadth']*self.request.data['height']
        if avg_volume + serializer.validated_data['volume'] > 1000:
            return Response({"detail": "Average volume exceeds the limit V1"}, status=status.HTTP_400_BAD_REQUEST)

        # Check total boxes added in a week
        week_start = timezone.now() - timezone.timedelta(days=7)
        total_boxes_in_week = Box.objects.filter(created_at__gte=week_start).count()
        if total_boxes_in_week >= 100:
            return Response({"detail": "Total boxes added in a week exceeds the limit L1"}, status=status.HTTP_400_BAD_REQUEST)

        # Check total boxes added in a week by a user
        user_total_boxes_in_week = Box.objects.filter(created_at__gte=week_start, created_by=self.request.user).count()
        if user_total_boxes_in_week >= 50:
            return Response({"detail": "Total boxes added by the user in a week exceeds the limit L2"}, status=status.HTTP_400_BAD_REQUEST)
        print(self.request)
        serializer.save(created_by=self.request.user, area = curr_area, volume = curr_vol)

class BoxDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [IsCreatorOrReadOnly]
    filterset_class = BoxFilter

    def perform_update(self, serializer):
        # Additional conditions before updating a box
        # Check if the box has been updated by a staff user
        if self.request.user.is_staff:
            serializer.save()
        else:
            # Non-staff users should not be able to update creator or creation date
            serializer.validated_data.pop('created_by', None)
            serializer.validated_data.pop('created_at', None)
            serializer.save()

class MyBoxList(generics.ListAPIView):
    serializer_class = BoxSerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_class = BoxFilter

    def get_queryset(self):
        return Box.objects.filter(created_by=self.request.user)

class BoxDelete(generics.DestroyAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [IsCreatorOrReadOnly]

    def perform_destroy(self, instance):
        # Check if the user is the creator of the box before deleting
        if self.request.user == instance.created_by:
            instance.delete()
        else:
            return Response({"detail": "You do not have permission to delete this box"}, status=status.HTTP_403_FORBIDDEN)
