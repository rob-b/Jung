from django.test import TestCase
from models import InstantMessenger
from django.contrib.auth.models import User

class ImTest(TestCase):

    def test_im(self):
        im = InstantMessenger.objects.create(account='rberry')
        user = User.objects.create_user('rob', 'rob@example.com', 'password')
        profile = user.get_profile()
        profile.im.add(im)
