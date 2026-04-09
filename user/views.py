from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .models import User, Department
from .utils import token_generator

from .serializers import LoginSerializer, UserSerializer, DepartmentSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.validated_data["user"]

            refresh = RefreshToken.for_user(user)

            return Response({
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response(
                    {"error": "Refresh token requerido"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logout exitoso"},
                status=status.HTTP_200_OK
            )

        except Exception:
            return Response(
                {"error": "Token inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

class RequestPasswordReset(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"message": "Si el correo existe, recibirás instrucciones"})

        token = token_generator.make_token(user)

        reset_url = f"http://localhost:4200/reset-password?uid={user.id}&token={token}"

        send_mail(
            "Recuperación de contraseña",
            f"Usa este enlace para cambiar tu contraseña:\n{reset_url}",
            settings.EMAIL_HOST_USER,
            [email]
        )

        return Response({"message": "Correo enviado"})
    
class ResetPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        password = request.data.get("password")

        user = User.objects.filter(id=uid).first()

        if not user:
            return Response({"error": "Usuario inválido"}, status=400)

        if not token_generator.check_token(user, token):
            return Response({"error": "Token inválido"}, status=400)

        user.set_password(password)
        user.save()

        return Response({"message": "Contraseña actualizada"})

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]