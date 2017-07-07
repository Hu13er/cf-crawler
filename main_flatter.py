import json
import time
import math

def readFile(file):
	f = open(file)
	s = f.read()
	f.close()
	return s

def readInfo(handle):
	return readFile('user_info/' + handle + '.info.json')

def readSubmition(handle):
	return readFile('user_submition/' + handle + '.submition.json')

def LanguageFamily(name):
	name = name.upper()
	if name.find("C++") >= 0:
		return "C++"
	if name.find("JAVA") >= 0:
		return "Java"
	if name.find("C#") >= 0:
		return "C#"
	if name.find("PYTHON") >= 0:
		return "Python"
	return "Other"


def Out(*arg):
	s = ""
	for a in arg:
		s += str(a) + '\t'
	print(s)


def main():
	users = readFile('readed.csv')
	users = users.split('\n')

	Out('handle', 'registrationTime', 'country', 'organ', 'language', 'rating', 'Accepted', 'Wrong')
	for handle in users:
		if handle == '':
			continue

		info = json.loads(readInfo(handle))['result'][0]

		country = info.get('country', '-')
		rating = info.get('rating', '-')
		organ = info.get('organization', '-')

		submition = json.loads(readSubmition(handle))['result']

		langs = {}
		Accepted = 0
		Wrong = 0
		for s in submition:
			l = s['programmingLanguage']
			langs[l] = langs.get(l, 0) + 1
			if s['testset'] == 'PRETESTS':
				continue

			if s['verdict'] == 'OK':
				Accepted += 1
			else:
				Wrong += 1

		mx = -1
		language = ''
		for l in langs:
			if mx < langs[l]:
				mx = langs[l]
				language = LanguageFamily(l)

		registrationTime = round((time.time() - int(info.get('registrationTimeSeconds', 0))) / (3600 * 24 * 365))


		Out(handle, registrationTime, country, organ, language, rating, Accepted, Wrong)
		
main()
