from django.db import models
<<<<<<< HEAD
=======
from django.conf import settings
>>>>>>> base1
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Usuario (models.Model):
<<<<<<< HEAD
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
=======
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField('Profile pic', blank=True, default='')
    post_count = models.IntegerField('Post count', blank=True, default=0)
    email = models.EmailField()
    description=models.TextField( null=True,blank=True)

""" class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def last_post(self):
        posts = Post.objects.filter(user__id=self.user_id).order_by('-created')
        if posts:
            return posts[0].created
        else:
            return None
"""
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Usuario.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User) 
>>>>>>> base1
