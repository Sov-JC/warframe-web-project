import string
import random
from django.apps import apps

#Untested
def generate_random_string(chars, length):
	'''Generates a fixed length sequence of random characters.

	:param chars: Characters that the generator can select from
	to generate the string.
	:type chars: String
	:param length: The length of the password recovery code.
	:type length: Integer
	...
	:return: A randomly generated string of characters of length
	'length' from the list of valid characters, 'chars'.
	:rtype: String
	'''
	random_string = ""
	for i in range(length):
		random_char = chars[random.randint(0, len(chars)-1)]
		random_string += random_char

	return random_string