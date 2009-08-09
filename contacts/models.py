from django.db import models
_ = lambda x: x


LOCATIONS = (
    (1, 'Work'),
    (2, 'Personal'),
    (3, 'Other')
)

SERVICES = (
    ('aim', 'AIM'),
    ('msn', 'MSN'),
    ('icq', 'ICQ'),
    ('jabber', 'Jabber'),
    ('yahoo', 'Yahoo'),
    ('skype', 'Skype'),
    ('qq', 'QQ'),
    ('sametime', 'Sametime'),
    ('gadu-gadu', 'Gadu-Gadu'),
    ('google-talk', 'Google Talk'),
    ('other', 'Other')
)


class InstantMessenger(models.Model):

    service = models.CharField(_('Service'),
                               max_length=11,
                               choices=SERVICES,
                               default='jabber')
    location = models.IntegerField(_('Location'),
                                   choices=LOCATIONS,
                                   default=1)
    account = models.CharField(_('account'), max_length=150)

    def __unicode__(self):
        return u'%s %s' % (self.account, self.service)
