from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.permissions import IsAuthenticated
from projects.permissions import ProjectPermission




class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
    # Si l'action demandée est retrieve nous retournons le serializer de détail
        #if self.action == 'retrieve':
        if self.action == 'GET' and self.detail_serializer_class is not None:    
            return self.detail_serializer_class
        return super().get_serializer_class()


#@permission_classes([IsAuthenticated, ProjectPermission])
class ProjectListApiView(MultipleSerializerMixin, ReadOnlyModelViewSet):
   
    permission_classes = [permissions.IsAuthenticated, ProjectPermission]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the projects items for given requested user
        '''
        projects = Project.objects.filter(user = request.user.id)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Project with given project data
        '''
        data = request.data.copy()
        data['author'] = request.user.id
        
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)