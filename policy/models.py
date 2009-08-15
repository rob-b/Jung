from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import curry
from django.contrib.auth.models import User
from hostel.models import MarkdownField
from django_extensions.db.fields import AutoSlugField


class PolicyModel(models.Model):
    PROSPECT, ACTIVE, DORMANT, CLOSED = range(4)
    STATUS_CHOICES = (
        (PROSPECT, _('Prospect')),
        (ACTIVE, _('Active')),
        (DORMANT, _('Dormant')),
        (CLOSED, _('Closed')),
    )
    status = models.SmallIntegerField(_('status'),
                                      choices=STATUS_CHOICES)
    name = models.CharField(_('Name'), max_length=150)
    slug = AutoSlugField(editable=True, populate_from='name')

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        abstract = True


class Account(PolicyModel):
    colour = models.CharField(_('Colour'), max_length=6, blank=True)
    description = MarkdownField(_('Description'))

    def get_absolute_url(self):
        return '/foo/'


class Programme(PolicyModel):
    description = MarkdownField(_('Description'))
    account = models.ForeignKey('Account', verbose_name=_('Account'))


FK = curry(models.ForeignKey, blank=True, null=True, to=User)
class Project(PolicyModel):
    account_manager = FK(verbose_name=_('Account Manager'), related_name='am_for')
    project_manger = FK(verbose_name=_('Project Manager'), related_name='pm_for')
    technical_lead = FK(verbose_name=_('Technical Lead'), related_name='tech_lead_for')
    design_lead = FK(verbose_name=_('Design lead'), related_name='design_lead_for')
    owner = FK(verbose_name=_('Project owner'), related_name='projects_owned')
    programme = FK(to='Programme', verbose_name='Programme')
    account = FK(to='Account', verbose_name='Account', blank=False)
    description = MarkdownField(_('Description'))

    @property
    def user_relations(self):
        for field, model in self._meta.get_fields_with_model():
            instance = None
            try:
                if issubclass(field.rel.to, User):
                    instance = getattr(self, field.name)
            except AttributeError:
                continue
            if instance is not None:
                yield field.verbose_name, instance

    @models.permalink
    def get_absolute_url(self):
        return ('policy_project_detail', [self.slug])
