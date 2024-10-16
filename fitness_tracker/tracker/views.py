from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Activity
from .serializers import ActivitySerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated] # Ensure only authenticated users can access this view
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        # Users can only view their own activities
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the current user to the activity being created
        serializer.save(user=self.request.user)
    def update(self, request, *args, **kwargs):
        # Get the instance of the activity to update
        instance = self.get_object()
        
        # Deserialize the data to check for validity
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        
        # Perform the update
        self.perform_update(serializer)
        
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

# UserViewSet to handle User CRUD operations
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        # Restrict access to the authenticated user's data only
        return User.objects.filter(id=self.request.user.id)

