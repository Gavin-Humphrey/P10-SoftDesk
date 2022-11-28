from rest_framework.permissions import BasePermission
from projects.models import Project, Contributor


from rest_framework import permissions
from rest_framework.generics import get_object_or_404




class ProjectPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            project = get_object_or_404(Project, id=view.kwargs['pk'])
            if request.method in permissions.SAFE_METHODS:
                return project in Project.objects.filter(contributors__user=request.user)
            return request.user == project.author
        except KeyError:
            return True


class ContributorPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(Project, id=view.kwargs['pk'])
        if request.method in permissions.SAFE_METHODS:
            return project in Project.objects.filter(contributors__user=request.user)
        return request.user == project.author


