from django.urls import reverse, resolve
from user.views import *
from django.test import SimpleTestCase

class TestUrls(SimpleTestCase):

	#Based off https://www.youtube.com/watch?v=0MrgsYswT1c&t=595s example
	def test_register_url_is_resolved(self):
		url = reverse('register')
		self.assertEquals(resolve(url).func, register)