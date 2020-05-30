from django.core.exceptions import ValidationError


class ValidCharactersValidator:
	LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	NUMBERS = "0123456789"
	SYMBOLS = "~!@#$%^&*()_+=-][.?"
	valid_chars = LETTERS+NUMBERS+SYMBOLS

	def __init__(self):
		pass

	def validate(self, password):
		'''
		Determine if password contains only characters in
		'valid_chars'. If password contains a characters
		not in 'valid_chars' then a ValidationError is raised.
		'''
		
		# if valid_chars is None:
		# 	raise ValueError("valid_chars can not be None")
			
		for pw_char in password:
			if (pw_char in self.valid_chars) == False:
				raise ValidationError(("Invalid character for string '%s'. The list of valid chars are: '%s'", (password, self.valid_chars)),
				code="invalid_char_exists")


	def get_help_text(self):
		msg = "Your password mustcontain valid character: letters, numbers, or the following symbols " + self.SYMBOLS
		return msg

class MaximumLengthValidator:
	max_len = 0

	def __init__(self, max_len=32):
		if max_len is None or max_len < 0:
			raise ValueError("max_len is required and must be positive")

		self.max_len=max_len
	
	def validate(self, password):
		'''
		Determine if a password is too long. If it exceeds
		a character limit, raises a ValidationError.
		'''
		if len(password) > self.max_len:
			raise ValidationError(
			("Character limit of this password cannot exceed %(max_len)d characters"),
			code="max_character_limit",
			params={'max_len': self.max_len}
			)

	def get_help_text(self):
		msg = "Your password cannot exceed %(max_len)d characters." % {'max_len': self.max_len}
		return msg

