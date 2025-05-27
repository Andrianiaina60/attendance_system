from rest_framework import generics
from .models import AdminSystem
from .serializers import AdminSystemSerializer

# CREATE
class AdminSystemCreateView(generics.CreateAPIView):
    queryset = AdminSystem.objects.all()
    serializer_class = AdminSystemSerializer

# READ (List + Retrieve)
class AdminSystemListView(generics.ListAPIView):
    queryset = AdminSystem.objects.all()
    serializer_class = AdminSystemSerializer

class AdminSystemDetailView(generics.RetrieveAPIView):
    queryset = AdminSystem.objects.all()
    serializer_class = AdminSystemSerializer

# UPDATE
class AdminSystemUpdateView(generics.UpdateAPIView):
    queryset = AdminSystem.objects.all()
    serializer_class = AdminSystemSerializer

# DELETE
class AdminSystemDeleteView(generics.DestroyAPIView):
    queryset = AdminSystem.objects.all()
    serializer_class = AdminSystemSerializer

