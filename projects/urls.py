from django.urls import path, include
from . import views


urlpatterns = [
    path('project-list/', views.projectList, name='project-list'),
    path('project-detail/<str:project_pk>', views.projectDetail, name='project-detail'),
    path('project-create/', views.projectCreate, name='project-create'),
    path('project-updates/<str:project_pk>', views.projectUpdate, name='project-updates'),
    path('project-delete/<str:project_pk>', views.projectDelete, name='project-delete'),

    # Contributor
    path('project/<int:project_pk>/users/', views.contributorList),
    path('project/<int:project_pk>/users/<int:contributor_pk>/', views.contributorDetail),

    # Issue
    path('project/<int:project_pk>/issues/', views.issueList),
    path('project/<int:project_pk>/create-issues/', views.createIssue),
    path('project/<int:project_pk>/issues/<int:issue_pk>/', views.issueDetail),

    # comment
    path('project/<int:project_pk>/issues/<int:issue_pk>/comments/', views.commentView),
]   

