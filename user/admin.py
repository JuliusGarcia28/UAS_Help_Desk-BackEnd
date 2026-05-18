from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department
from django.core.mail import send_mail
from django.conf import settings
from django.urls import path
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from .utils import token_generator


class TechnicianCreationForm(forms.ModelForm):
    """Form to create technician users without requiring department."""
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        labels = {
            'email': 'Correo electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con este correo')
        return email


class CustomUserCreationForm(forms.ModelForm):
    """Custom form for creating users that makes password optional for technicians."""
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "role", "status", "is_active")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            self.add_error('password_confirm', 'Las contraseñas no coinciden.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
        return user




@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "description",
        "status"
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "status",
    )

    ordering = ("name",)

    list_per_page = 20


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "department",
        "status",
        "is_staff"
    )

    list_filter = (
        "role",
        "status",
        "department",
        "is_staff"
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name"
    )

    ordering = ("username",)

    list_per_page = 20

    change_list_template = "admin/user_change_list.html"

    fieldsets = (

        ("Información de acceso", {
            "fields": ("username", "password")
        }),

        ("Información personal", {
            "fields": (
                "first_name",
                "last_name",
                "email"
            )
        }),

        ("Información organizacional", {
            "fields": (
                "role",
                "department",
                "status"
            )
        }),

        ("Permisos", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions"
            )
        }),

        ("Fechas importantes", {
            "fields": (
                "last_login",
                "date_joined"
            )
        }),

    )

    add_fieldsets = (

        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "email",
                "first_name",
                "last_name",
                "role",
                "status",
                "is_active",
                "password",
                "password_confirm"
            ),
        }),

    )

    def get_fieldsets(self, request, obj=None):
        """Override fieldsets to hide password field when editing."""
        if obj is None:
            # Creating new user
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """Use custom form for creating users."""
        if obj is None:
            # Creating new user - use custom form
            return CustomUserCreationForm
        
        # Editing existing user - use default form
        form = super().get_form(request, obj, **kwargs)
        
        # Restrict role choices to technician and client only
        if hasattr(form, 'base_fields') and 'role' in form.base_fields:
            form.base_fields['role'].choices = [
                ('technician', 'Technician'),
                ('client', 'Client'),
            ]
        
        return form

    def save_model(self, request, obj, form, change):
        """Auto-generate password for technicians and prevent admin creation."""
        # Prevent creating admin users
        if not change and obj.role == 'admin':
            from django.core.exceptions import ValidationError
            raise ValidationError('No se puede crear nuevos usuarios administradores.')
        
        # For new technician users, autogenerate password and set must_change_password
        if not change and obj.role == 'technician':
            pwd = User.objects.make_random_password()
            obj.set_password(pwd)
            obj.must_change_password = True
            obj.status = 1
            obj.is_active = True
            
            # Save the user first
            super().save_model(request, obj, form, change)
            
            # Send email with reset link
            try:
                from .utils import token_generator
                token = token_generator.make_token(obj)
                reset_url = f"http://localhost:4200/reset-password?uid={obj.id}&token={token}"
                send_mail(
                    'Cuenta de Técnico creada - Restablece tu contraseña',
                    f'Se ha creado tu cuenta de técnico. Usuario: {obj.email}\nPara establecer tu contraseña, usa este enlace:\n{reset_url}',
                    settings.EMAIL_HOST_USER,
                    [obj.email]
                )
            except Exception:
                pass
        else:
            super().save_model(request, obj, form, change)

    actions = ['make_technician']

    def make_technician(self, request, queryset):
        """Convert selected users into technicians, set temp password and email a secure reset link."""
        from .utils import token_generator

        for user in queryset:
            # set a random unusable password (we'll send reset link)
            pwd = User.objects.make_random_password()
            user.role = 'technician'
            user.set_password(pwd)
            user.must_change_password = True
            user.status = 1
            user.is_active = True
            user.save()

            # build secure reset link using token generator
            try:
                token = token_generator.make_token(user)
                reset_url = f"http://localhost:4200/reset-password?uid={user.id}&token={token}"

                send_mail(
                    'Cuenta de Técnico creada - Restablece tu contraseña',
                    f'Se ha creado tu cuenta de técnico. Usuario: {user.email}\nPara establecer tu contraseña, usa este enlace:\n{reset_url}\nEste enlace expira según la configuración del sistema.',
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )
            except Exception:
                # ignore email errors in admin action
                pass

    make_technician.short_description = 'Convertir usuarios seleccionados en técnicos (autogenera contraseña)'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('create-technician/', self.admin_site.admin_view(self.create_technician_view), name='user_create_technician'),
        ]
        return my_urls + urls

    def create_technician_view(self, request):
        from .utils import token_generator

        if request.method == 'POST':
            email = request.POST.get('email', '').strip().lower()
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            dept = request.POST.get('department') or None

            if not email:
                messages.error(request, 'El correo es requerido')
            elif User.objects.filter(email__iexact=email).exists():
                messages.error(request, 'Ya existe una cuenta con ese correo')
            else:
                # create user
                user = User(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    role='technician',
                    status=1,
                    is_active=True
                )
                if dept:
                    try:
                        user.department = Department.objects.get(id=dept)
                    except Department.DoesNotExist:
                        pass

                pwd = User.objects.make_random_password()
                user.set_password(pwd)
                user.must_change_password = True
                user.save()

                # send secure reset link
                try:
                    token = token_generator.make_token(user)
                    reset_url = f"http://localhost:4200/reset-password?uid={user.id}&token={token}"
                    send_mail(
                        'Cuenta de Técnico creada - Restablece tu contraseña',
                        f'Se ha creado tu cuenta de técnico. Usuario: {user.email}\nPara establecer tu contraseña, usa este enlace:\n{reset_url}',
                        settings.EMAIL_HOST_USER,
                        [user.email]
                    )
                except Exception:
                    # ignore email send errors
                    pass

                messages.success(request, f'Técnico creado: {email}')
                return redirect('admin:user_user_changelist')

        context = dict(
            self.admin_site.each_context(request),
            departments=Department.objects.filter(status=1),
        )

        return TemplateResponse(request, 'admin/user_create_technician.html', context)