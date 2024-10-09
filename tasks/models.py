from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Crear una tabla ORM django con SQL en-->  Task/forms.py (Utilizar)
class Tasks(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True) # añade fecha y hora automaticamente al crear tarea
    datecompleted = models.DateTimeField(null=True, blank=True) # Campo vacio inicialmente, permite admin no rellenarlo
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title + '- by ' + self.user.username # mostrar titulo de la tarea y su 'username' de 'user'