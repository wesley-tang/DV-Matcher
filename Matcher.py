import csv
import random 
import re

nameInd = 1
tagStart = 10
tagEnd = 25
recPrefInd = 27
recPref2Ind = 29

def createMatchups():
	# Open the tsv file for reading
	with open('2022 - DVSS Responses - Registration.csv') as tsvin:
		# 0: Artist name, 1: Recipient Page, 2: Recipient name
		#3: Recipient References
		csvin = csv.reader(tsvin, delimiter=',')

		nameInd = 1
		tagStart = 10
		tagEnd = 25
		recPrefInd = 27
		recPref2Ind = 29

		matched = []

		matchups = []
		matchupsDbg = []

		values = []

		# for each person
		for row in csvin:
			values.append(row)

		firstRow = values.pop(0)[tagStart:tagEnd+1]

		remainingRecips = values.copy()

		for row in values:
			print("Matching: " + row[nameInd])

			candidates = remainingRecips.copy()

			useSecondaryDrawPrefs = False
			useSecondaryRecPref = False
			idealMatchings = True

			while True:
				# What happens if we ran out of candidates to match
				if len(candidates) == 0:
					candidates = remainingRecips.copy()
					if idealMatchings:
						print("Dropping Ideal Matchings")
						idealMatchings = False
					elif not useSecondaryDrawPrefs:
						print("Using secondary Draw Pref")
						idealMatchings = True
						useSecondaryDrawPrefs = True
					elif not useSecondaryRecPref:
						useSecondaryRecPref = True
					else:
						print("All possible candidates exhausted. Matchup Failed.")
						tsvin.close()
						return False
						

				# Choose person who is not matched
				candidateRow = random.randint(0, len(candidates)-1)

				if candidates[candidateRow][nameInd] in matched or row[nameInd] == candidates[candidateRow][nameInd]:
					del candidates[candidateRow]
					continue

				print("Candidate: " + candidates[candidateRow][nameInd])

				# Choose person with appropriate preferences
				santaPref = generatePrefArray(row[tagStart:tagEnd+1], "Highly Want", firstRow)
				santaAvoidDraw = generatePrefArray(row[tagStart:tagEnd+1], "Do NOT Want", firstRow)

				if useSecondaryDrawPrefs:
					santaPref = santaPref + generatePrefArray(row[tagStart:tagEnd+1], "Willing to Draw", firstRow)

				recipPref = candidates[candidateRow][recPrefInd].split(", ")

				if useSecondaryRecPref:
					recipPref = recipPref + candidates[candidateRow][recPref2Ind].split(", ")

				# Find a matchup by seeing what the draw pref and receive pref have in common
				matchingPrefs = list(set(santaPref) & set(recipPref))

				minMatchingPrefs = min(len(santaPref), len(recipPref))

				if idealMatchings and minMatchingPrefs > 1:
					minMatchingPrefs -= 1
				else:
					minMatchingPrefs = 1

				if len(matchingPrefs) < minMatchingPrefs:
					del candidates[candidateRow]
					continue

				# Create a matchup
				matchups.append((row[nameInd], candidates[candidateRow][nameInd], matchingPrefs))
				matchupsDbg.append((row[nameInd], candidates[candidateRow][nameInd], santaPref, recipPref, str(len(matchingPrefs)) + "/" + str(min(len(santaPref), len(recipPref)))))
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
				f.write(str(match[0]) + "\t" + str(match[2]) + "\t" + str(match[1]) + "\t" + str(match[3]) + "\t" + match[4] + "\n")
			f.close()

		return True

def generatePrefArray(tagData, level, firstRow):
	prefDraw = []
	for n in range(len(tagData)):
		if tagData[n] == level:
			prefDraw.append(re.search(r"\[(.*)\]",firstRow[n]).group(1))
	return prefDraw
		
while not createMatchups():
	createMatchups()

print('Done!')
