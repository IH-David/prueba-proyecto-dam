from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Pregunta(models.Model):
    mensaje = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

class Respuesta(models.Model):
    mensaje = models.CharField(max_length=255)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, default=None)


    
    