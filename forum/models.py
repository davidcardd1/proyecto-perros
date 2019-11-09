from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save


class Usuario (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField('Profile pic', blank=True, default='')
    post_count = models.IntegerField('Post count', blank=True, default=0)
    bio = models.TextField(max_length=2500, null=True,blank=True, default='')
    
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Usuario.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User) 

class Topic(models.Model):
    name = models.CharField('Subject', max_length=50, unique=True)
    description = models.CharField(max_length=150)
    created = models.DateTimeField('Created', auto_now_add=True)
    updated = models.DateTimeField('Updated', null=True)
    user = models.ForeignKey(Usuario, related_name='topicUser',on_delete=models.CASCADE)
    no_views = models.IntegerField('Views count', blank=True, default=0)
    subscribers = models.ManyToManyField(Usuario, blank=True, related_name='topics')
    post_count = models.IntegerField('Post count', blank=True, default=0)

    def __str__(self):
        return self.name

class Thread(models.Model):
    name = models.CharField('Name', max_length=255)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, default='0', related_name='threads')
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE,  related_name='threads')
    created = models.DateTimeField('Created', auto_now_add=True)
    updated = models.DateTimeField('Updated', auto_now=True)
    body = models.TextField('Message')
    body_html = models.TextField('HTML version')
    post_count = models.IntegerField('Post count', blank=True, default=0)
    #last_post = models.ForeignKey('Post', related_name='last_forum_post', blank=True, null=True)
    def __str__(self):
        return self.name


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=False, default='0', related_name='posts')
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE,  related_name='posts')
    created = models.DateTimeField('Created', auto_now_add=True)
    updated = models.DateTimeField('Updated', auto_now=True)
    body = models.TextField('Message')
    body_html = models.TextField('HTML version')
