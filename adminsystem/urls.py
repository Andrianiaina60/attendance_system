from django.urls import path
from .views import (
    AdminSystemCreateView, AdminSystemListView, AdminSystemDetailView,
    AdminSystemUpdateView, AdminSystemDeleteView
)

urlpatterns = [
    path('create/', AdminSystemCreateView.as_view(), name='create_admin'),
    path('list/', AdminSystemListView.as_view(), name='list_admins'),
    path('<int:pk>/', AdminSystemDetailView.as_view(), name='detail_admin'),
    path('<int:pk>/update/', AdminSystemUpdateView.as_view(), name='update_admin'),
    path('<int:pk>/delete/', AdminSystemDeleteView.as_view(), name='delete_admin'),
]



#  Test API : 
# POST /adminsystem/create/ : Créer un nouvel admin

# GET /adminsystem/list/ : Liste tous les admins

# GET /adminsystem/3/ : Détail admin avec ID 3

# PUT /adminsystem/3/update/ : Modifier un admin

# DELETE /adminsystem/3/delete/ : Supprimer un admin