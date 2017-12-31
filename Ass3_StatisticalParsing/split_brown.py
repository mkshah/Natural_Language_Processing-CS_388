import sys

if __name__ == '__main__':
	inputfilename = sys.argv[1]
	outputtrainfilename = sys.argv[2]
	outputtestfilename = sys.argv[3]
	
	inputfile = open(inputfilename, "r") 
	cnt = 0
	for sentence in inputfile:
		if(len(sentence)==1):
			cnt = cnt + 1
	no_sent = cnt
	no_train_sent = 0.9 * no_sent;
	cnt = 0
	train_sent = ""
	test_sent = ""
	inputfile.seek(0)
	skip_first_line = 1
	for sentence in inputfile:
		if(len(sentence)==1):
			cnt = cnt + 1
		if(cnt<no_train_sent+1):
			train_sent += sentence
		else:
			if(skip_first_line==1):
				skip_first_line=0
			else:
				test_sent += sentence
	inputfile.close()
	
	outputtrainfile = open(outputtrainfilename, "a+")
	outputtrainfile.write(train_sent)
	outputtrainfile.close()
	
	outputtestfile = open(outputtestfilename, "a+")
	outputtestfile.write(test_sent)
	outputtestfile.close()