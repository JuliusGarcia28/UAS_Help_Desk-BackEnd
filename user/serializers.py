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

    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        min_length=6
    )

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name", 
            "role", "status", "is_active", "is_staff", "is_superuser",
            "department", "department_id", "last_login", "date_joined",
            "must_change_password", "password"
        ]
        read_only_fields = ["id", "last_login", "date_joined"]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        normalized_email = value.strip().lower()

        if User.objects.filter(email__iexact=normalized_email).exists():
            raise serializers.ValidationError('Ya existe una cuenta con este correo')

        return normalized_email

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']

        user = User(
            username=email,
            email=email,
            role='client',
            status=1
        )
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
        except User.MultipleObjectsReturned:
            raise serializers.ValidationError("Existe más de una cuenta con este correo")

        if not user.check_password(password):
            raise serializers.ValidationError("Credenciales inválidas")

        if user.status != 1:
            raise serializers.ValidationError("Usuario inactivo")

        data["user"] = user
        return data