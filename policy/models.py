from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import curry
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


class Programme(PolicyModel):
    description = MarkdownField(_('Description'))
    account = models.ForeignKey('Account', verbose_name=_('Account'))


FK = curry(models.ForeignKey, blank=True, null=True, to='auth.User')
class Project(PolicyModel):
    am = FK(verbose_name=_('Account Manager'), related_name='am_for')
    pm = FK(verbose_name=_('Project Manager'), related_name='pm_for')
    tech = FK(verbose_name=_('Technical Lead'), related_name='tech_lead_for')
    design = FK(verbose_name=_('Design lead'), related_name='design_lead_for')
    owner = FK(verbose_name=('Project owner'), related_name='projects_owned')
    programme = FK(to='Programme', verbose_name='Programme')
    account = FK(to='Account', verbose_name='Account', blank=False)
    description = MarkdownField(_('Description'))

