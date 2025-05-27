from django.db import models

class AdminSystem(models.Model):
    idadmin = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.nom

