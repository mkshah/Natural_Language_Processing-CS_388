import sys

if __name__ == '__main__':
	inputfilename = sys.argv[1]
	outputtrainfilename = sys.argv[2]
	no = int(sys.argv[3])
	
	inputfile = open(inputfilename, "r") 
	train_sent = ""
	cnt=0
	for sentence in inputfile:
		if(len(sentence)==1):
			cnt = cnt + 1
		if(cnt<no):
			train_sent += sentence
		else:
			break
	train_sent += "\n"
	inputfile.close()
	
	outputtrainfile = open(outputtrainfilename, "a+")
	outputtrainfile.write(train_sent)
	outputtrainfile.close()
	