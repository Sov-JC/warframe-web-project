from django.core.exceptions import ValidationError


def valid_password_characters(password):
	'''
	Determine if password contains only specific characters.
	'''
	LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	NUMBERS = "0123456789"
	SYMBOLS = "~!@#$%^&*()_+=-][.?<>,/|}{`"
	valid_chars = LETTERS+NUMBERS+SYMBOLS
	
	# if valid_chars is None:
	# 	raise ValueError("valid_chars can not be None")
		
	for pw_char in password:
		if (pw_char in valid_chars) == False:
			raise ValidationError(("Invalid character for string '%s'. The list of valid chars are: '%s'", (password, valid_chars)),
			code="invalid_char_exists")