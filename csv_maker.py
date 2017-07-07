import json
from sys import argv


def All(js): 
	s = []
	s.append(js.get('handle', '-'))
	s.append(js.get('maxRating', '-'))
	s.append(js.get('rating', '-'))
	s.append(js.get('country', '-'))
	s.append(js.get('organization', '-'))
	s.append(js.get('email', '-'))
	s.append(js.get('friendOfCount'))
	s = map(lambda x: str(x), s)
	return '\t'.join(s)

def User(js):
	return js.get('handle', '-')

def main():
	if len(argv) != 3:
		print("not enough arguments...")
		exit(1)

	_, file, typ = argv
	if file == "":
		print("Enter file name...")
		exit()

	txt = open(file).read()
	js = json.loads(txt)["result"]

	if typ == "--all" or typ == "":
		print('handle\tmaxRating\trating\tcountry\torganization\temail\tfriendOfCount')
		for user in js:
			print(All(user))
	elif typ == "--handle":
		for user in js:
			print(User(user))

main()
