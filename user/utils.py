import random


def _generate_warframe_account_verification_code(self):
		VALID_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		CODE_LENGTH = 12
		generated_wfa_verification_code = ""

		for i in range(0,CODE_LENGTH):
			rand_char = VALID_CHARS[random.randint(0,len(VALID_CHARS)-1)]
			generated_wfa_verification_code += rand_char

		return generated_wfa_verification_code

def _generate_email_verification_code(self):
		VALID_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
		CODE_LENGTH = 32
		generated_email_verification_code = ""

		for i in range(0,CODE_LENGTH):
			rand_char = VALID_CHARS[random.randint(0,len(VALID_CHARS)-1)]
			generated_email_verification_code += rand_char

		return generated_email_verification_code