import os
import tempfile
import logging
import numpy as np
import cv2
import dateutil.parser

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Employee, Department, Attendance
from .utils import extract_face_encoding, verify_identity
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

logger = logging.getLogger(__name__)

@swagger_auto_schema(
    method="post",
    manual_parameters=[ 
        openapi.Parameter("name", openapi.IN_FORM, description="Nom", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter("immatricule", openapi.IN_FORM, description="Matricule", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter("poste", openapi.IN_FORM, description="Poste", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter("department_name", openapi.IN_FORM, description="Nom du département", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter("phone_number", openapi.IN_FORM, description="Téléphone", type=openapi.TYPE_STRING, required=False),
        openapi.Parameter("image", openapi.IN_FORM, description="Image", type=openapi.TYPE_FILE, required=True),
        openapi.Parameter("date_of_hire", openapi.IN_FORM, description="Date d'embauche", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, required=False),
    ],
    responses={201: "Employé enregistré", 400: "Erreur"},
)
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def register_employee(request):
    name = request.data.get("name")
    immatricule = request.data.get("immatricule")
    poste = request.data.get("poste", "Inconnu")
    department_name = request.data.get("department_name")
    phone_number = request.data.get("phone_number")
    image = request.FILES.get("image")
    date_of_hire = request.data.get("date_of_hire")

    if not name or not immatricule or not image:
        return Response({"error": "Champs requis manquants."}, status=400)

    temp_file_path = None

    try:
        if image.content_type not in ['image/jpeg', 'image/png']:
            return Response({"error": "Format image non supporté. Utilisez .jpeg, .jpg ou .png."}, status=400)

        with tempfile.NamedTemporaryFile(delete=False, dir=UPLOAD_DIR, suffix=".jpg") as temp_file:
            for chunk in image.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        encoding = extract_face_encoding(temp_file_path)
        if encoding is None:
            return Response({"error": "Visage non détecté."}, status=400)

        department = None
        if department_name:
            try:
                department = Department.objects.get(name=department_name)
            except Department.DoesNotExist:
                return Response({"error": f"Département avec le nom '{department_name}' introuvable."}, status=400)

        if date_of_hire:
            date_of_hire = dateutil.parser.parse(date_of_hire).date()

        Employee.objects.create(
            name=name,
            immatricule=immatricule,
            poste=poste,
            department=department,
            phone_number=phone_number,
            face_encoding=encoding.tolist(),
            date_of_hire=date_of_hire,
        )

        return Response({"message": f"Employé {name} enregistré."}, status=201)

    except Exception as e:
        logger.error(f"Erreur enregistrement : {e}")
        return Response({"error": "Erreur serveur."}, status=500)

    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@swagger_auto_schema(
    method="post",
    manual_parameters=[openapi.Parameter("image", openapi.IN_FORM, description="Image", type=openapi.TYPE_FILE, required=True)],
    responses={200: "Présence validée", 400: "Erreur"},
)
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def verify_attendance(request):
    image = request.FILES.get("image")
    if not image:
        return Response({"error": "Image requise."}, status=400)

    if image.content_type not in ['image/jpeg', 'image/png']:
        return Response({"error": "Format image non supporté."}, status=400)

    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, dir=UPLOAD_DIR, suffix=".jpg") as temp_file:
            for chunk in image.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        img = cv2.imread(temp_file_path)
        if img is None:
            return Response({"error": "Image corrompue ou illisible."}, status=400)

        encoding = extract_face_encoding(temp_file_path)
        if encoding is None:
            return Response({"error": "Visage non détecté."}, status=400)

        for employee in Employee.objects.all():
            try:
                stored_encoding = np.array(employee.face_encoding, dtype=np.float32)
                is_match, similarity = verify_identity(encoding, stored_encoding, threshold=0.6)
                if is_match:
                    Attendance.objects.create(employee=employee)
                    return Response({"message": f"Présence validée pour {employee.name} (similarité: {similarity:.2f})"}, status=200)
            except Exception as e:
                logger.warning(f"Comparaison erreur : {e}")

        return Response({"error": "Aucune correspondance."}, status=400)
    except Exception as e:
        logger.error(f"Erreur vérification : {e}")
        return Response({"error": "Erreur traitement."}, status=500)
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@api_view(["GET"])
def employee_list(request):
    """
    Récupère tous les employés avec leurs départements
    """
    try:
        employees = Employee.objects.all()
        data = []
        for employee in employees:
            data.append({
                "idemployee": employee.idemployee,  # Utilisation de idemployee comme identifiant
                "name": employee.name,
                "immatricule": employee.immatricule,
                "poste": employee.poste,
                "phone_number": employee.phone_number,
                "date_of_hire": employee.date_of_hire,
                "department": employee.department.name if employee.department else None,
                "is_active": employee.is_active,
            })
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des employés: {str(e)}")
        return Response({"error": "Erreur serveur lors de la récupération des employés."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET", "PUT", "DELETE"])
def employee_detail(request, pk):
    try:
        employee = Employee.objects.get(idemployee=pk)  # Utilisation de idemployee
    except Employee.DoesNotExist:
        return Response({"error": "Employé non trouvé"}, status=404)

    if request.method == "GET":
        return Response({
            "idemployee": employee.idemployee,  # Utilisation de idemployee
            "name": employee.name,
            "immatricule": employee.immatricule,
            "poste": employee.poste,
            "department": employee.department.name if employee.department else None,
            "phone_number": employee.phone_number,
            "date_of_hire": employee.date_of_hire,
            "is_active": employee.is_active,
        })

    elif request.method == "PUT":
        data = request.data
        
        # Mettre à jour les champs de l'employé, tout en respectant les valeurs nulles
        employee.name = data.get("name", employee.name)
        employee.immatricule = data.get("immatricule", employee.immatricule)
        employee.poste = data.get("poste", employee.poste)
        employee.phone_number = data.get("phone_number", employee.phone_number)
        employee.is_active = data.get("is_active", employee.is_active)

        # Mise à jour du département si présent, ou laisser comme null
        department_name = data.get("department")
        if department_name:
            try:
                dept = Department.objects.get(name=department_name)
                employee.department = dept
            except Department.DoesNotExist:
                return Response({"error": f"Département '{department_name}' introuvable"}, status=400)
        else:
            employee.department = None  # Si aucun département n'est fourni, on met à null

        # Mise à jour de la date d'embauche si présente, ou laisser comme null
        date_of_hire = data.get("date_of_hire")
        if date_of_hire:
            employee.date_of_hire = dateutil.parser.parse(date_of_hire).date()
        else:
            employee.date_of_hire = None  # Si aucune date d'embauche n'est fournie, on met à null

        employee.save()
        return Response({"message": "Employé mis à jour"}, status=200)

    elif request.method == "DELETE":
        employee.delete()
        return Response({"message": "Employé supprimé"}, status=204)



@api_view(["GET", "POST"])
def department_list_create(request):
    if request.method == "GET":
        departments = Department.objects.all().values("id", "name", "description")
        return Response(list(departments), status=200)
    elif request.method == "POST":
        name = request.data.get("name")
        description = request.data.get("description", "")
        if not name:
            return Response({"error": "Nom requis"}, status=400)
        dept = Department.objects.create(name=name, description=description)
        return Response({"id": dept.id, "name": dept.name}, status=201)


@api_view(["GET", "PUT", "DELETE"])
def department_detail(request, pk):
    try:
        department = Department.objects.get(pk=pk)
    except Department.DoesNotExist:
        return Response({"error": "Département non trouvé"}, status=404)

    if request.method == "GET":
        department_data = {
            "id": department.id,
            "name": department.name,
            "description": department.description
        }
        return Response(department_data)
    elif request.method == "PUT":
        name = request.data.get("name", department.name)
        description = request.data.get("description", department.description)
        department.name = name
        department.description = description
        department.save()
        return Response({"id": department.id, "name": department.name}, status=200)
    elif request.method == "DELETE":
        department.delete()
        return Response({"message": "Département supprimé"}, status=204)
