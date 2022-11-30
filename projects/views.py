from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db import IntegrityError
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer
from .models import Issue, Project, Contributor
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import (
    ProjectPermissions,
    ContributorPermissions)



@api_view(['GET'])
@permission_classes([IsAuthenticated, ProjectPermissions])
def projectList(request):
    projects = Project.objects.filter(contributors__user=request.user)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated, ProjectPermissions])
def projectDetail(request, pk):
    projects = get_object_or_404(Project, id=pk)
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
def projectUpdate(request, pk):
    project = get_object_or_404(Project, id=pk)
    serializer = ProjectSerializer(instance=project, data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def projectDelete(request, pk):
    project = get_object_or_404(Project, id=pk)
    project.delete()
    return Response(project.title + " successfully delete!", status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
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
#@permission_classes([IsAuthenticated, ContributorPermissions])
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
#@permission_classes([IsAuthenticated])
def issueList(request, project_pk):
    project = get_object_or_404(Project, id=project_pk)
    issues = Issue.objects.filter(project=project)#
    serializer = IssueSerializer(issues, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
#@permission_classes([IsAuthenticated, ProjectPermissions])
def createIssue(request, project_pk):
    project = get_object_or_404(Project, id=project_pk)
    issues = Issue.objects.filter(project=project)
    data = request.data.copy()
    data['project'] = project.id
    data['author'] = request.user.id
    Contributor.objects.get(id=data['assignee'], project=project.id)
    serializer = IssueSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

