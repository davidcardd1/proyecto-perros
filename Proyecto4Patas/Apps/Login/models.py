from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Usuario (models.Model):
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