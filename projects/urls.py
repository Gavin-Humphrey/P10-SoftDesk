from django.urls import path
from . import views


urlpatterns = [
    path('', views.projectList, name='project-list'),
    path('<str:project_pk>', views.projectDetail, name='project-detail'),
    path('', views.projectCreate, name='project-create'),
    path('<str:project_pk>', views.projectUpdate, name='project-updates'),
    path('<str:project_pk>', views.projectDelete, name='project-delete'),

    # Contributor
    path('<int:project_pk>/users/', views.contributorList),
    path('<int:project_pk>/users/<int:contributor_pk>/', views.contributorDetail),

    # Issue
    path('<int:project_pk>/issues/', views.issueList),
    path('<int:project_pk>/create-issues/', views.createIssue),
    path('<int:project_pk>/issues/<int:issue_pk>/', views.issueDetail),

    # comment
    path('<int:project_pk>/issues/<int:issue_pk>/comments/<int:comment_pk>/', views.commentView),
]   

