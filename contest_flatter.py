import json
import time
import os

def readFile(file):
	f = open(file)
	s = f.read()
	f.close()
	return s


def readInfo(handle):
	return readFile('user_info/' + handle + '.info.json')

def readSubmition(handle):
	return readFile('user_submition/' + handle + '.submition.json')

def readRating(handle):
	return readFile('user_rating/' + handle + '.rating.json')

def sh(cmd):
	os.system(cmd)

def Out(handle, *arg):
	s = ""
	for a in arg:
		s += str(a) + '\t'

	sh('echo "%s" >> %s' % (s, 'rated_submition/' + handle + '.csv'))


def findContestTime(contestId, contestList):
	for contest in contestList:
		#print(contest['id'])
		if int(contestId) == int(contest['id']):
			return int(contest['startTimeSeconds'])
	return 0



def main():
	
	users = readFile('readed.csv')
	users = users.split('\n')

	contestList = readFile('contest.list.json')
	contestList = json.loads(contestList)['result']

	for handle in users:
		if handle == '':
			continue

		Out(handle, 'oldRating', 'newRating', 'A', 'B', 'C', 'D', 'EaU')
		rating = json.loads(readRating(handle))['result']
		submition = json.loads(readSubmition(handle))['result']
		submition.reverse()

		indxSub = 0

		A = 0
		B = 0
		C = 0
		D = 0
		EaU = 0

		for contest in rating:

			contestId = contest['contestId']

			startTime = int(findContestTime(contestId, contestList))

			oldRating = contest['oldRating']
			newRating = contest['newRating']

			while int(submition[indxSub]['creationTimeSeconds']) < startTime:
				if submition[indxSub]['verdict'] == 'OK':
					if submition[indxSub]['problem']['index'] == 'A':
						A += 1
					elif submition[indxSub]['problem']['index'] == 'B':
						B += 1
					elif submition[indxSub]['problem']['index'] == 'C':
						C += 1
					elif submition[indxSub]['problem']['index'] == 'D':
						D += 1
					else:
						EaU += 1

				indxSub += 1

			Out(handle, oldRating, newRating, A, B, C, D, EaU)

main()