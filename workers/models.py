from django.db import models
from django.utils.translation import ugettext_lazy as _
from hostel.storage import AttachmentStorage
import os.path

def rename_avatar(instance, filename):
    username = instance.user.username
    stem, ext = os.path.splitext(filename)
    filename = filename.replace(stem, username)
    return os.path.join('avatars', filename)

class Employee(models.Model):

    user = models.ForeignKey('auth.User', verbose_name=_('User'), unique=True)
    skill = models.ManyToManyField('Skill', verbose_name=_('Skill'))
    avatar = models.ImageField(_('You can upload an avatar image'),
                               blank=True,
                               default='avatars/default.jpg',
                               upload_to=rename_avatar,
                               storage=AttachmentStorage(overwrite=True),)


class Skill(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()

    def __unicode__(self):
        return self.title
