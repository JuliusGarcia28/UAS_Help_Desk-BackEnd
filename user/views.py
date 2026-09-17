from rest_framework.views import APIView, PermissionDenied
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.password_validation import validate_password
from django.conf import settings

from .models import User, Department
from .utils import token_generator
from .permissions import IsAdmin
from .email_service import send_password_reset_email
from .serializers import (
LoginSerializer,
UserSerializer,
DepartmentSerializer,
ChangePasswordSerializer
)
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        response = Response({
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
        })

        response.set_cookie(
            key=settings.REFRESH_COOKIE_NAME,
            value=str(refresh),
            max_age=7 * 24 * 60 * 60,
            httponly=settings.REFRESH_COOKIE_HTTPONLY,
            secure=settings.REFRESH_COOKIE_SECURE,
            samesite=settings.REFRESH_COOKIE_SAMESITE,
            path="/auth/",
        )

        return response
    
class RefreshTokenView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        refresh_token = request.COOKIES.get(
            settings.REFRESH_COOKIE_NAME
        )

        if not refresh_token:
            return Response(
                {"error": "Sesión no válida"},
                status=401
            )

        try:

            refresh = RefreshToken(refresh_token)

            access_token = refresh.access_token

            response = Response({
                "access": str(access_token)
            })

            if settings.SIMPLE_JWT.get(
                "ROTATE_REFRESH_TOKENS"
            ):

                refresh.set_jti()
                refresh.set_exp()

                response.set_cookie(
                    key=settings.REFRESH_COOKIE_NAME,
                    value=str(refresh),
                    max_age=7 * 24 * 60 * 60,
                    httponly=True,
                    secure=settings.REFRESH_COOKIE_SECURE,
                    samesite=settings.REFRESH_COOKIE_SAMESITE,
                    path="/auth/",
                )

            return response

        except TokenError:

            response = Response(
                {"error": "Sesión expirada"},
                status=401
            )

            response.delete_cookie(
                settings.REFRESH_COOKIE_NAME,
                path="/auth/"
            )

            return response

class Logout(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        refresh_token = request.COOKIES.get(
            settings.REFRESH_COOKIE_NAME
        )

        response = Response({
            "message": "Logout exitoso"
        })

        if refresh_token:

            try:

                token = RefreshToken(
                    refresh_token
                )

                token.blacklist()

            except Exception:
                pass

        response.delete_cookie(
            settings.REFRESH_COOKIE_NAME,
            path="/auth/"
        )

        return response

class RequestPasswordReset(APIView):
  permission_classes = [AllowAny]


  def post(self, request):

    email = request.data.get("email")

    user = User.objects.filter(email=email).first()

    if not user:
        return Response({
            "message": "Si el correo existe, recibirás instrucciones"
        })

    token = token_generator.make_token(user)

    reset_url = (
        f"{settings.FRONTEND_URL}/reset-password"
        f"?uid={user.id}&token={token}"
    )

    send_password_reset_email(
        user=user,
        reset_url=reset_url
    )

    return Response({
        "message": "Correo enviado"
    })

class ActivateAccount(APIView):
  permission_classes = [AllowAny]

  def post(self, request):

    uid = request.data.get("uid")
    token = request.data.get("token")
    password = request.data.get("password")

    user = User.objects.filter(id=uid).first()

    if not user:
        return Response(
            {"error": "Usuario inválido"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not token_generator.check_token(user, token):
        return Response(
            {"error": "Token inválido"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        validate_password(password)

    except Exception as e:
        return Response(
            {"error": list(e.messages)},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.set_password(password)
    user.email_verified = True
    user.status = 1
    user.save()

    return Response({
        "message": "Cuenta activada correctamente"
    })

class ResetPassword(APIView):
  permission_classes = [AllowAny]


  def post(self, request):

    uid = request.data.get("uid")
    token = request.data.get("token")
    password = request.data.get("password")

    user = User.objects.filter(id=uid).first()

    if not user:
        return Response(
            {"error": "Usuario inválido"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not token_generator.check_token(user, token):
        return Response(
            {"error": "Token inválido"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        validate_password(password)

    except Exception as e:
        return Response(
            {"error": list(e.messages)},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.set_password(password)
    user.save()

    return Response({
        "message": "Contraseña actualizada"
    })
    
class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ChangePasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        current_password = serializer.validated_data[
            "current_password"
        ]

        new_password = serializer.validated_data[
            "new_password"
        ]

        user = request.user

        if not user.check_password(current_password):
            return Response(
                {
                    "error":
                    "La contraseña actual es incorrecta"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(new_password)

        except Exception as e:

            return Response(
                {
                    "error":
                    list(e.messages)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {
                "message":
                "Contraseña actualizada correctamente"
            }
        )

class UserView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):

    serializer = UserSerializer(request.user)

    return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def check_permissions(self, request):
        super().check_permissions(request)

        role = request.user.role

        if request.method == "GET":

            if role not in ["admin"]:
                raise PermissionDenied(
                    "No tienes permiso para consultar todos los usuarios."
                )
                
        elif request.method == "POST":

            if role not in ["admin"]:
                raise PermissionDenied(
                    "No tienes permiso para registrar usuarios."
                )
        
        elif request.method in ["PUT", "PATCH"]:

            if role not in ["admin"]:
                raise PermissionDenied(
                    "No tienes permiso para modificar usuarios."
                )
            
    # Prohibe la eliminación de usuarios a través de la API
    def destroy(self, request, *args, **kwargs):
            raise PermissionDenied(
                "La eliminación de usuarios no está permitida."
            )

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def check_permissions(self, request):
        super().check_permissions(request)

        role = request.user.role

        if request.method == "GET":

            if role not in ["admin"]:
                raise PermissionDenied(
                    "No tienes permiso para consultar los departamentos."
                )
                
        elif request.method == "POST":

            if role not in ["admin"]:
                raise PermissionDenied(
                    "No tienes permiso para registrar departamentos."
                )
        
        elif request.method in ["PUT", "PATCH"]:

            if role not in ["admin"]:
                raise PermissionDenied(
                    "No tienes permiso para modificar departamentos."
                )
                
    # Prohibe la eliminación de departamentos a través de la API
    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied(
            "La eliminación de departamentos no está permitida."
        )