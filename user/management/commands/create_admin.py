from django.core.management.base import BaseCommand
from django.db import transaction

from user.models import User


class Command(BaseCommand):
    help = 'Create or update an admin user (sets is_staff/is_superuser and status=1).'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, required=True, help='Email del admin')
        parser.add_argument('--password', type=str, required=True, help='Password del admin')

    @transaction.atomic
    def handle(self, *args, **options):
        email = options.get('email').strip().lower()
        password = options.get('password')

        # Try to find existing user by email (case-insensitive)
        user = User.objects.filter(email__iexact=email).first()

        if user:
            user.username = email if not user.username else user.username
            user.email = email
            user.role = 'admin'
            user.status = 1
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Admin actualizado: {email}'))
        else:
            # Create new admin user
            user = User(
                username=email,
                email=email,
                role='admin',
                status=1,
                is_staff=True,
                is_superuser=True,
                is_active=True,
            )
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Admin creado: {email}'))
