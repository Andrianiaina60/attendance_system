from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from attendance.models import Employee  # Assure-toi que ce chemin est correct

class AuthenticationManager(BaseUserManager):
    def create_user(self, email, password=None, role='employee', status=True, employee=None, **extra_fields):
        if not email:
            raise ValueError("L'utilisateur doit avoir un email")
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, status=status, employee=employee, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, role='admin', status=True, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Authentication(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employé'),
    )

    email = models.EmailField(unique=True, max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    status = models.BooleanField(default=True)  # actif ou non

    idemployee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)  
    # relation vers Employee, null possible

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Pour admin Django

    objects = AuthenticationManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
















# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from attendance.models import Employee  # Assure-toi que ce chemin est correct

# class AuthenticationManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("L'email est requis.")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)  # hash du mot de passe
#         user.save()
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         return self.create_user(email, password, **extra_fields)

# class Authentication(AbstractBaseUser, PermissionsMixin):
#     ROLE_CHOICES = (
#         ('admin', 'Administrateur'),
#         ('employee', 'Employé'),
#         ('manager', 'Manager'),
#     )

#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
#     status = models.BooleanField(default=True)

#     idemployee = models.OneToOneField(
#         Employee,
#         on_delete=models.CASCADE,
#         related_name='auth',
#         null=True,
#         blank=True,
#         default=None
#     )

#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['role']

#     objects = AuthenticationManager()

#     def __str__(self):
#         return f"{self.email} - {self.role}"
