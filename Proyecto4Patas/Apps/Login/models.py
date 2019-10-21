from django.db import models
from django.conf import settings
from Proyecto4Patas.fields import AutoOneToOneField, ExtendedImageField, JSONField

# Create your models here.
class Usuario (models.Model):
    
    user = OneToOneField(settings.AUTH_USER_MODEL, related_name='forum_profile', verbose_name=_('User'))
    profile_pic = ImageField(_('Profile pic'), blank=True, default='')
    post_count = models.IntegerField(_('Post count'), blank=True, default=0)
    email = models.EmailField()
    description=models.TextField( null=True,blank=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def last_post(self):
        posts = Post.objects.filter(user__id=self.user_id).order_by('-created')
        if posts:
            return posts[0].created
        else:
            return None
    
