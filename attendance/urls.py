from django.urls import path
from .views import (
    register_employee,
    verify_attendance,
    department_list_create,
    department_detail,
    employee_list,        
    employee_detail              
)

urlpatterns = [
    # Enregistrement Employees avec reconnaissance faciale
    path("register/", register_employee, name="register_employee"),
    
    # Vérification de présence
    path("verify/", verify_attendance, name="verify_attendance"),

    # Endpoints employés
    path("employees/", employee_list, name="employee_list"),              # GET all
    path("employee/<int:pk>/", employee_detail, name="employee_detail"),   # GET, PUT, DELETE

    # Endpoints départements
    path("departments/", department_list_create, name="department_list_create"), # GET all
    path("department/<int:pk>/", department_detail, name="department_detail"), # GET, PUT, DELETE
]


# Enregistrement d'un employé : POST http://127.0.0.1:8000/api/register/
# Vérification de présence : POST http://127.0.0.1:8000/api/verify/

# env\Scripts\Activate
# cd attendance_system 
# python manage.py runserver

# Méthode | URL | Description
# POST | /register/ | Enregistrement d’un employé avec image
# POST | /verify/ | Vérification de présence par reconnaissance
# GET | /employees/ | Liste de tous les employés
# GET | /employees/<id>/ | Détails d’un employé
# PUT | /employees/<id>/ | Mise à jour d’un employé
# DELETE | /employees/<id>/ | Suppression d’un employé
# GET | /departments/ | Liste des départements
# POST | /departments/ | Création d’un nouveau département
# GET | /departments/<id>/ | Détail d’un département
# PUT | /departments/<id>/ | Mise à jour d’un département
# DELETE | /departments/<id>/ | Suppression d’un département


# Maintenant, teste ces URLs :
# curl -X POST http://127.0.0.1:8000/api/register/ 
# {
#   "name": "John Doe",
#   "immatricule": "12345",
#   "poste": "Manager",
#   "department_name": "informatique",
#   "department_id": 1,
#   "email": "john@example.com",
#   "phone_number": "+1234567890",
#   "date_of_hire": "2025-04-01"
# }


# departement
# {
#   "name": "informatique",
#   "description": "Département IT"
# }

