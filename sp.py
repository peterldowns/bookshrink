#!/usr/bin/env python
import re
			
class sentenceAnalyzer():
	def clean(self, s):
		""" Get rid of any non-alphabetic character and clean up whitespace """
		s = re.sub(r'[^a-zA-Z]', ' ', s) # remove everything that isn't an alphabet character (only interested in words, not numbers or punctuation)
		s = re.sub(r'\s+', ' ', s) # change multiple whitespace in a row to a single space
		return s
	def __init__(self, input_string=None, seed_string=None, uselemmat=False, usepunkt=False):
		# Set up the input string
		if input_string is not None:
			self.inputstr = (input_string)
		else:
			self.inputstr = ""
		# deal with the optional seed strings
		self.seed_string = seed_string # this should be a comma separated string of words to be weighted extra
		self.seeds = None
		if self.seed_string is not None:
			self.seeds = [self.clean(s).strip().lower() for s in self.seed_string.split(',')] # split based on ', then clean up everything
		# darkest highlight color
		self.darkest="#FF0F0F"
		# Define the ~100 most common words in the english language (which are ignored in the analysis)
		# according to http://www.duboislc.org/EducationWatch/First100Words.html
		self.commonstr = "mr mrs ms dr the of and a to in is you that it he was for on are as with his they i at be this have from or one had by word but not what all were we when your can said there use an each which she do how their if will up other about out many then them these so some her would make like him into time has look two more write go see number no way could people my than first water been call who oil its now find long down day did get come made may part am let"
		self.radical_mod_method = False
		self.uselemmat = uselemmat # whether not to try to lemmatize the text
		self.usepunkt = usepunkt # whether or not to use the PunktSentenceTokenizer to split sentences

	def analyze(self, input_string=None):
		if input_string is not None:
			self.inputstr = input_string # holds the actual input
		""" SPLIT INPUT INTO SENTENCES"""
		if self.usepunkt:
			from nltk.tokenize.punkt import PunktSentenceTokenizer
			tokenizer = PunktSentenceTokenizer()
			self.sentences = tokenizer.tokenize(self.inputstr.strip())
		else:
			god_awful_regex = r'''(?<!\d)(?<![A-Z]\.)(?<!\.[a-z]\.)(?<!\.\.\.)(?<!etc\.)(?<![Mm]r\.)(?<![Pp]rof\.)(?<![Dd]r\.)(?<![Mm]rs\.)(?<![Mm]s\.)(?<![Mm]z\.)(?<![Mm]me\.)(?:(?<=[.!?])|(?<=[.!?]['"]))[\s]+?(?=[\S])'''
			self.sentences = re.split(god_awful_regex, self.inputstr.strip())

		""" GET JUST THE WORDS OUT OF THE TEXT """
		if self.uselemmat:
			from nltk.stem.wordnet import WordNetLemmatizer
			_wnl = WordNetLemmatizer() # create a lemmatizer instance only once
			def lmtz(orig, l): # string, lemmatizer instance
				instr = orig.lower()
				types = ['n', 'v', 'a', 'r'] # noun, verb, adjective, adverb
				outstr = instr
				for t in types:
					tmp = l.lemmatize(instr, t)
					if (tmp != instr): # if we've successfully lemmatized to a different word
						outstr = tmp
						break
				if orig.istitle():
					outstr = outstr.title()
				return outstr
			self.words = [lmtz(x, _wnl) for x in self.clean(self.inputstr).split()]
		else:
			self.words = self.clean(self.inputstr).split()
		""" ASSIGN EACH WORD A FREQUENCY """
		self.wfreq = {} # keeps track of word frequencies
		for word in self.words:
			if word.lower() not in self.commonstr: # make sure it's an important word, not a shit word
				if word in self.wfreq:
					self.wfreq[word] += 1
				else:
					self.wfreq[word] = 1
		""" MODIFY THE FREQUENCIES BASED ON CERTAIN CONDITIONS """
		for word in self.wfreq:
			if word.istitle() and not word.isupper(): # if it's a proper noun
				self.wfreq[word] = self.wfreq[word]*2
			if self.seeds is not None and word.lower() in self.seeds: # if the word matches a user-supplied list of important words (seeds)
				self.wfreq[word] = self.wfreq[word]*3 # this should be considered *super* important
		""" ASSIGN EACH SENTENCE A SCORE """
		self.total_sentence_length = 0.0
		lengths = []
		self.scores = {}
		for s in self.sentences:
			sentence = self.clean(s) # get rid of the shit we don't want
			lengths.append(len(sentence.split())) # keep track of each sentence length so we can find an average later
			s_sum = 0.0 # sum of the frequencies of the words in this sentence
			s_words = 0 # number of words in the sentence
			for s_word in sentence.split():
				try: # the word may be 'the' or 'and' or something not in the dictionary
					if self.uselemmat:
						s_sum += self.wfreq[lmtz(s_word, _wnl)]
					else:
						s_sum += self.wfreq[s_word]
				except: pass 
				s_words += 1
			if s_words == 0:
				self.scores[s] = 0
			else:
				self.scores[s] = s_sum/s_words # sentence score is normalized by length
		
		""" GET THE AVERAGE SENTENCE LENGTH """
		self.av_length = sum(lengths)/len(lengths)
		
		""" MODIFY SENTENCE SCORES BASED ON LENGTH """
		for sentence in self.sentences:
			length = len(self.clean(sentence).split())
			if self.radical_mod_method == True:
				try:
					self.scores[sentence] *= length/self.av_length # this favors longer self.sentences
				except: pass
			else:
				if length < self.av_length/1.5: # punish short self.sentences
					try:
						self.scores[sentence] = float(self.scores[sentence])/3
					except: pass
				elif length > self.av_length*1.5: # reward longer self.sentences
					try:
						self.scores[sentence] = self.scores[sentence]*3
					except: pass
		
		""" SORT THE SENTENCES BY SCORE """
		self.sorted_sentences = sorted(self.scores.keys(), key=lambda k: self.scores[k], reverse=True)
		self.highest_s_score = self.scores[self.sorted_sentences[0]]
		
		""" SORT WORDS BY SCORE (FREQUENCY) """
		self.sorted_words = sorted(self.wfreq.keys(), key=lambda key: self.wfreq[key], reverse=True)
		self.highest_w_score = self.wfreq[self.sorted_words[0]]
	
	def get_results(self, result_type, num_results=15):
		# hex color changing functions stolen from http://thadeusb.com/weblog/2010/10/10/python_scale_hex_color
		# for use in the highlighting section
		def clamp(val, minimum=0, maximum=255):
			if val < minimum:
				return minimum
			if val > maximum:
				return maximum
			return val
		def colorscale(hexstr, scalefactor):
			"""
			Scales a hex string by ``scalefactor``. Returns scaled hex string.
			To darken the color, use a float value between 0 and 1.
			To brighten the color, use a float value greater than 1.
			>>> colorscale("#4F75D2", 1)
			"""
			hexstr = hexstr.strip('#')
			if scalefactor < 0 or len(hexstr) != 6:
				return hexstr
			r, g, b = int(hexstr[:2], 16), int(hexstr[2:4], 16), int(hexstr[4:], 16)
			r = clamp(r * scalefactor)
			g = clamp(g * scalefactor)
			b = clamp(b * scalefactor)
			return "#%02x%02x%02x" % (r, g, b)
			
		if num_results < 1: # if num_results is < 1, then it is a percentage
			num_results = num_results*len(self.sorted_sentences)
		if num_results < 1: # if num_results is STILL < 1, then we just have a really short input text.
			num_results = 1 	# we should be nice, and give back at least something
		if num_results > len(self.sorted_sentences): # at most, return all of our sentences, but no more!
			num_results = len(self.sorted_sentences)
		
		self.individ_list = self.sorted_sentences[0:int(num_results)] # create a list of the first num_results sentences
		if result_type == "paragraph":
			self.paragraph = " ".join(self.individ_list)
			return self.paragraph
		elif result_type == "individual":
			self.paragraph = "<br><br>".join(self.individ_list)
			return self.paragraph
		elif result_type == "frequency":
			self.individ_freq_list = [] # add information to the first num_results sentences and put them in a list
			for i, sentence in enumerate(self.individ_list):
				self.individ_freq_list.append("%d (%f): %s" % (i+1, float(self.scores[sentence])/self.highest_s_score, sentence))
			return "<br><br>".join(self.individ_freq_list)
		elif result_type == "highlight":
			self.highlight = self.sentences
			for sentence in self.sorted_sentences:
				score = self.scores[sentence]/self.highest_s_score # this is the relative score!
				score *= score # try making the highlighting better looking by making the differences between scores larger
				color = self.darkest
				if score != 0:
					factor = 1.0/score
					color = colorscale(color, factor).upper()
				else:
					color = "#FFFFFF"
				self.highlight.insert(self.highlight.index(sentence), '<div class="highlight" style="background-color:%s;">' % color)
				self.highlight.insert(self.highlight.index(sentence)+1, '</div><div></div>')
		
			self.highlight = " ".join(self.highlight) # recompile the list back into a paragraph form
			self.highlight = re.sub(r'\n', '<br>', self.highlight) # correct newlines
			self.highlight = re.sub(r'\r', '', self.highlight) # get rid of carriage returns
			self.highlight = re.sub(r'\t', '&nbsp;'*4, self.highlight) # try to substitute for spaces
			return self.highlight
		else:
			return None
