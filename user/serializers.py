from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import AuditLog, User, Department

from .email_service import send_activation_email
from django.conf import settings
from .utils import token_generator


class DepartmentSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Department
        fields = ["id", "name", "description", "status", "parent"]
        
    def validate_parent(self, value):

      if not self.instance:
        return value

      if value == self.instance:

        raise serializers.ValidationError(
            "Un departamento no puede depender de sí mismo"
        )

      parent = value

      while parent:

        if parent == self.instance:

            raise serializers.ValidationError(
                "Dependencia circular detectada"
            )

        parent = parent.parent

      return value


class UserSerializer(serializers.ModelSerializer):
    # Mostrar Objeto completo
    department = DepartmentSerializer(read_only=True)
    
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source='department',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "status",
            "email_verified",
            "department",
            "department_id"
        ]

        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True}
        }

    def create(self, validated_data):

      validated_data.pop("password", None)

      user = User(**validated_data)

      user.status = 0
      user.email_verified = False

      user.set_unusable_password()

      user.save()

      token = token_generator.make_token(user)

      activation_url = (
        f"{settings.FRONTEND_URL}/activate-account"
        f"?uid={user.id}&token={token}"
      )
      
      try:
        send_activation_email(
          user=user,
          activation_url=activation_url
        )
      except Exception as e:
       print("====================================")
       print("ERROR ENVIANDO CORREO")
       print("TIPO:", type(e).__name__)
       print("ERROR:", str(e))
       print("====================================")

       user.delete()

       raise serializers.ValidationError(
        "Error al enviar el correo de activación"
       )
      
      AuditLog.objects.create(
        user=user,
        action="create",
        description="Usuario creado"
      )

      return user
    
    def update(self, instance, validated_data):

      request = self.context.get("request")

      if request:

        if (
            request.user.role != "admin"
            and "role" in validated_data
        ):
            validated_data.pop("role")

      return super().update(
        instance,
        validated_data
      )
    
    def validate_email(self, value):

        qs = User.objects.filter(email__iexact=value)

        if self.instance:
          qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
          raise serializers.ValidationError(
            "Ya existe un usuario con este correo"
          )
          
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

      email = data.get("email", "").strip().lower()

      password = data.get("password")

      try:

        user = User.objects.get(
            email__iexact=email
        )

      except User.DoesNotExist:

        raise serializers.ValidationError(
            "Credenciales inválidas"
        )

      user = authenticate(
        username=user.username,
        password=password
      )

      if not user:

        raise serializers.ValidationError(
            "Credenciales inválidas"
        )

      if not user.email_verified:

        raise serializers.ValidationError(
            "Debes activar tu cuenta"
        )

      if user.status != 1:

        raise serializers.ValidationError(
            "Usuario inactivo"
        )

      data["user"] = user
      
      AuditLog.objects.create(
        user=user,
        action="login",
        description="Inicio de sesión"
      )

      return data
      
class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)