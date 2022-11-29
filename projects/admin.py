from django.contrib import admin
from .models import Project, Contributor



@admin.register(Project)
class Project(admin.ModelAdmin):

    list_display = ['id', 'title', 'type', 'author', 'author_id'] 



@admin.register(Contributor)
class Contributor(admin.ModelAdmin):

    list_display = ['user', 'project', 'role'] 






