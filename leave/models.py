from django.db import models
from django.conf import settings

class Leave(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('ANNUAL', 'Annual'),
        ('AUTHORIZED', 'Authorized Absence'),
        ('SICK', 'Sick'),
        ('PATERNITY', 'Paternity'),
        ('MATERNITY', 'Maternity'),
    ]

    LEAVE_STATUS_CHOICES = [
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('PENDING', 'Pending'),
    ]

    idleave = models.AutoField(primary_key=True)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    reason = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.IntegerField()
    status = models.CharField(max_length=20, choices=LEAVE_STATUS_CHOICES, default='PENDING')

    def save(self, *args, **kwargs):
        self.duration = (self.end_date - self.start_date).days + 1  # Calcul automatique de la durée
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.email} - {self.leave_type} ({self.status})"

