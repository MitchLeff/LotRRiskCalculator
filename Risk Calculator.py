import random

RUNS = 100000
PRINT_COMBATS = False

ATTACKER_HAS_GENERAL = True
DEFENDER_HAS_GENERAL = True
DEFENDER_HAS_STRONGHOLD = True


def rollD6():
	return random.randint(1,6)

def combat(attacker, defender):
	attackerWins = 0
	defenderWins = 0

	attacker.rollAttacks()
	defender.rollDefense()
	
	a1 = max(attacker.rolls)
	a2 = min(attacker.rolls)
	
	d1 = max(defender.rolls)
	d2 = min(defender.rolls)

	
	if a1 > d1:
		attackerWins += 1
	else: 
		defenderWins += 1
	
	if a2 > d2:
		attackerWins += 1
	else:
		defenderWins += 1

	if PRINT_COMBATS:
		print("Attacker: " + str(a1) + ", " + str(a2))
		print("Defender: " + str(d1) + ", " + str(d2))
		print("Outcome: " + str(attackerWins) + " - " + str(defenderWins) + "\n")
	
	return [attackerWins, defenderWins]
	
class Attacker:
	def __init__(self, hasGeneral):
		self.rolls = []
		self.hasGeneral = hasGeneral
	
	def rollAttacks(self):
		self.rolls = []
		for i in range(0,3):
			self.rolls.append(rollD6())
		
		self.rolls.remove(min(self.rolls))
		
		self.rolls.sort()
		
		if self.hasGeneral:
			self.rolls[1] = self.rolls[1] + 1
		
		return self.rolls

class Defender:
	def __init__(self, hasGeneral, hasStronghold):
		self.rolls = []
		self.hasGeneral = hasGeneral
		self.hasStronghold = hasStronghold

	def rollDefense(self):
		self.rolls = []
		for i in range(0,2):
			self.rolls.append(rollD6())
		
		self.rolls.sort()
		
		if self.hasGeneral:
			self.rolls[1] = self.rolls[1] + 1
		
		if self.hasStronghold:
			self.rolls[1] = self.rolls[1] + 1
			
		return self.rolls

myAttacker = Attacker(ATTACKER_HAS_GENERAL)
myDefender = Defender(DEFENDER_HAS_GENERAL, DEFENDER_HAS_STRONGHOLD)

attacker_2_0_count = 0
one_and_one_count = 0
defender_2_0_count = 0

for i in range(0,RUNS):
	outcome = combat(myAttacker, myDefender)
	if outcome[0] > outcome[1]:
		attacker_2_0_count += 1
	elif outcome[0] < outcome[1]:
		defender_2_0_count += 1
	else:
		one_and_one_count += 1

attacker_2_0_percentage = float(attacker_2_0_count) / RUNS
defender_2_0_percentage = float(defender_2_0_count) / RUNS
one_and_one_percentage = float(one_and_one_count) / RUNS
		
print("Attacker_2_0_count: " + str(attacker_2_0_count) + ", " + str(attacker_2_0_percentage * 100) + "%")
print("Defender_2_0_count: " + str(defender_2_0_count) + ", " + str(defender_2_0_percentage * 100) + "%")
print("One_and_One_count: " + str(one_and_one_count) + ", " + str(one_and_one_percentage * 100) + "%")