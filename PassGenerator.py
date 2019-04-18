#### Password Generator; can create Simple and Complex passwords
#### Can easily add and modify the list for Simple passwords

import random

def password_gen(Simple=True):
	if Simple == True:
		result = random.choice(['Abstract', 'Acceptable', 'Banker', 'Candidate', 'Campaign']) # Simple words for Password Generator
	else:
		pass_len = random.randrange(8,17)

		alphabet = 'abcdefjhijklmnopqrstuvwxyz' # Initializing the Alphabet
		symbols = '!@#$%^&*' # Initializing Symbols
		weight_choices = [('alphabet', 4), ('symbols', 2), ('numbers', 4)] # 40% chance letters 20% chance symbols, 40% chance numbers 
		choices = [val for val, cnt in weight_choices for i in range(cnt)]

		result = []

		for x in range(pass_len): # This is password length, generated randomly between 8 and 16 characters
			if random.choice(choices) == 'alphabet': # Random choices in our choices list, append a random letter 
				result.append(random.choice(alphabet))
			elif random.choice(choices) == 'symbols': # Random choices in our choices list, append a random symbol
				result.append(random.choice(symbols))
			else:
				result.append(random.randrange(0,10)) # Append a random number 
		result = ''.join(str(y) for y in result) # Converts list into string by joining each character

	return result #


## Printing the generated password for both a Simple and Non - Simple example
print(password_gen(Simple=True))
print(password_gen(Simple=False))
