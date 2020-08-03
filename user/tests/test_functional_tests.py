from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from user.models import *
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.urls import reverse
from django.conf import settings

import time

class ForgotPwEmailSentFunctionalTests(StaticLiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		print("setUpClass called start")
		#self.browser = webdriver.Chrome(settings.CHROME_DRIVER_PATH)
		super().setUpClass()
		#cls.selenium = webdriver.Chrome('user/tests/chromedriver.exe')
		
		cls.selenium = WebDriver(executable_path=settings.FIREFOX_DRIVER_PATH)
		#cls.selenium.implicitly_wait(10)
		#cls.selenium.implicitly_wait(5)
		print("setUp called end")

	@classmethod
	def tearDownClass(cls):
		print("tearDownClass called start")
		#cls.selenium.quit()
		cls.selenium.quit()
		super().tearDownClass()
		print("tearDown called end")

	# def setUp(self):
	# 	print("setUp called")
	# 	self.selenium = WebDriver(executable_path=settings.FIREFOX_DRIVER_PATH)

	# def tearDown(self):
	# 	super.tearDown(ForgotPwEmailSentFunctionalTests, self)
	# 	print("tearDown called")
	# 	self.selenium.close()

	def test_first_selenium_test(self):
		print("test_first_selenium_test start")
		#path = reverse('user:forgot_pw_email_sent')
		self.selenium.get(self.live_server_url)
		print("test_first_selenium_test end")
		

	def test_home_page_link_works(self):
		'''Home page link is displayed and should redirect user
		to the home page.'''
		print("test_home_page_link_works start")
		path = reverse('user:forgot_pw_email_sent')
		self.selenium.get(self.live_server_url + path)
		print("self.live_server_url is: %s" % (self.live_server_url))
		print("reverse string produces %s" % (reverse('user:forgot_pw_email_sent')))
		time.sleep(1)
		home_ancor = self.selenium.find_element_by_id('return-home')
		home_ancor.click()

		time.sleep(2)
		print("test_home_page_link_works end")
		

		
		
