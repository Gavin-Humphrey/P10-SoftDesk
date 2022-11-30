from django.contrib import admin
from .models import Project, Contributor, Issue



@admin.register(Project)
class Project(admin.ModelAdmin):

    list_display = ['id', 'title', 'type', 'author', 'author_id'] 



@admin.register(Contributor)
class Contributor(admin.ModelAdmin):

    list_display = ['id', 'user', 'project', 'role'] 


@admin.register(Issue)
class Issue(admin.ModelAdmin):

    list_display = ['title', 'desc', 'tag', 'priority', 'status', 'project', 'author',  'assignee', 'created_time' ] 







