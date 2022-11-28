from django.contrib import admin
from .models import Project


admin.site.register(Project)



class Project(admin.ModelAdmin):

    list_display = ('title', 'author')





