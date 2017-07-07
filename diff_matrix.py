import json
import math

def readFile(file):
	f = open(file)
	s = f.read()
	f.close()
	return s

def readCsv(file):
	s = readFile(file).strip()
	ary = s.split('\n')
	for i in range(len(ary)):
		ary[i] = ary[i].strip().split('\t')
	return ary

def Max(arg, table):
	mx = -1
	for t in table:
		if int(t[arg]) > mx:
			mx = int(t[arg])
	return mx

def Out(*args):
	args = map(str, args)
	print('\t'.join(args))

abs = lambda x: x if x > 0 else -x

def main():
	db = readCsv('maindb.csv')
	db = db[1:]
	#print(db)

	length = len(db)
	maxRegister = Max(1, db)
	maxRate = Max(5, db)

	maxAccept = Max(6, db)
	maxWrong = Max(7, db)

	Out('firsrt', 'second', 'diff')
	for a in range(len(db)):
		for b in range(a, len(db)):
			diff = 0
			diff += abs(int(db[a][1]) - int(db[b][1])) / maxRegister
			diff += (0 if db[a][2] == db[b][2] else 1) * (0 if db[a][2] == '-' or db[b][2] == '-' else 1)
			diff += (0 if db[a][3] == db[b][3] else 1) * (0 if db[a][3] == '-' or db[b][3] == '-' else 1)
			diff += 0 if db[a][4] == db[b][4] else 1
			diff += 3 * abs(int(db[a][5]) - int(db[b][5])) / maxRate

			diff += 1 - ((int(db[a][6]) * int(db[b][6]) + int(db[a][7]) * int(db[b][7])) / (math.sqrt(int(db[a][6]) ** 2 + int(db[a][7]) ** 2) * math.sqrt(int(db[b][6]) ** 2 + int(db[b][7]) ** 2)))

			count = 8
			count -= 1 if db[a][2] == '-' or db[b][2] == '-' else 0
			count -= 1 if db[a][3] == '-' or db[b][3] == '-' else 0
			diff /= count

			Out(a + 1, b + 1, diff)

main()