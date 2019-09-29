from django.db import models
from Apps.Login.models import Usuario

# Create your models here.
class Post (models.Model):
    ide=models.IntegerField(primary_key=True)
    fecha=models.DateField()
    contenido=models.TextField(max_length=200)
    respuestas=models.IntegerField()
    owner=models.ForeignKey(Usuario,null=True,blank=True, on_delete=models.CASCADE)

class Comentario(models.Model):
    ide=models.IntegerField(primary_key=True)
    fecha=models.DateField()
    contenido=models.TextField(max_length=200)
    Post=models.ForeignKey(Post, null=True,blank=True, on_delete=models.CASCADE)

