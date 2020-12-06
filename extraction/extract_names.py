from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import os,codecs

def  main(st,bio_dir,name_path):
	names = []
	for i in range(len(os.listdir(bio_dir))-1):
		with codecs.open(os.path.join(bio_dir,str(i)+'.txt'),'r',encoding='utf-8',errors='ignore') as f:
			
 			text = f.read()
		tokenized_text = word_tokenize(text)
		classified_text = st.tag(tokenized_text)
		found_name = False
		name = ''
		for tup in classified_text:
			if found_name:
				if tup[1] == 'PERSON':
					name += ' '+tup[0].title()
				else:
					break
			elif tup[1] == 'PERSON':
				name += tup[0].title()
				found_name = True
		names.append(name)
		print(i,name)

	with open(name_path,'w') as f:
		for name in names[:-1]:
			f.write(name)
			f.write('\n')
		f.write(names[-1])



if __name__ == '__main__':
	st = StanfordNERTagger('../stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',
					   '../stanford-ner-2018-10-16/stanford-ner.jar',
					   encoding='utf-8')
	bio_dir = os.path.dirname(os.path.realpath(__file__)) + '../data/compiled_bios/'
	name_path = os.path.dirname(os.path.realpath(__file__)) + '../data/names.txt'
	main(st,bio_dir,name_path)

