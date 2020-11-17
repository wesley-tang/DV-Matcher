import csv
import random 

# Open the tsv file for reading
with open('2020_Secret_Santa_Form_Responses_-_OfficialReg.csv') as tsvin:
	# 0: Artist name, 1: Recipient Page, 2: Recipient name
	#3: Recipient References
	csvin = csv.reader(tsvin, delimiter=',')

	nameInd = 1
	avoidMatchInd = 6
	drawPrefInd = 7
	avoidDrawInd = 9
	recPrefInd = 11

	matched = []

	matchups = []

	values = []

	# for each person
	for row in csvin:
		values.append(row)

	values.pop(0)

	for row in values:
		candidateRow = -1

		print("Matching: " + row[nameInd])

		candidates = values.copy()

		while True:
			if len(candidates) == 0:
				print("FAILURE")
				break

			# Choose person who is not matched
			candidateRow = random.randint(0, len(candidates)-1)

			if candidateRow in matched or candidates[candidateRow][nameInd] == row[avoidMatchInd] or row[nameInd] == candidates[candidateRow][nameInd]:
				del candidates[candidateRow]
				continue

			print("Candidate: " + candidates[candidateRow][nameInd])


			# Choose person with appropriate preferences
			santaPref = row[drawPrefInd].split(", ")
			santaAvoidDraw = row[avoidDrawInd].split(", ")

			recipPref = candidates[candidateRow][recPrefInd].split(", ")

			avoidDrawCheck = list(set(santaAvoidDraw) & set(recipPref))

			# Don't match if they have any forbidden values
			if len(avoidDrawCheck) > 0:
				del candidates[candidateRow]
				continue

			matchingPrefs = list(set(santaPref) & set(recipPref))

			# Don't match unless they have at least 2 things in common
			if len(matchingPrefs) < 2:
				del candidates[candidateRow]
				continue

			# Create a matchup
			matchups.append((row[nameInd], candidates[candidateRow][nameInd], matchingPrefs))
			print((row[nameInd], candidates[candidateRow][nameInd], matchingPrefs))
			break

	with open('matchups.csv', 'w+') as f:
		for match in matchups:
			f.write(str(match[0]) + " > " + str(match[1]) + "\t(" + str(match[2]) + ")\n")
		f.close()

print('Done!')
