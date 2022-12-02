from django.db import models
from django.conf import settings


class Choice:
    TYPES = [
        ('BACKEND', 'BACKEND'),
        ('FRONTEND', 'FRONTEND'),
        ('iOS', 'iOS'),
        ('ANDROID', 'ANDROID')
    ]

    ROLES = [
        ('AUTHOR', 'AUTHOR'),
        ('CONTRIBUTOR', 'CONTRIBUTOR')
    ]

    TAGS = [
        ('BUG', 'BUG'),
        ('TASK', 'TASK'),
        ('UPGRADE', 'UPGRADE')
    ]

    PRIORITIES = [
        ('LOW', 'LOW'),
        ('MEDIUM', 'MEDIUM'),
        ('HIGH', 'HIGH')
    ]

    STATUSES = [
        ('TODO', 'TODO'),
        ('IN PROGRESS', 'IN PROGRESS'),
        ('DONE', 'DONE')
    ]


class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    type = models.CharField(choices=Choice.TYPES, max_length=8)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')

    def __str__(self):
        return self.title 


class Contributor(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, related_name='contributors')
    role = models.CharField(max_length=11, choices=Choice.ROLES, default='CONTRIBUTOR')

    def __str__(self):
        return f"{self.user} {self.project} {self.role}"


class Issue(models.Model):
    title = models.CharField(max_length=128)
    desc = models.TextField(max_length=2048)
    tag = models.CharField(choices=Choice.TAGS, max_length=7)
    priority = models.CharField(choices=Choice.PRIORITIES, max_length=6, default='LOW')
    status = models.CharField(choices=Choice.STATUSES, max_length=11, default='TODO')
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_to", null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    desc = models.TextField(max_length=2048)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} {self.issue}"
