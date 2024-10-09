from django.contrib import admin
from .models import Tasks

class TaskAdmin(admin.ModelAdmin): # mostrar fecha creaccion
    readonly_fields = ("created", )
    
# Register your models here.
admin.site.register(Tasks, TaskAdmin)