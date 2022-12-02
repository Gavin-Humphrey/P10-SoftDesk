from django.contrib import admin
from .models import Project, Contributor, Issue, Comment



@admin.register(Project)
class Project(admin.ModelAdmin):

    list_display = ['id', 'title', 'type', 'author', 'author_id'] 


@admin.register(Contributor)
class Contributor(admin.ModelAdmin):

    list_display = ['id', 'user', 'project', 'role'] 


@admin.register(Issue)
class Issue(admin.ModelAdmin):

    list_display = ['id', 'title', 'desc', 'tag', 'priority', 'status', 
                    'project', 'author',  'assignee', 'created_time' 
                    ] 


@admin.register(Comment)
class Comment(admin.ModelAdmin):

    list_display = ['id', 'desc', 'author', 'issue', 'created_time'] 








