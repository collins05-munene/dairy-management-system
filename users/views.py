from django.contrib.auth.hashers import check_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status

from .models import Farmer, Collector, Clerk, Admin, UserToken
from .serializers import FarmerSerializer, CollectorSerializer, ClerkSerializer, AdminSerializer, LoginSerializer

# Create your views here.
USER_REGISTRY = {
    'farmer': (Farmer, FarmerSerializer),
    'collector': (Collector, CollectorSerializer),
    'clerk': (Clerk, ClerkSerializer),
    'admin': (Admin, AdminSerializer)    
}


def get_authenticated_user(request):
    auth_header = request.headers.get("Authorization", '')
    if not auth_header.startswith('Token'):
        return None, None
    token_key = auth_header.split(' ')[1]

    try:
        token = UserToken.objects.get(token=token_key)
        model, _ = USER_REGISTRY[token.user_type]
        user = model.objects.get(id=token.user_id)
        return token.user_type, user
    
    except (UserToken.DoesNotExist, KeyError):
        return None, None
    

class AuthRequiredMixin:
    def get_auth(self, request):
        user_type, user = get_authenticated_user(request)
        if not user:
            return None, None, Response(
                {'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED
            )
        return user_type, user, None
    

class RegisterView(APIView):
    def post(self, request, user_type):
        entry = USER_REGISTRY.get(user_type)
        if not entry:
            return Response({"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)
        
        _, serializer_class = entry

        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = UserToken.objects.create(
                token=UserToken.generate_token(),
                user_type = user_type,
                user_id = user.id
            )
            return Response(
                {"token": token.token, "user": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        phone = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']
        user_type = serializer.validated_data['user_type']

        model, serializer_class = USER_REGISTRY[user_type]

        try:
            user = model.objects.get(phone_number=phone)
        except model.DoesNotExist:
            return Response({'error': "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not check_password(password, user.password):
            return Response({"error": "Invalid  credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        UserToken.objects.filter(user_type=user_type, user_id=user.id).delete()
        token = UserToken.objects.create(
            token=UserToken.generate_token(),
            user_type=user_type,
            user_id=user.id
        )
        return Response({"token": token.token, "user": serializer_class(user).data})
    

class LogoutView(AuthRequiredMixin, APIView):
    def post(self, request):
        _, _, err = self.get_auth(request)
        if err:
            return err
        auth_header = request.headers.get('Authorization', '')
        token_key = auth_header.split(' ')[1]
        UserToken.objects.filter(token=token_key).delete()
        return Response({'message': "Logged out successfully"})
    

class BaseListView(AuthRequiredMixin, APIView):
    model = None
    serializer_class = None
    
    def get(self, request):
        _, _, err = self.get_auth(request)
        if err:
            return err
        serializer = self.serializer_class(self.model.objects.all(), many=True)
        return Response(serializer.data)
    

    def post(self, request):
        _, _, err  = self.get_auth(request)
        if err:
            return err
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BaseDetailView(AuthRequiredMixin, APIView):
    model=None
    serializer_class=None

    def get_object(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            return None
        
    def get(self, request, pk):
        _, _, err = self.get_auth(request)
        if err:
            return err
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.serializer_class(obj).data)
    

    def put(self, request, pk):
        _, _, err = self.get_auth(request)
        if err:
            return err
        obj = self.get_object(pk)

        if not obj:
            return Response({'error': "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer =- self.serializer_class(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        _, _, err = self.get_auth(request)
        if err:
            return err
        obj = self.get_object(pk)
        if not obj:
            return Response({'error': "Not found"}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class FarmerListView(BaseListView):
    model, serializer_class = Farmer, FarmerSerializer

class FarmerDetailView(BaseDetailView):
    model, serializer_class = Farmer, FarmerSerializer

class CollectorListView(BaseListView):
    model, serializer_class = Collector, CollectorSerializer

class CollectorDetailView(BaseDetailView):
    model, serializer_class = Collector, CollectorSerializer

class ClerkListView(BaseListView):
    model, serializer_class = Clerk, ClerkSerializer

class ClerkDetailView(BaseDetailView):
    model, serializer_class = Clerk, ClerkSerializer

class AdminListView(BaseListView):
    model, serializer_class = Admin, AdminSerializer

class AdminDetailView(BaseDetailView):
    model, serializer_class = Admin, AdminSerializer