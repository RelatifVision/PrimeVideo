from django import forms
from .models import Tasks

class TaskForm(forms.ModelForm):
    class Meta:              
        model = Tasks       # Eligiriamos la tabla del modelo para hacer el formulario  
        fields = ['title', 'description', 'important'] # Elegimos campos que queremos envíar
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'
            }),
        } # Nos permite colocar diccionario como valor para especificar otros inputs que está generando, PARA ESTILIZAR FORMULARIO