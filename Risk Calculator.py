import random

RUNS = 1000000
PRINT_COMBATS = False

ATTACKER_HAS_GENERAL = False
DEFENDER_HAS_GENERAL = False
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
	
	#Determine low dice outcome
	if a2 > d2:
		attackerWins += 1
	else:
		defenderWins += 1

	#Print combat outcome
	if PRINT_COMBATS:
		print("Attacker: " + str(a1) + ", " + str(a2))
		print("Defender: " + str(d1) + ", " + str(d2))
		print("Outcome: " + str(attackerWins) + " - " + str(defenderWins) + "\n")
	
	#Return combat outcome
	return [attackerWins, defenderWins]

#Class to represent the attacking player
class Attacker:
	#Initialize the attacker
	def __init__(self, hasGeneral):
		self.rolls = []
		self.hasGeneral = hasGeneral			#Denotes if the attacker has a General while attacking
	
	def rollAttacks(self):
		self.rolls = []							#Reset rolls to empty
		for i in range(0,3):
			self.rolls.append(rollD6())			#Roll 3d6
		
		self.rolls.remove(min(self.rolls))		#Keep the highest 2 results (remove the lowest result)
		
		self.rolls.sort()						#Sort in ascending order
		
		if self.hasGeneral:						#If the attacker has a General, add 1 to the highest die
			self.rolls[1] = self.rolls[1] + 1	
		
		return self.rolls						#Return the resulting values

#Class to represent the defending player
class Defender:
	def __init__(self, hasGeneral, hasStronghold):
		self.rolls = []
		self.hasGeneral = hasGeneral			#Denotes if the defender has a General while defending
		self.hasStronghold = hasStronghold		#Denotes if the defender has a Stronghold while defending

	def rollDefense(self):
		self.rolls = []							#Reset rolls to empty
		for i in range(0,2):
			self.rolls.append(rollD6())			#Roll 2d6
		
		self.rolls.sort()						#Sort in ascending order
		
		if self.hasGeneral:						#If the defender has a General, add 1 to the highest die
			self.rolls[1] = self.rolls[1] + 1
		
		if self.hasStronghold:					#If the defender has a Stronghold, add 1 to the highest die
			self.rolls[1] = self.rolls[1] + 1
			
		return self.rolls						#Return the resulting values

#Create attacker and defender objects
myAttacker = Attacker(ATTACKER_HAS_GENERAL)
myDefender = Defender(DEFENDER_HAS_GENERAL, DEFENDER_HAS_STRONGHOLD)

#Initialize results counters
attacker_2_0_count = 0
one_and_one_count = 0
defender_2_0_count = 0

#Perform number of simulated combats and count each outcome
for i in range(0,RUNS):
	outcome = combat(myAttacker, myDefender)
	if outcome[0] > outcome[1]:
		attacker_2_0_count += 1
	elif outcome[0] < outcome[1]:
		defender_2_0_count += 1
	else:
		one_and_one_count += 1

#Convert results to a percentage
attacker_2_0_percentage = float(attacker_2_0_count) / RUNS
defender_2_0_percentage = float(defender_2_0_count) / RUNS
one_and_one_percentage = float(one_and_one_count) / RUNS
		
#Print the results
print("Attacker_2_0_count: " + str(attacker_2_0_count) + ", " + str(attacker_2_0_percentage * 100) + "%")
print("Defender_2_0_count: " + str(defender_2_0_count) + ", " + str(defender_2_0_percentage * 100) + "%")
print("One_and_One_count: " + str(one_and_one_count) + ", " + str(one_and_one_percentage * 100) + "%")