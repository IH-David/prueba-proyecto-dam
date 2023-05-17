from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import CustomUserCreationForm
from .models import Pregunta, Respuesta
from django.contrib.auth.decorators import login_required

import openai

# Create your views here.


@login_required
def index(request):
    return render(request, 'chat/index.html')

def specific(request):
    list1 = [1,2,3,4]
    return HttpResponse(list1)

@login_required
def getResponse(request):
    openai.api_key = "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"
    context = {"role": "system","content":"Tienes que repetir lo que yo digo pero respondeme en mayuscula y con exclamaciones"}
    messages = [context]
    userMessage =  request.GET.get('userMessage')
    messages.append({"role": "user","content":userMessage})
    
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                    messages = messages)
    
    response_content = str(response.choices[0].message.content)
        
    messages.append({"role": "assistant", "content": response_content})
    
    #Inserción base de datos
    usuario = request.user
    
    pregunta = Pregunta(mensaje=userMessage, usuario=usuario)
    pregunta.save()
    
    respuesta = Respuesta(mensaje=response_content, pregunta=pregunta)
    respuesta.save()
    
    """ texto = ''
    for message in messages:
        if isinstance(message, dict):
            mensaje_str = ', '.join(f"{key}: {value}" for key, value in message.items())
            texto += mensaje_str + '\n'
        else:
            texto += str(message) + '\n'

    file = open("nuevo_archivo.txt","w")
    file.write(texto)
    file.close() """
    
    return HttpResponse(response_content)


def signup(request):

    if request.method == 'GET':
        print('Enviando formulario')
        return render(request, 'signup.html', {'form': CustomUserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Registrar usuario
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': CustomUserCreationForm,
                    "error": 'Usuario ya existe'
                })

        return render(request, 'signup.html', {
            'form': CustomUserCreationForm,
            "error": 'Contraseñas no coinciden'
        })

@login_required
def signout(request):
    logout(request)
    return redirect('signin')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error':'Usuario o contraseña no válidos'
            })
        else:
            login(request, user)
            return redirect('index')