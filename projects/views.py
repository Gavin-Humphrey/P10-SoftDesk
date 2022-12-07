from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)
from .models import Issue, Project, Contributor, Comment
from rest_framework.permissions import IsAuthenticated
from .permissions import (
    ProjectPermissions,
    ContributorPermissions,
    IssuePermissions,
    CommentPermissions,
)


class ProjectListView(APIView):
    permission_classes = (IsAuthenticated, ProjectPermissions)

    def get(self, request, *args, **kwargs):
        projects = Project.objects.filter(contributors__user=request.user)
        
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data["author"] = request.user.id
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            Contributor.objects.create(
                user=request.user, project=project, role="AUTHOR"
            )
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    permission_classes = (IsAuthenticated, ProjectPermissions)

    def get_object(self, request, project_pk):  #
        try:
            return Project.objects.get(id=project_pk)
        except Project.DoesNotExist:
            return None

    def get(self, request, project_pk, *args, **kwargs):
        project = get_object_or_404(Project, id=project_pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, project_pk, *args, **kwargs):
        project = get_object_or_404(Project, id=project_pk)

        data = request.data.copy()
        data["author"] = project.author.id
        serializer = ProjectSerializer(project, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_pk, *args, **kwargs):
        project = get_object_or_404(Project, id=project_pk)
        project.delete()
        return Response(
            project.title + " successfully delete!", status=status.HTTP_204_NO_CONTENT
        )


class ContributorListView(APIView):
    permission_classes = (IsAuthenticated, ContributorPermissions)

    def get(self, request, project_pk, *args, **kwargs):
        project = get_object_or_404(Project, id=project_pk)
        contributors = Contributor.objects.filter(project=project)
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_pk, *args, **kwargs):
        project = get_object_or_404(Project, id=project_pk)
        data = request.data.copy()
        data["project"] = project.id

        try:
            Contributor.objects.get(user=data["user"], project=project.id)
            return Response(
                "This user has already been added.", status=status.HTTP_400_BAD_REQUEST
            )
        except Contributor.DoesNotExist:
            try:
                User.objects.get(id=data["user"])
                serializer = ContributorSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except User.DoesNotExist:
                return Response(
                    "This user does not exist.", status=status.HTTP_400_BAD_REQUEST
                )


class ContributorDetailView(APIView):
    permission_classes = (IsAuthenticated, ContributorPermissions)

    def delete(self, request, project_pk, contributor_pk, *args, **kwargs):
        get_object_or_404(Project, id=project_pk)
        contributor = get_object_or_404(Contributor, id=contributor_pk)

        if contributor.role == "AUTHOR":
            return Response(
                "Project author cannot be deleted.", status=status.HTTP_400_BAD_REQUEST
            )
        else:
            contributor.delete()
            return Response(
                "Contributor successfully deleted.", status=status.HTTP_204_NO_CONTENT
            )


class IssueListView(APIView):
    permission_classes = (IsAuthenticated, IssuePermissions)

    def get(self, request, project_pk, *args, **kwargs):
        project = get_object_or_404(Project, id=project_pk)
        issues = Issue.objects.filter(project=project)  #
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_pk, *args, **kwargs):
        project = get_object_or_404(Project, id=project_pk)
        data = request.data.copy()
        data["project"] = project.id
        data["author"] = request.user.id
        serializer = IssueSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueDetailView(APIView):
    permission_classes = (IsAuthenticated, IssuePermissions)

    def get_object(self, request, issue_pk):  
        try:
            return Issue.objects.get(id=issue_pk)
        except Issue.DoesNotExist:
            return None

    def put(self, request, project_pk, issue_pk, *args, **kwargs):
        project = get_object_or_404(Project, id=project_pk)
        issue = get_object_or_404(Issue, id=issue_pk)
        data = request.data.copy()
        data["project"] = project.id
        data["author"] = issue.author.id
        try:
            serializer = IssueSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Contributor.DoesNotExist:
            return Response(
                "This user is not a contributor to this project or does not exist.",
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, issue_pk, *args, **kwargs):
        issue = get_object_or_404(Issue, id=issue_pk)
        issue.delete()
        return Response(
            "Issue successfully deleted.", status=status.HTTP_204_NO_CONTENT
        )


class CommentListView(APIView):
    permission_classes = (IsAuthenticated, CommentPermissions)

    def get(self, request, project_pk, issue_pk, *args, **kwargs):
        get_object_or_404(Project, id=project_pk)
        issue = get_object_or_404(Issue, id=issue_pk)
        comments = Comment.objects.filter(issue=issue)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, issue_pk, *args, **kwargs):
        issue = get_object_or_404(Issue, id=issue_pk)
        data = request.data.copy()
        data["issue"] = issue.id
        data["author"] = request.user.id

        serializer = CommentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    permission_classes = (IsAuthenticated, CommentPermissions)

    def get(self, request, project_pk, comment_pk, *args, **kwargs):
        get_object_or_404(Project, id=project_pk)
        comment = get_object_or_404(Comment, id=comment_pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, issue_pk, comment_pk, *args, **kwargs):
        issue = get_object_or_404(Issue, id=issue_pk)
        comment = get_object_or_404(Comment, id=comment_pk)
        data = request.data.copy()
        data["issue"] = issue.id
        data["author"] = comment.author.id

        serializer = CommentSerializer(comment, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, comment_pk, *args, **kwargs):
        comment = get_object_or_404(Comment, id=comment_pk)
        comment.delete()
        return Response(
            "Comment, successfully deleted.", status=status.HTTP_204_NO_CONTENT
        )
