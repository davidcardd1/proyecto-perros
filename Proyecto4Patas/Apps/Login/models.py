from django.db import models

# Create your models here.
class Usuario (models.Model):
    nombre = models.CharField(max_length=15)
    contrasena=models.CharField(null=True,blank=True,max_length=15)
    user_Name= models.CharField(max_length=15)
    correo=models.EmailField()
    descripcion=models.TextField( null=True,blank=True)
    foto=models.ImageField( null=True,blank=True)
    