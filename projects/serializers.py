from rest_framework import serializers
from projects.models import Project, Contributor



class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'
        read_only__fields = ('author', 'id')


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = '__all__'
        read_only__fields = ('project', 'role', 'id')

