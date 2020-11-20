import csv
import random 

def createMatchups():
	# Open the tsv file for reading
	with open('2020_Secret_Santa_Form_Responses_-_OfficialReg.csv') as tsvin:
		# 0: Artist name, 1: Recipient Page, 2: Recipient name
		#3: Recipient References
		csvin = csv.reader(tsvin, delimiter=',')

		nameInd = 1
		avoidMatchInd = 6
		drawPrefInd = 7
		drawPref2Ind = 8
		avoidDrawInd = 9
		recPrefInd = 11
		recPref2Ind = 13

		matched = []

		matchups = []
		matchupsDbg = []

		values = []

		# for each person
		for row in csvin:
			values.append(row)

		values.pop(0)

		remainingRecips = values.copy()

		for row in values:
			print("Matching: " + row[nameInd])



			candidates = remainingRecips.copy()

			useSecondaryDrawPrefs = False
			useSecondaryRecPref = False

			while True:
				# What happens if we ran out of candidates to match
				if len(candidates) == 0:
					candidates = remainingRecips.copy()
					if not useSecondaryDrawPrefs:
						print("Using secondary Draw Pref")
						useSecondaryDrawPrefs = True
					elif not useSecondaryRecPref:
						useSecondaryRecPref = True
					else:
						print("All possible candidates exhausted. Matchup Failed.")
						tsvin.close()
						return False
						

				# Choose person who is not matched
				candidateRow = random.randint(0, len(candidates)-1)

				if candidates[candidateRow][nameInd] in matched or candidates[candidateRow][nameInd] == row[avoidMatchInd] or row[nameInd] == candidates[candidateRow][nameInd]:
					del candidates[candidateRow]
					continue

				print("Candidate: " + candidates[candidateRow][nameInd])


				# Choose person with appropriate preferences
				santaPref = row[drawPrefInd].split(", ")
				santaAvoidDraw = row[avoidDrawInd].split(", ")

				if useSecondaryDrawPrefs:
					santaPref = santaPref + row[drawPref2Ind].split(", ")

				recipPref = candidates[candidateRow][recPrefInd].split(", ")

				if useSecondaryRecPref:
					recipPref = recipPref + candidates[candidateRow][recPref2Ind].split(", ")

				avoidDrawCheck = list(set(santaAvoidDraw) & set(recipPref))

				# Don't match if they have any forbidden values
				if len(avoidDrawCheck) > 0:
					del candidates[candidateRow]
					continue

				matchingPrefs = list(set(santaPref) & set(recipPref))

				minMatchingPrefs = 2
				# Don't match unless they have at least 2 things in common, unless there preference lists are short
				if len(santaPref) < 2 or len (recipPref) < 2:
					minMatchingPrefs = 1

				if len(matchingPrefs) < minMatchingPrefs:
					del candidates[candidateRow]
					continue

				# Create a matchup
				matchups.append((row[nameInd], candidates[candidateRow][nameInd], matchingPrefs))
				matchupsDbg.append((row[nameInd], candidates[candidateRow][nameInd], santaPref, recipPref))
				remainingRecips.remove(candidates[candidateRow])
				matched.append(candidates[candidateRow][nameInd])
				print((row[nameInd], candidates[candidateRow][nameInd], matchingPrefs))
				break

		with open('matchups.txt', 'w+') as f:
			for match in matchups:
				f.write(str(match[0]) + " > " + str(match[1]) + "\t(" + str(match[2]) + ")\n")
			f.close()

		with open('matchupsDebug.tsv', 'w+') as f:
			for match in matchupsDbg:
				f.write(str(match[0]) + "\t" + str(match[2]) + "\t" + str(match[1]) + "\t" + str(match[3]) + "\n")
			f.close()

		return True

while not createMatchups():
	createMatchups()

print('Done!')
