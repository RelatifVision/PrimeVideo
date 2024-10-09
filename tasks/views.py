from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import TaskForm
from .models import Tasks
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == "GET":
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })

    else:
        if request.POST['password1'] == request.POST['password2']: # Comprueba que la password1 == pasword2
            try: # si no pones try except causará los errores de repetir ususario o no coincidir pass
                # Register user y password
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()  # guardar usuario
                login(request, user) # así se registran en las cookies
                return redirect(tasks)
            except IntegrityError: #Muestra error en específico
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Pasword do not match'
        })

@login_required # indicar que requiere login
def tasks(request):
    tasks = Tasks.objects.filter(user=request.user, datecompleted__isnull=True)  # Filtrar tareas incompletas del usuario actual
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    tasks = Tasks.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')  # Filtrar tareas completas del usuario actual poreso en False
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def create_task(request):
    
    if request.method == 'GET':
        return render(request, 'create_task.html', {
        'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)# Recibe los datos y se los pasa a la clase TaskForm en formulario
            new_task = form.save(commit=False) # me devuelva los datos sin guardarlos
            new_task.user = request.user # para comprobar que coincide con el del login
            new_task.save() # guarda dato enla DB
            return redirect('tasks')
        except ValueError: # Cuando consideremos un error de valor
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Please provide valide data',
            })

@login_required            
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Tasks, pk=task_id, user=request.user) # obtenga la tarea del id seleccionado, hasta que indiques idique no exista
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Tasks, pk=task_id, user=request.user) # Muestra solo tareas del usuario
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError: # en caso de generar error
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': "Error updating task"})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id, user=request.user)
    if request.method == 'POST':  # Verificamos que sea un POST
        task.datecompleted = timezone.now()  # Añadir fecha y hora actual
        task.save()  # Guardamos la tarea
        return redirect('tasks')  # Redirigimos a la lista de tareas

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id, user=request.user)
    if request.method == 'POST':  # Verificamos que sea un POST
        task.delete() # Eliminar tarea
        return redirect('tasks')  # Redirigimos a la lista de tareas
        

@login_required    
def cerrar_sesion(request):
    logout(request) # funcion logout desloguea sesion
    return redirect('home') # te reenvia home

def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': "Username or password is"
            })   
        else:
            login(request, user)
            return redirect('tasks')
            
        
          