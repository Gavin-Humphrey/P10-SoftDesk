from django.contrib import admin
from django.contrib.auth.models import User 


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 
                    'last_name', 'is_superuser', 'is_staff'
                    ]
    readonly_fields = ('id',)
    list_filter = ('is_staff',)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
    

