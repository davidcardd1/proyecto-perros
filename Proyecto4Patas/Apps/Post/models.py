from django.db import models
from Apps.Login.models import Usuario

# Create your models here.

    
 class Post(models.Model):
    topic = models.ForeignKey(Topic, related_name='posts', verbose_name=_('Topic'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', verbose_name=_('User'))
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), blank=True, null=True)
    body = models.TextField(_('Message'))
    body_html = models.TextField(_('HTML version'))


    class Meta:
        ordering = ['created']
        get_latest_by = 'created'
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def save(self, *args, **kwargs):
        self.body_html = convert_text_to_html(self.body, self.markup)
        super(Post, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self_id = self.id
        head_post_id = self.topic.posts.order_by('created')[0].id
        forum = self.topic.forum
        topic = self.topic
        profile = self.user.forum_profile
        self.last_topic_post.clear()
        self.last_forum_post.clear()
        super(Post, self).delete(*args, **kwargs)
        #if post was last in topic - remove topic
        if self_id == head_post_id:
            topic.delete()
        else:
            try:
                topic.last_post = Post.objects.filter(topic__id=topic.id).latest()
            except Post.DoesNotExist:
                topic.last_post = None
            topic.post_count = Post.objects.filter(topic__id=topic.id).count()
            topic.save()
        try:
            forum.last_post = Post.objects.filter(topic__forum__id=forum.id).latest()
        except Post.DoesNotExist:
            forum.last_post = None
        #TODO: for speedup - save/update only changed fields
        forum.post_count = Post.objects.filter(topic__forum__id=forum.id).count()
        forum.topic_count = Topic.objects.filter(forum__id=forum.id).count()
        forum.save()
        profile.post_count = Post.objects.filter(user__id=self.user_id).count()
        profile.save()

    
class Forum(models.Model):
    name = models.CharField(_('Name'), max_length=80)
    position = models.IntegerField(_('Position'), blank=True, default=0)
    description = models.TextField(_('Description'), blank=True, default='')
    updated = models.DateTimeField(_('Updated'), auto_now=True)
    post_count = models.IntegerField(_('Post count'), blank=True, default=0)
    last_post = models.ForeignKey('Post', related_name='last_forum_post', blank=True, null=True)

    class Meta:
        ordering = ['position']
        verbose_name = _('Forum')
        verbose_name_plural = _('Forums')

    def __str__(self):
        return self.name

    @property
    def posts(self):
        return Post.objects.filter(topic__forum__id=self.id).select_related()



class Topic(models.Model):
    name = models.CharField(_('Subject'), max_length=255)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'))
    views = models.IntegerField(_('Views count'), blank=True, default=0)
    closed = models.BooleanField(_('Closed'), blank=True, default=False)
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subscriptions', verbose_name=_('Subscribers'), blank=True)
    post_count = models.IntegerField(_('Post count'), blank=True, default=0)
    last_post = models.ForeignKey('Post', related_name='last_topic_post', blank=True, null=True)

    class Meta:
        ordering = ['-updated']
        get_latest_by = 'updated'
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        try:
            last_post = self.posts.latest()
            last_post.last_forum_post.clear()
        except Post.DoesNotExist:
            pass
        else:
            last_post.last_forum_post.clear()
        forum = self.forum
        super(Topic, self).delete(*args, **kwargs)
        try:
            forum.last_post = Topic.objects.filter(forum__id=forum.id).latest().last_post
        except Topic.DoesNotExist:
            forum.last_post = None
        forum.topic_count = Topic.objects.filter(forum__id=forum.id).count()
        forum.post_count = Post.objects.filter(topic__forum__id=forum.id).count()
        forum.save()

    @property
    def head(self):
        try:
            return self.posts.select_related().order_by('created')[0]
        except IndexError:
            return None

    @property
    def reply_count(self):
        return self.post_count - 1

    def update_read(self, user):
        tracking = user.posttracking
        #if last_read > last_read - don't check topics
        if tracking.last_read and (tracking.last_read > self.last_post.created):
            return
        if isinstance(tracking.topics, dict):
            #clear topics if len > 5Kb and set last_read to current time
            if len(tracking.topics) > 5120:
                tracking.topics = None
                tracking.last_read = timezone.now()
                tracking.save()
            #update topics if exist new post or does't exist in dict
            if self.last_post_id > tracking.topics.get(str(self.id), 0):
                tracking.topics[str(self.id)] = self.last_post_id
                tracking.save()
        else:
            #initialize topic tracking dict
            tracking.topics = {self.id: self.last_post_id}
            tracking.save()

