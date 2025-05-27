from django.db import models
from django.core.validators import RegexValidator
import numpy as np

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Département"
        verbose_name_plural = "Départements"
        ordering = ['name']

    def __str__(self):
        return self.name

class Employee(models.Model):
    idemployee = models.AutoField(primary_key=True)
    immatricule = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255, db_index=True)
    face_encoding = models.JSONField(null=True, blank=True)
    poste = models.CharField(max_length=100, default="Inconnu")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_hire = models.DateField(null=True, blank=True)
    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Le numéro de téléphone doit être au format international."
        )]
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def set_face_encoding(self, encoding):
        if isinstance(encoding, np.ndarray):
            encoding = encoding.astype(np.float32).tolist()
        elif not isinstance(encoding, list):
            raise ValueError("L'encodage du visage doit être un tableau NumPy ou une liste.")
        if not encoding:
            raise ValueError("L'encodage du visage ne peut pas être vide.")
        self.face_encoding = encoding
        self.save()

    def get_face_encoding(self):
        if self.face_encoding:
            return np.array(self.face_encoding, dtype=np.float32)
        return np.array([], dtype=np.float32)

    def __str__(self):
        return f"{self.name} - {self.poste} - {self.department.name if self.department else 'Sans département'}"

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendances")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['employee', 'timestamp'])]
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.employee.name} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
