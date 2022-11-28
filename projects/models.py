
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
        return self.user