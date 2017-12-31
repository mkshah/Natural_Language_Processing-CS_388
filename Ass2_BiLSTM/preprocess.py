import glob
from random import shuffle
from pyparsing import StringEnd, oneOf, FollowedBy, Optional, ZeroOrMore, SkipTo

MAX_LENGTH = 100

class PreprocessData:

	def __init__(self, dataset_type='wsj'):
		self.vocabulary = {}
		self.pos_tags = {}
		self.dataset_type = dataset_type
		
		# Prefix Dictionary
		self.preix_dict = {"anti":1, "de":2, "dis":3, "en":4, "em":4, "fore":5, "in":6, "im":6, "il":6, "ir":6, "inter":7, "mid":8, "mis":9, "non":10, "over":11, "pre":12, "re":13, "semi":14, "sub":15, "super":16, "trans":17, "un":18, "under":19}
		# Suffix Dictionary
		self.suffix_dict = {"able":1, "ible":1, "al":2, "ial":2, "ed":3, "en":4, "er":5, "est":6, "ful":7, "ic":8, "ing":9, "ion":10, "tion":10, "ation":10, "ition":10, "ity":11, "ty":11, "ive":12, "ative":12, "itive":12, "less":13, "ly":14, "ment":15, "mess":16, "ous":17, "eous":17, "ious":17, "s":18, "es":18, "y":19}
		
		# Regular Expression for Parsing Word
		self.endOfString = StringEnd()
		self.prefix = oneOf("anti de dis en em fore in im il ir inter mid mis non over pre re semi sub super trans un under")
		self.suffix = oneOf("able ible al ial ed en er est ful ic ing ion tion ation ition ity ty ive ative itive less ly ment mess ous eous ious s es y") + FollowedBy(self.endOfString)		
		self.word = (ZeroOrMore(self.prefix)("prefixes") + SkipTo(self.suffix | self.endOfString)("root") +  Optional(self.suffix)("suffix"))

	## Get standard split for WSJ
	def get_standard_split(self, files):
		if self.dataset_type == 'wsj':
			train_files = []
			val_files = []
			test_files = []
			for file_ in files:
				partition = int(file_.split('/')[-2])
				if partition >= 0 and partition <= 18:
					train_files.append(file_)
				elif partition <= 21:
					val_files.append(file_)
				else:
					test_files.append(file_)
			return train_files, val_files, test_files
		else:
			raise Exception('Standard Split not Implemented for '+ self.dataset_type)

	@staticmethod
	def isFeasibleStartingCharacter(c):
		unfeasibleChars = '[]@\n'
		return not(c in unfeasibleChars)

	## unknown words represented by len(vocab)
	def get_unk_id(self, dic):
		return len(dic)

	def get_pad_id(self, dic):
		return len(self.vocabulary) + 1

	## get id of given token(pos) from dictionary dic.
	## if not in dic, extend the dic if in train mode
	## else use representation for unknown token
	def get_id(self, pos, dic, mode):
		if pos not in dic:
			if mode == 'train':
				dic[pos] = len(dic)
			else:
				return self.get_unk_id(dic)
		return dic[pos]

	## Process single file to get raw data matrix
	def processSingleFile(self, inFileName, mode):
		matrix = []
		row = []
		with open(inFileName) as f:
			lines = f.readlines()
			for line in lines:
				line = line.strip()
				if line == '':
					pass
				else:
					tokens = line.split()
					for token in tokens:
						## ==== indicates start of new example					
						if token[0] == '=':
							if row:
								matrix.append(row)
							row = []
							break
						elif PreprocessData.isFeasibleStartingCharacter(token[0]):
							wordPosPair = token.split('/')
							if len(wordPosPair) == 2:
								## get ids for word and pos tag
								feature = self.get_id(wordPosPair[0], self.vocabulary, mode)
								# parse the word - prefix,root,suffix
								res = self.word.parseString(wordPosPair[0])
								# if there is prefix, fetch its id, otherwise assign id 0
								if(len(res.prefixes)>0):
									pre = self.preix_dict.get(res.prefixes[0])
								else:
									pre = 0
								# if there is suffix, fetch its id, otherwise assign id 0
								if(len(res.suffix)>0):
									suf = self.suffix_dict.get(res.suffix[0])
								else:
									suf = 0
								# include all pos tags.
								row.append((feature, pre, suf, self.get_id(wordPosPair[1],
											self.pos_tags, 'train')))
		if row:
			matrix.append(row)
		return matrix


	## get all data files in given subdirectories of given directory
	def preProcessDirectory(self, inDirectoryName, subDirNames=['*']):
		if not(subDirNames):
			files = glob.glob(inDirectoryName+'/*.pos')
		else:
			files = [glob.glob(inDirectoryName+ '/' + subDirName + '/*.pos')
					for subDirName in subDirNames]
			files = set().union(*files)
		return list(files)


	## Get basic data matrix with (possibly) variable sized senteces, without padding
	def get_raw_data(self, files, mode):
		matrix = []
		for f in files:
			matrix.extend(self.processSingleFile(f, mode))
		return matrix

	def split_data(self, data, fraction):
		split_index = int(fraction*len(data))
		left_split = data[:split_index]
		right_split = data[split_index:]
		if not(left_split):
			raise Exception('Fraction too small')
		if not(right_split):
			raise Exception('Fraction too big')
		return left_split, right_split

	## Get rid of sentences greater than max_size
	## and pad the remaining if less than max_size
	def get_processed_data(self, mat, max_size):
	# Perform same processing for prefix and suffix vectors also 
		X = []
		p = []
		s = []
		y = []
		original_len = len(mat)
		mat = filter(lambda x: len(x) <= max_size, mat)
		no_removed = original_len - len(mat)
		for row in mat:
			X_row = [tup[0] for tup in row]
			p_row = [tup[1] for tup in row]
			s_row = [tup[2] for tup in row]
			y_row = [tup[3] for tup in row]
			## padded words represented by len(vocab) + 1
			X_row = X_row + [self.get_pad_id(self.vocabulary)]*(max_size - len(X_row))
			## Padded pos tags represented by -1
			p_row = p_row + [-1]*(max_size-len(p_row))
			s_row = s_row + [-1]*(max_size-len(s_row))
			y_row = y_row + [-1]*(max_size-len(y_row))
			X.append(X_row)
			p.append(p_row)
			s.append(s_row)
			y.append(y_row)
		# return all 4 processed vectors	
		return X, p, s, y, no_removed
