# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
# from .models import Leave
# from .serializers import LeaveSerializer

# class LeaveCreateView(generics.CreateAPIView):
#     queryset = Leave.objects.all()
#     serializer_class = LeaveSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         # Assigner l'utilisateur connecté à l'employé
#         serializer.save(employee=self.request.user)
