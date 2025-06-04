# # models.py
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.hashers import make_password

# class Employee(AbstractUser):
#     ROLE_CHOICES = [
#         ('admin', 'Administrator'),
#         ('manager', 'Manager'),
#         ('employee', 'Employee'),
#         ('hr', 'Human Resources'),
#     ]
    
#     STATUS_CHOICES = [
#         ('active', 'Active'),
#         ('inactive', 'Inactive'),
#         ('suspended', 'Suspended'),
#     ]

#     employee_id = models.CharField(max_length=20, unique=True)
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     email = models.EmailField(unique=True)

#     # Utiliser email comme username
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['employee_id']

#     def __str__(self):
#         return f"{self.employee_id} - {self.email}"

#     def save(self, *args, **kwargs):
#         # Hash du mot de passe si nécessaire
#         if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
#             self.password = make_password(self.password)
#         super().save(*args, **kwargs)

#     class Meta:
#         # db_table = 'employees'
#         db_table = 'authentication'


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class Employee(AbstractUser):
    username = None  # Supprimer le champ hérité `username`

    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
        ('hr', 'Human Resources'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]

    employee_id = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    email = models.EmailField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Utiliser email comme identifiant
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['employee_id']  # champs requis à la création d'un superuser

    def __str__(self):
        return f"{self.employee_id} - {self.email}"

    def save(self, *args, **kwargs):
        # Hachage du mot de passe si non déjà haché
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'authentication'
