from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import get_object_or_404
from .models import Project, Contributor
from .serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import ProjectPermission



"""
Below Function going to display all the projects store in the data base.
"""
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, ProjectPermission])
def project_list(request):
    if request.method == 'GET':
        projects = Project.objects.filter(contributors__user=request.user)
        serializer = ProjectSerializer(projects, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = request.data.copy()
        data['author'] = request.user.id
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            Contributor.objects.create(user=request.user, project=project, role='AUTHOR')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, ProjectPermission])
def project_detail(request, pk):
    """
    This Function going to display, update and delete Detailed 
    view of one perticuler project with the help of pk.
    """
    projects = get_object_or_404(Project, id=pk)
    if request.method == 'GET':
        serializer = ProjectSerializer(projects, many = False)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data.copy()
        data['author'] = project.author.id
        serializer = ProjectSerializer(instance = project, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        project = Project.objects.get(id=pk)
        project.delete()
        return Response("Project deleted successfully.", status=status.HTTP_200_OK)