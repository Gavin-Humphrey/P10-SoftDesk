from django.urls import path
from . import views


urlpatterns = [
    path("", views.ProjectListView.as_view()),
    path("<str:project_pk>/", views.ProjectDetailView.as_view()),
    # Contributor
    path("<int:project_pk>/users/", views.ContributorListView.as_view()),
    path(
        "<int:project_pk>/users/<int:contributor_pk>/",
        views.ContributorDetailView.as_view(),
    ),
    # Issue
    path("<int:project_pk>/issues/", views.IssueListView.as_view()),
    path("<int:project_pk>/issues/<int:issue_pk>/", views.IssueDetailView.as_view()),
    # comment
    path(
        "<int:project_pk>/issues/<int:issue_pk>/comments/<int:comment_pk>/",
        views.CommentDetailView.as_view(),
    ),
    path(
        "<int:project_pk>/issues/<int:issue_pk>/comments/",
        views.CommentListView.as_view(),
    ),
]
