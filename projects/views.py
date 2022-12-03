from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db import IntegrityError
from .serializers import (
    ProjectSerializer, 
    ContributorSerializer, 
    IssueSerializer, 
    CommentSerializer
    )
from .models import Issue, Project, Contributor, Comment
from rest_framework.permissions import IsAuthenticated
from .permissions import (
    ProjectPermissions,
    ContributorPermissions,
    IssuePermissions,
    CommentPermissions

    )



@api_view(['GET'])
@permission_classes([IsAuthenticated, ProjectPermissions])
def projectList(request):
    projects = Project.objects.filter(contributors__user=request.user)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated, ProjectPermissions])
def projectDetail(request, project_pk):
    projects = get_object_or_404(Project, id=project_pk)
    serializer = ProjectSerializer(projects, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated, ProjectPermissions])
def projectCreate(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        project = serializer.save()
        Contributor.objects.create(user=request.user, project=project, role='AUTHOR')
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, ProjectPermissions])
def projectUpdate(request, project_pk):
    project = get_object_or_404(Project, id=project_pk)
    serializer = ProjectSerializer(instance=project, data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, ProjectPermissions])
def projectDelete(request, project_pk):
    project = get_object_or_404(Project, id=project_pk)
    project.delete()
    return Response(project.title + " successfully delete!", status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, ProjectPermissions])
def contributorList(request, project_pk):
    project = get_object_or_404(Project, id=project_pk)

    if request.method == 'GET':
        contributors = Contributor.objects.filter(project=project)
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data.copy()
        data['project'] = project.id

        try:
            Contributor.objects.get(user=data['user'], project=project.id)
            return Response('This user has already been added.', status=status.HTTP_400_BAD_REQUEST)
        except Contributor.DoesNotExist:
            try:
                User.objects.get(id=data['user'])
                serializer = ContributorSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except User.DoesNotExist:
                return Response('This user does not exist.', status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, ContributorPermissions])
def contributorDetail(request, project_pk, contributor_pk):
    get_object_or_404(Project, id=project_pk)
    contributor = get_object_or_404(Contributor, id=contributor_pk)

    if request.method == 'DELETE':
        if contributor.role == 'AUTHOR':
            return Response('Project author cannot be deleted.', status=status.HTTP_400_BAD_REQUEST)
        else:
            contributor.delete()
            return Response('Contributor successfully deleted.', status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IssuePermissions])
def issueList(request, project_pk):
    project = get_object_or_404(Project, id=project_pk)
    issues = Issue.objects.filter(project=project)#
    serializer = IssueSerializer(issues, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IssuePermissions])
def createIssue(request, project_pk):
    project = get_object_or_404(Project, id=project_pk)
    data = request.data.copy()
    data['project'] = project.id
    data['author'] = request.user.id
    serializer = IssueSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IssuePermissions])
def issueDetail(request, project_pk, issue_pk):
    project = get_object_or_404(Project, id=project_pk)
    issue = get_object_or_404(Issue, id=issue_pk)
    if request.method == 'PUT':
        data = request.data.copy()
        data['project'] = project.id
        data['author'] = issue.author.id
        try:
            serializer = IssueSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Contributor.DoesNotExist:
            return Response(
                'This user is not a contributor to this project or does not exist.',
                status=status.HTTP_400_BAD_REQUEST
            )
    elif request.method == 'DELETE':
        issue.delete()
        return Response('Issue successfully deleted.', status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, CommentPermissions])
def commentList(request, project_pk, issue_pk):
    get_object_or_404(Project, id=project_pk)
    issue = get_object_or_404(Issue, id=issue_pk)

    if request.method == 'GET':
        comments = Comment.objects.filter(issue=issue)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data.copy()
        data['issue'] = issue.id
        data['author'] = request.user.id
        
        serializer = CommentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, CommentPermissions])
def commentDetail(request, project_pk, issue_pk, comment_pk):
    get_object_or_404(Project, id=project_pk)
    #issue = Issue.objects.filter(Issue, id=issue_pk)#####
    issue = Issue.objects.get(id=issue_pk)
    comment = get_object_or_404(Comment, id=comment_pk)
    if request.method == 'GET':
        comments = Comment.objects.filter(issue=issue)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # elif request.method == 'POST':
    #     data = request.data.copy()
    #     data['issue'] = issue.id
    #     data['author'] = request.user.id
        
    #     serializer = CommentSerializer(data=data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        data = request.data.copy()
        data['issue'] = issue.id
        data['author'] = comment.author.id

        serializer = CommentSerializer(comment, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        comment.delete()
        return Response('Comment, successfully deleted.', status=status.HTTP_204_NO_CONTENT)
