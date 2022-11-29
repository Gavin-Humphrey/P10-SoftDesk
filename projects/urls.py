from django.urls import path, include
from . import views


urlpatterns = [
    path('project-list/', views.projectList, name='project-list'),
    path('project-detail/<str:pk>', views.projectDetail, name='project-detail'),
    path('project-create/', views.projectCreate, name='project-create'),
    path('project-updates/<str:pk>', views.projectUpdate, name='project-updates'),
    path('project-delete/<str:pk>', views.projectDelete, name='project-delete'),

    path('project/<int:project_pk>/users/', views.contributor_list),
    path('project/<int:project_pk>/users/<int:contributor_pk>/', views.contributor_detail),
]   

