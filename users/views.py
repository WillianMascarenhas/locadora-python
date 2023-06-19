from rest_framework.views import APIView, Request, Response, status
from users.serializers import UserBusterSerializer, LoginSerializer
from users.models import User

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from users.permissions import IsUserOwner, IsEmployeeOrReadOnly
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication

from django.shortcuts import get_object_or_404



# São as 3 formas de se fazer login cada vez mais abstratas, para ver a mais comum e mais abstrata ir em em urls

class LoginBusterView(TokenObtainPairView):
    ...

class LoginBusterView2(APIView):
    def post(self, request:Request) -> Response:
        serializer = TokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(data=serializer.validated_data, status=status.HTTP_200_OK)

class LoginBusterView1(APIView):
    def post(self, request:Request) -> Response:
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if not user:
            return Response(data={"msg": "invalid credentials"}, status=status.HTTP_403_FORBIDDEN)
        
        refresh = RefreshToken.for_user(user)

        token_dict = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        return Response(data=token_dict, status=status.HTTP_200_OK)

class UserBusterView(APIView):
    def post(self, request:Request) -> Response:
        data = request.data
        serializer = UserBusterSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
class UserByIdView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsUserOwner, IsAuthenticated]

    def get(self, request:Request, user_id: int) -> Response:
        user = get_object_or_404(User, pk=user_id)
        self.check_object_permissions(request, user)

        serializer = UserBusterSerializer(instance=user)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request: Request, user_id:int) -> Response:
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)

        serializer = UserBusterSerializer(instance=user, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
 
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
