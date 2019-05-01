# Flesch Readability Score Formula generator
import nltk
from nltk import tokenize
from nltk.tokenize import word_tokenize

nltk.download('punkt')

# Example String inputs to be analyzed by the below function
#str_text = str(input("Enter the text you want to analyze. Text must be a sentence: "))
#str_text = 'Our mission is to organize the world’s information and make it universally accessible and useful.'
#str_text = 'The most powerful products for business are the ones people already love to use. Apple products have always been designed for the way we work as much as for the way we live. Today they help employees to work more simply and productively, solve problems creatively and collaborate with a shared purpose. And they’re all designed to work together beautifully. When people have access to iPhone, iPad and Mac, they can do their best work and reimagine the future of their business.'
str_text = 'Turn first-time users into lifelong customers. Build better products, create engaging marketing campaigns, and tie them together into seamless, personalized journeys your customers will love. Taplytics combines industry-leading product optimization and AI-driven marketing capabilities to create deeply personalized experiences across the entire customer lifecycle—without putting user privacy at risk.'
#str_text = 'Artificial Intelligence for the Insurance industry. Chisel offers the global insurance industry the only out-of-the-box solutions that apply natural language processing and AI to unstructured data sources such as insurance documents. These solutions empower insurers, reinsurers, and brokers to free trapped knowledge and automate E&O policy checking, submission prioritization, quote comparison, and submission triage.'

class word_initialize:
	# adding text argument to the class, so it initializes with text inside the class
	def __init__(self, text):
		self.text = text

	def word_count(self):
		# tokenize.sent_tokenize used to parse our input text
		sentences = tokenize.sent_tokenize(self.text)
		word_count = []
		# for each sentence in our text
		for sentence in sentences:
			length_sentence = 0 # Each sentence will have a 'length_sentence' interger which will count how many words are in the sentence
			# For each word in our sentence if the word is not a symbol, then we can increase our word count
			for x in word_tokenize(sentence):
				if x not in ['\'', '.', '!','?', '’']:
					length_sentence += 1
			word_count.append(length_sentence - 1) # Append our sentence length back to our word count list

		return sum(word_count), float(len(word_count)) # Returns the number of words inside our input text, and then number of sentences inside our input text

	def syllable_count(self):
		vowels = "aeiouyAEIOUY" # Initialize vowels for function
		sentences1 = tokenize.sent_tokenize(self.text) # Once again tokenize our sentences
		syllable_num = [] 

		for word1 in sentences1: # For each sentence in our sentences
			for val1 in word_tokenize(word1): # For each word in the given sentence
				syl_count = 0
				if val1[0] in vowels: # Check if first letter of the word is a vowel
					syl_count += 1
				for index in range(1, len(val1)): # For each letter after the first letter 
					if val1[index] in vowels and val1[index -1] not in vowels and val1[index] not in ['\'', '.', '!','?', '’']: # Checking to see if our letter is a vowel, if the previous letter was a vowel , and if our letter is a symbol
						syl_count += 1
				if val1[-1] in "eE": # If our word ends in the letter 'e', need to take away a vowel
					syl_count -= 1
				if syl_count == 0 and val1 not in ['\'', '.', '!','?', '’']: # Somehow if a word does not have a vowel and is not a symbol, has to have a symbol count of 1
					syl_count += 1

				syllable_num.append(syl_count)

		return sum(syllable_num), float(len(syllable_num)) # Returns the total number of syllables in our text, along with the total number of words

class flesch_readability(word_initialize):
	def __init__(self, text):
		super().__init__(text)

	def avg_word_sen(self):
		return (self.word_count()[0] / self.word_count()[1]) # Returns the average # of words per sentence in our text

	def avg_syl_word(self):
		return (self.syllable_count()[0] / self.word_count()[0]) # Returns the # of syllables per word in our text

	def FRS(self):
		v1 = round(self.avg_word_sen(), 2)
		v2 = round(self.avg_syl_word(), 2)
		v3 = round(206.835 - (1.015 * v1) - (84.6 * v2), 2) # Calculation of the flesch readability score

		return v1, v2, v3

	def FKRS(self):
		v4 = round(0.39 * self.FRS()[0] + 11.8 * self.FRS()[1] - 15.59, 2) # Calculation of the Flesch Kincaid Readability Score

		return v4

class automated_readability(flesch_readability):
	def __init__(self, text):
		super().__init__(text)

	def char_count(self):
		sentences2 = tokenize.sent_tokenize(self.text) # Tokenizing our text to split it into sentences again
		character_count = 0
		for word2 in sentences2: # For each sentence in our sentences
			for char in word2: # For each character in the sentence
				if char not in ['\'', '.', '!','?', '’', ' ']:
					character_count += 1 # Increase the character count variable by one if the character is not a symbol

		return character_count # Return the character count

	def ARI(self):
		v5 = round(self.char_count() / self.word_count()[0], 2) # Calling character and word count variables 
		v6 = 4.71 * v5 + 0.5 * self.avg_word_sen() - 21.43 

		return round(v6,2) # Calculation and return of the automated readability index

#print(word_initialize(str_text).word_count())
#print(word_initialize(str_text).syllable_count())
#print(flesch_readability(str_text).FRS())
#print(flesch_readability(str_text).FKRS())
#print(automated_readability(str_text).char_count())
#print(automated_readability(str_text).ARI())

# Printing off values in a sensible format 
print('Character Count: {} Characters'.format(automated_readability(str_text).char_count()))
print('Word Count: {} Words.'.format(word_initialize(str_text).word_count()[0]))
print('Syllable Count: {} Syllables'.format(word_initialize(str_text).syllable_count()[0]))
print('Flesch Readability Score: {} / 100 (Higher is easier to read)'.format(flesch_readability(str_text).FRS()[2]))
print('Flesch - Kincaid Readability Score: {} (Lower is easier to read)'.format(flesch_readability(str_text).FKRS()))
print('Automated Readability Index: {} (Lower is easier to read)'.format(automated_readability(str_text).ARI()))