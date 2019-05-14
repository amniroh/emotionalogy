from __future__ import unicode_literals
from hazm import *

from collections import defaultdict

normalizer = Normalizer()
stemmer = Stemmer()
lemmatizer = Lemmatizer()

def doc_word_freq(doc):
	word_count = defaultdict(lambda :0)
	for sent in sent_tokenize(doc):
		for word in word_tokenize(sent):
			word = lemmatizer.lemmatize(
				stemmer.stem(word)
			)
			word_count[word] += 1
	return word_count

def load_lexicon(filepath='nrc_persian.txt'):
	dict = defaultdict(set)
	with open(filepath, 'r') as f:
		for line in f:
			try:
				word, emotion, is_true = line.strip().split('\t')
				if is_true == '1':
					dict[word].add(emotion)
			except:
				continue
	return dict

def emotion_scorer(doc, emotion_dict):
	emotions = defaultdict(lambda : 0)
	for word in doc:
		if word in emotion_dict:
			for emotion in emotion_dict[word]:
				emotions[emotion] += doc[word]
	return emotions

dict = load_lexicon()

with open('test.txt', 'r') as f:
	s = f.read()
	temp = doc_word_freq(s)

print(emotion_scorer(temp, dict))

# write a processed dictionary
#with open('processed_nrc.txt', 'w') as f:
#	for key in list(dict.keys()):
#		f.write(key)
#		f.write(': ')
#		f.write(str(dict[key]))
#		f.write('\n')



#
## tagger = POSTagger(model='resources/postagger.model')
## tagger.tag(word_tokenize(sent)
## tree2brackets(chunker.parse(tagged))
## parser = DependencyParser(tagger=tagger, lemmatizer=lemmatizer)
## parser.parse(word_tokenize(sent))
