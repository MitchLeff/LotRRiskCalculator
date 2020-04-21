#"It's actually pretty simple, do you have a whiteboard?" -My Incorrect Friend

import random

#Parameters for simulator
RUNS = 1000000					#Number of simulated combats to be performed
PRINT_COMBATS = False			#Flag to display each combat result

#Parameters for number of attackers and defenders
ATTACKING_DICE = 2				#Number of dice attacking (1-3)
DEFENDING_DICE = 1				#Number of dice defending (1-2)

#Dice number options to iterate through
Attacker_Dice_Options = [1,2,3]
Defender_Dice_Options = [1,2]

#Flags for traversing truth table options
Flag_Options = [True, False]

#Parameters for bonuses
ATTACKER_HAS_Leader = False
DEFENDER_HAS_Leader = False
DEFENDER_HAS_STRONGHOLD = False


#Function to roll 1 six sided die
def rollD6():
	return random.randint(1,6)


#Function to determine the outcome of combat
def combat(attacker, defender):
	#Counters for high and low dice wins
	attackerWins = 0
	defenderWins = 0

	#Roll each player's combat
	attacker.rollAttacks()
	defender.rollDefense()
	
	#Select high and low dice for attacker
	a1 = max(attacker.rolls)
	a2 = min(attacker.rolls)
	
	#Select high and low dice for defender
	d1 = max(defender.rolls)
	d2 = min(defender.rolls)

	#Determine high dice outcome
	if a1 > d1:
		attackerWins += 1
	else: 
		defenderWins += 1
	
	if attacker.numDice > 1 and defender.numDice > 1:	#Only determine low dice outcome if both players are using more than 1 dice
		#Determine low dice outcome
		if a2 > d2:
			attackerWins += 1
		else:
			defenderWins += 1

	#Print combat outcome
	if PRINT_COMBATS:
		if attacker.numDice > 1: 
			print("Attacker: " + str(a1) + ", " + str(a2))
		else:
			print("Attacker: " + str(a1))
		if defender.numDice > 1:
			print("Defender: " + str(d1) + ", " + str(d2))
		else:
			print("Defender: " + str(d1))
		print("Outcome: " + str(attackerWins) + " - " + str(defenderWins) + "\n")
	
	#Return combat outcome
	return [attackerWins, defenderWins]

#Class to represent the attacking player
class Attacker:
	#Initialize the attacker
	def __init__(self, hasLeader, numDice):
		self.rolls = []
		self.hasLeader = hasLeader				#Denotes if the attacker has a Leader while attacking
		self.numDice = numDice					#Number of dice the attacker is using
	
	def rollAttacks(self):
		self.rolls = []							#Reset rolls to empty
		for i in range(0,self.numDice):
			self.rolls.append(rollD6())			#Roll a dice per number of dice chosen to defend
		
		if self.numDice > 2:					#Keep the highest results up to the number of dice being rolled (remove the lowest result if more than 2 dice)
			self.rolls.remove(min(self.rolls))	
		
		self.rolls.sort()						#Sort in ascending order
		
		if self.hasLeader:						#If the attacker has a Leader, add 1 to the highest die
			self.rolls[-1] = self.rolls[-1] + 1	
		
		return self.rolls						#Return the resulting values

#Class to represent the defending player
class Defender:
	def __init__(self, hasLeader, hasStronghold, numDice):
		self.rolls = []
		self.hasLeader = hasLeader			#Denotes if the defender has a Leader while defending
		self.hasStronghold = hasStronghold		#Denotes if the defender has a Stronghold while defending
		self.numDice = numDice					#Number of dice defender is using

	def rollDefense(self):
		self.rolls = []							#Reset rolls to empty
		for i in range(0,self.numDice):
			self.rolls.append(rollD6())			#Roll a dice per number of dice chosen to defend
		
		self.rolls.sort()						#Sort in ascending order
		
		if self.hasLeader:						#If the defender has a Leader, add 1 to the highest die
			self.rolls[-1] = self.rolls[-1] + 1
		
		if self.hasStronghold:					#If the defender has a Stronghold, add 1 to the highest die
			self.rolls[-1] = self.rolls[-1] + 1
			
		return self.rolls						#Return the resulting values


def SimulateCombat(attacker, defender, runs):
	# Initialize results counters
	attacker_wins_count = 0
	defender_wins_count = 0
	one_and_one_count = 0

	# Perform number of simulated combats and count each outcome
	for i in range(0,runs):
		outcome = combat(attacker, defender)
		if outcome[0] > outcome[1]:
			attacker_wins_count += 1
		elif outcome[0] < outcome[1]:
			defender_wins_count += 1
		else:
			one_and_one_count += 1

	# Convert results to a percentage
	attacker_win_percentage = 100 * float(attacker_wins_count) / runs
	defender_win_percentage = 100 * float(defender_wins_count) / runs
	one_and_one_percentage = 100 * float(one_and_one_count) / runs
			
	# Print the results
	print("Attacker_wins_count: " + str(attacker_wins_count) + ", " + str(attacker_win_percentage) + "%")
	print("Defender_wins_count: " + str(defender_wins_count) + ", " + str(defender_win_percentage) + "%")
	print("One_and_One_count: " + str(one_and_one_count) + ", " + str(one_and_one_percentage) + "%\n")
	
	return [attacker_win_percentage, defender_win_percentage, one_and_one_percentage]

# Create attacker and defender objects for combat (Single Instance)
# myAttacker = Attacker(ATTACKER_HAS_Leader, ATTACKING_DICE)
# myDefender = Defender(DEFENDER_HAS_Leader, DEFENDER_HAS_STRONGHOLD, DEFENDING_DICE)

# SimulateCombat(myAttacker, myDefender, RUNS)


# Main loop to traverse each possible arrangement of options
with open("RiskCalcOutcomes.txt", 'w') as f:
	for i in Flag_Options:				#Attacker has a Leader
		for j in Flag_Options:			#Defender has a Leader
			for k in Flag_Options:		#Defender has a Stronghold
				#Write Flag options to file
				f.writelines("Attacker has Leader:\t\t" + str(i) + "\n")
				f.writelines("Defender has Leader:\t\t" + str(j) + "\n")
				f.writelines("Defender has Stronghold:\t" + str(k) + "\n\n")
	
				for l in Attacker_Dice_Options:			#Attacking number of dice (1-3)
					for m in Defender_Dice_Options:		#Defending number of dice (1-2)
						#Create Attacker and Defender objects
						myAttacker = Attacker(i, l)
						myDefender = Defender(j, k, m)
						
						#Collect results from simulated combats
						combat_results = SimulateCombat(myAttacker, myDefender, RUNS)
						
						#Write results to file
						f.writelines(str(l) + " - " +str(m) + "\n")
						f.writelines("Attacker Wins:\t" + str(combat_results[0]) + "%\n")
						f.writelines("Defender Wins:\t" + str(combat_results[1]) + "%\n")
						f.writelines("One and One:\t" + str(combat_results[2])+ "%\n\n")