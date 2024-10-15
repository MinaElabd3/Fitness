from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Activity
from .serializers import ActivitySerializer, UserSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users can only view their own activities
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the current user to the activity being created
        serializer.save(user=self.request.user)

# UserViewSet to handle User CRUD operations
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Optional: Restrict access to the authenticated user's data only
        return User.objects.filter(id=self.request.user.id)
