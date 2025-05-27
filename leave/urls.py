from django.urls import path
from .views import (
    LeaveCreateView, LeaveListView, LeaveDetailView,
    LeaveUpdateView, LeaveDeleteView, LeaveTypeListView
)

urlpatterns = [
    path('create/', LeaveCreateView.as_view(), name='create_leave'),
    path('list/', LeaveListView.as_view(), name='list_leaves'),
    path('<int:pk>/', LeaveDetailView.as_view(), name='detail_leave'),
    path('<int:pk>/update/', LeaveUpdateView.as_view(), name='update_leave'),
    path('<int:pk>/delete/', LeaveDeleteView.as_view(), name='delete_leave'),
    path('leave/types/', LeaveTypeListView.as_view(), name='leave_types'),  # ← liste des types
]



# Méthode	URL	Action
# POST	/leave/create/	    Créer un congé
# GET  	/leave/list/	    Lister les congés
# GET	    /leave/<id>/	    Détails d’un congé
# PUT/PATCH	/leave/<id>/update/	  Modifier un congé
# DELETE	   /leave/<id>/delete/	  Supprimer un congé
# GET	      /leave/types/	          Liste des types de congé