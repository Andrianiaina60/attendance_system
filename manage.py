#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendance_system.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
admin_setup.py
# import django
# import os

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')  # Remplace par ton projet
# django.setup()

# from authentication.models import CustomUser
# from django.contrib.auth import authenticate

# email = 'ravintsoandraibeandrianiaina@gmail.com'
# user = CustomUser.objects.get(email=email)

# user.is_staff = True
# user.is_superuser = True
# user.is_active = True
# user.set_password('admin')
# user.save()

# authenticated_user = authenticate(email=email, password='admin')
# print("Authenticated user:", authenticated_user)
