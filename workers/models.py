from django.db import models
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
from hostel.storage import AttachmentStorage
import os.path

def rename_avatar(instance, filename):
    username = instance.user.username
    stem, ext = os.path.splitext(filename)
    filename = filename.replace(stem, username)
    return os.path.join('avatars', filename)

def create_employee_profile(sender, **kwargs):
    if 'created' not in kwargs or not kwargs['created']:
        return
    if not hasattr(settings, 'AUTH_PROFILE_MODULE'):
        return
    user = kwargs.get('instance')
    app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
    model = models.get_model(app_label, model_name)
    try:
        profile = model.objects.create(user=user)
    except Exception, e:
        raise e
models.signals.post_save.connect(create_employee_profile, sender=User)


class Employee(models.Model):

    user = models.ForeignKey('auth.User', verbose_name=_('User'), unique=True)
    skill = models.ManyToManyField('Skill', verbose_name=_('Skill'),
                                   blank=False, null=True)
    avatar = models.ImageField(_('Avatar'),
                               blank=True,
                               default='avatars/default.jpg',
                               upload_to=rename_avatar,
                               storage=AttachmentStorage(overwrite=True),)
    role = models.ForeignKey('Role', verbose_name=_('Role'),
                             blank=False, null=True)

    def __unicode__(self):
        return _('Employee profile for %s') % self.user.username

    @models.permalink
    def get_absolute_url(self):
        return ('profiles_profile_detail', (self.user.username,))


class Skill(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField()

    def __unicode__(self):
        return self.title

class Role(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField()

    def __unicode__(self):
        return self.title
