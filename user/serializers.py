from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Department


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
        if self.instance and value == self.instance:
            raise serializers.ValidationError("Un departamento no puede depender de sí mismo")
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
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):

        email = data.get("email", "").strip().lower()
        password = data.get("password")

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Credenciales inválidas")

        if not user.check_password(password):
            raise serializers.ValidationError("Credenciales inválidas")

        if user.status != 1:
            raise serializers.ValidationError("Usuario inactivo")

        data["user"] = user
        return data