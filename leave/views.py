from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Leave
from .serializers import LeaveSerializer

# CRUD VIEWS
class LeaveCreateView(generics.CreateAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer

class LeaveListView(generics.ListAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer

class LeaveDetailView(generics.RetrieveAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer

class LeaveUpdateView(generics.UpdateAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer

class LeaveDeleteView(generics.DestroyAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer

# Custom API to get leave types
class LeaveTypeListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        leave_types = [{"key": k, "label": v} for k, v in Leave.LEAVE_TYPE_CHOICES]
        return Response(leave_types)
