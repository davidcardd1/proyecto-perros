from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Usuario (models.Model):
    nombre = models.CharField(max_length=15)
    contrasena=models.CharField(null=True,blank=True,max_length=15)
    user_Name= models.CharField(max_length=15)
    #user_Name = models.OneToOneField(User)
    correo=models.EmailField()
    descripcion=models.TextField( null=True,blank=True)
    foto=models.ImageField( null=True,blank=True)

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)