from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProjectSerializer
from .models import Project, Contributor



@api_view(['GET'])
def projectList(request):
    projects = Project.objects.filter()#contributors__user=request.user
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def projectDetail(request, pk):
    projects = Project.objects.get(id=pk)
    serializer = ProjectSerializer(projects, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def projectCreate(request):
    serializer = ProjectSerializer(data=request.data)
    #print(serializer)
    if serializer.is_valid(raise_exception=True):
        project = serializer.save()
        #Contributor.objects.create(user=request.user, project=project, role='AUTHOR')
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

@api_view(['PUT'])
def projectUpdate(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(instance=project, data=request.data)
    #print(serializer)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def projectDelete(request, pk):
    project = Project.objects.get(id=pk)
    project.delete()
    
    return Response(project.title + " successfully delete!")



