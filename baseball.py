import random
import time
import math
from datetime import datetime
home_score = 0
away_score = 0
half_inning = 1
balls = 0
strikes = 0
outs = 0
first = False
second = False
third = False
rand = 0
result = "_"
gameover = False

away_strikeout_count = 0
away_walk_count = 0
away_single_count = 0
away_double_count = 0
away_triple_count = 0
away_homerun_count = 0
away_hbp_count = 0

home_strikeout_count = 0
home_walk_count = 0
home_single_count = 0
home_double_count = 0
home_triple_count = 0
home_homerun_count = 0
home_hbp_count = 0

def random_number():
	global rand
	rand = random.randint(1, 100)
	
def resetcount():
	global balls
	global strikes
	balls = 0
	strikes = 0
	
def out():
	global outs
	global half_inning
	global first
	global second
	global third
	global home_score
	global away_score
	global gameover
	global balls
	global strikes
	if outs <=1:
		resetcount()
		outs = outs + 1
	elif outs == 2:
		outs = 3
		if half_inning < 17: #before 9th inning, no win possible
			print ("Half-inning has ended.")
			print("")
			wait()
			half_inning = half_inning + 1
			outs = 0
			first = False
			second = False
			third = False
			balls = 0
			strikes = 0
			
		elif half_inning >= 17: # if 9th inning or later
			#print ("it is the 9th inning or later")
			
			#away_score = 10
			#home_score = 10
			
			if half_inning % 2 != 0: # if end of top of inning
				#print ("it is the end of the top of an inning.")
				if home_score > away_score:
					print("Game has ended. HOME wins.")
					gameover = True
					
				else:
					print ("Half-inning has ended.")
					print("")
					wait()
					half_inning = half_inning + 1
					outs = 0
					first = False
					second = False
					third = False
					balls = 0
					strikes = 0
					
					#pitch()
					
			elif half_inning % 2 == 0: # if end of bottom of inning
				#print ("it is the end of the bottom of an inning.")
				if home_score > away_score:
					print("Game has ended. HOME wins.")
					gameover = True
					
				elif home_score < away_score:
					print("Game has ended. AWAY wins.")
					gameover = True
					
				elif home_score == away_score:
					print ("Half-inning has ended.")
					wait()
					print("")
					half_inning = half_inning + 1
					outs = 0
					first = False
					second = False
					third = False
					balls = 0
					strikes = 0
					return
				return

def grounder():
	global first
	global second
	global third
	if first == False and second == False and third == False:
		print ("GROUND OUT!")
		out()		
	elif first == True and second == False and third == False:
		if outs < 2:
			print ("DOUBLE PLAY!")
			out()
			out()
		else:
			print ("GROUND OUT!")
			out()	
	elif first == False and second == True and third == False:
		print ("GROUND OUT!")
		out()	
	elif first == False and second == False and third == True:
		print ("GROUND OUT!")
		out()
	elif first == True and second == True and third == False:
		if outs == 0:
			print ("TRIPLE PLAY!")
			out()
			out()
			out()
		elif outs == 1:	
			print ("DOUBLE PLAY!")
			out()
			out()
		elif outs == 2:
			print ("GROUND OUT!")
			out()	
	elif first == False and second == True and third == True:
		print ("GROUND OUT!")
		out()
	elif first == True and second == True and third == True:
		if outs == 0:
			print ("TRIPLE PLAY!")
			out()
			out()
			out()
		elif outs == 1:	
			print ("DOUBLE PLAY!")
			out()
			out()
		elif outs == 2:
			print ("GROUND OUT!")
			out()	
	elif first == True and second == False and third == True:
		if outs < 2:
			print ("DOUBLE PLAY!")
			out()
			out()
		else:
			print ("GROUND OUT!")
			out()
	resetcount()
	
def outfieldfly():
	global first
	global second
	global third
	global outs
	if first == False and second == False and third == False:
		#result = "Outfield fly"
		print ("FLY OUT!")
		out()
	elif first == True and second == False and third == False:
		#result = "Outfield fly"
		print ("FLY OUT!")
		out()
	elif first == False and second == True and third == False:
		if outs < 2:
			#result = "Outfield fly"
			print ("FLY OUT! RUNNER ADVANCED.")
			second = False
			third = True
			out()
		else:
			#result = "Outfield fly"
			print ("FLY OUT!")
			out()
	elif first == False and second == False and third == True:
		if outs < 2:
			#result = "Sacrifice fly"
			print ("SACRIFICE FLY!")
			third = False
			out()
			run()
		else:
			#result = "Outfield fly"
			print ("FLY OUT!")
			out()
	elif first == True and second == True and third == False:
		if outs < 2:
			#result = "Outfield fly"
			print ("FLY OUT! RUNNERS ADVANCED.")
			second = False
			third = True
			out()
		else:
			#result = "Outfield fly"
			print ("FLY OUT!")
			out()
	elif first == False and second == True and third == True:
		if outs < 2:
			#result = "Sacrifice fly"
			print ("SACRIFICE FLY!")
			third = False
			out()
			run()
		else:
			#result = "Outfield fly"
			print ("FLY OUT!")
			out()
	elif first == True and second == False and third == True:
		if outs < 2:
			#result = "Sacrifice fly"
			print ("SACRIFICE FLY!")
			third = False
			out()
			run()
		else:
			#result = "Outfield fly"
			print ("FLY OUT!")
			out()
	elif first == True and second == True and third == True:
		if outs < 2:
			#result = "Sacrifice fly"
			print ("SACRIFICE FLY!")
			third = False
			out()
			run()
		else:
			#result = "Outfield fly"
			print ("FLY OUT!")
			out()
	resetcount()
	
def walk():
	global home_walk_count
	global away_walk_count
	global first
	global second
	global third
	if first == False and second == False and third == False:
		first = True
	elif first == True and second == False and third == False:
		second = True
	elif first == False and second == True and third == False:
		first = True
	elif first == False and second == False and third == True:
		first = True
	elif first == True and second == True and third == False:
		third = True
	elif first == False and second == True and third == True:
		first = True
	elif first == True and second == True and third == True:
		run()
	elif first == True and second == False and third == True:
		second = True
	if half_inning % 2 != 0: #if top of inning
		away_walk_count = away_walk_count + 1
	elif half_inning % 2 ==	0: # if bottom of inning
		home_walk_count = home_walk_count + 1
	resetcount()
	
def hit_by_pitch():
	global first
	global second
	global third
	global home_hbp_count
	global away_hbp_count
	if first == False and second == False and third == False:
		first = True
	elif first == True and second == False and third == False:
		second = True
	elif first == False and second == True and third == False:
		first = True
	elif first == False and second == False and third == True:
		first = True
	elif first == True and second == True and third == False:
		third = True
	elif first == False and second == True and third == True:
		first = True
	elif first == True and second == True and third == True:
		run()
	elif first == True and second == False and third == True:
		second = True
	if half_inning % 2 != 0: #if top of inning
		away_hbp_count = away_hbp_count + 1
	elif half_inning % 2 ==	0: # if bottom of inning
		home_hbp_count = home_hbp_count + 1
	resetcount()

def single():
	global first
	global second
	global third
	global home_single_count
	global away_single_count
	if first == False and second == False and third == False:
		first = True
	elif first == True and second == False and third == False:
		second = True
	elif first == False and second == True and third == False:
		first = True
	elif first == False and second == False and third == True:
		first = True
		run()
	elif first == True and second == True and third == False:
		third = True
	elif first == False and second == True and third == True:
		first = True
		second = False
		run()
	elif first == True and second == True and third == True:
		run()
	elif first == True and second == False and third == True:
		second = True
		third = False
		run()
	if half_inning % 2 != 0: #if top of inning
		away_single_count = away_single_count + 1
	elif half_inning % 2 ==	0: # if bottom of inning
		home_single_count = home_single_count + 1
	resetcount()

def double():
	global first
	global second
	global third
	global home_double_count
	global away_double_count
	if first == False and second == False and third == False:
		second = True
	elif first == True and second == False and third == False:
		second = True
		third = True
	elif first == False and second == True and third == False:
		run()
	elif first == False and second == False and third == True:
		run()
		third = False
		second = True
	elif first == True and second == True and third == False:
		first = False
		run()
		run()
	elif first == False and second == True and third == True:
		third = False
		run()
		run()
	elif first == True and second == True and third == True:
		first = False
		third = False
		run()
		run()
		run()
	elif first == True and second == False and third == True:
		second = True
		first = False
		third = False
		run()
		run()
	if half_inning % 2 != 0: #if top of inning
		away_double_count = away_double_count + 1
	elif half_inning % 2 ==	0: # if bottom of inning
		home_double_count = home_double_count + 1
	resetcount()
	
def triplee():
	global first
	global second
	global third
	global home_triple_count
	global away_triple_count
	if first == False and second == False and third == False:
		third = True
	elif first == True and second == False and third == False:
		first = False
		third = True
		run()
	elif first == False and second == True and third == False:
		third = True
		second = False
		run()
	elif first == False and second == False and third == True:
		run()
	elif first == True and second == True and third == False:
		third = True
		first = False
		second = False
		run()
		run()
	elif first == False and second == True and third == True:
		second = False
		run()
		run()
	elif first == True and second == True and third == True:
		first = False
		second = False
		third = True
		run()
		run()
		run()
	elif first == True and second == False and third == True:
		first = False
		run()
		run()
	if half_inning % 2 != 0: #if top of inning
		away_triple_count = away_triple_count + 1
	elif half_inning % 2 ==	0: # if bottom of inning
		home_triple_count = home_triple_count + 1
	resetcount()

def homerun():
	global first
	global second
	global third
	global home_homerun_count
	global away_homerun_count
	if first == False and second == False and third == False:
		run()
	elif first == True and second == False and third == False:
		first = False
		run()
		run()
	elif first == False and second == True and third == False:
		second = False
		run()
		run()
	elif first == False and second == False and third == True:
		third = False
		run()
	elif first == True and second == True and third == False:
		first = False
		second = False
		run()
		run()
	elif first == False and second == True and third == True:
		third = False
		second = False
		run()
		run()
		run()
	elif first == True and second == True and third == True:
		first = False
		second = False
		third = False
		run()
		run()
		run()
		run()
	elif first == True and second == False and third == True:
		first = False
		third = False
		run()
		run()
		run()
	if half_inning % 2 != 0: #if top of inning
		away_homerun_count = away_homerun_count + 1
	elif half_inning % 2 ==	0: # if bottom of inning
		home_homerun_count = home_homerun_count + 1
	resetcount()
	
def run():
	global half_inning
	global away_score
	global home_score
	global gameover
	if half_inning < 18: # no walkoff possible
		#if the half_inning number is odd, score for away. if even, score for home.
		if half_inning % 2 != 0: #odd
			away_score = away_score + 1
			print ("Run scored by AWAY!")
		elif half_inning % 2 ==	0: #even
			home_score = home_score + 1
			print ("Run scored by HOME!")
	elif half_inning >= 18: #walkoff occurs if home scores		
		#if the half_inning number is odd, score for away. if even, score for home.
		if half_inning % 2 != 0: #odd/top
			away_score = away_score + 1
			print ("Run scored by AWAY!")
			
		elif half_inning % 2 ==	0: #even/bottom
			if away_score > home_score:
				home_score = home_score + 1
				print ("Run scored by HOME!")
			elif away_score == home_score:
				home_score = home_score + 1
				print ("WALKOFF RUN scored by HOME!")
				print ("Game has ended. HOME wins.")
				gameover = True
			
#def pitch():
	global rand
	global balls
	global strikes
	global outs
	global result

def status():
	global outs
	global half_inning
	global home_score
	global away_score
	global first
	global second
	global third
	print ("Outs: " + str(outs) + " | Inning: ", end ="")
	if half_inning % 2 != 0:
		print ("Top ", end ="")
	elif half_inning % 2 == 0:
		print ("Bot ", end ="")
	print (str(math.ceil(half_inning / 2)) + " | Home: " + str(home_score) + " | Away: " + str(away_score) + " | 1B: ", end ="")
	if first == True:
		print ("X 2B: ", end ="")
	elif first == False:
		print ("- 2B: ", end ="")
	if second == True:
		print ("X 3B: ", end ="")
	elif second == False:
		print ("- 3B: ", end ="")
	if third == True:
		print ("X")
	elif third == False:
		print ("-")

def wait():
	time.sleep(0)

#program starts		
print ("Welcome to Baseball Simulator")
status()

#while home_score + away_score < 100:
	
while gameover == False:
	
	print ("Pitching...")
	wait()
	random_number()
	if 0 <= rand <= 36:
		result = "Ball"
		if balls < 3:
			balls = balls + 1
			print ("Ball. (" + str(balls) + " - " + str(strikes) + ")")
			wait()
		elif balls == 3:
			result = "Walk"
			print ("WALK!")
			walk()
			wait()
	elif 35 <= rand <= 67:
		result = "Strike"
		if strikes < 2:
			strikes = strikes + 1
			print ("Strike. (" + str(balls) + " - " + str(strikes) + ")")
			wait()
		elif strikes == 2:
			result = "Strikeout"
			print ("STRIKEOUT!")
			if half_inning % 2 != 0: #if top of inning
				away_strikeout_count = away_strikeout_count + 1
			elif half_inning % 2 ==	0: # if bottom of inning
				home_strikeout_count = home_strikeout_count + 1
			out()
			wait()
	elif 66 <= rand <= 77:
		result = "Foul"
		if strikes < 2:
			strikes = strikes + 1
			wait()
		#else:	
		print ("Foul. (" + str(balls) + " - " + str(strikes) + ")")
	elif 76 <= rand <= 83:
		result = "Grounder"	
		grounder()
		wait()
	elif 82 <= rand <= 85:
		result = "Fly"
		print ("INFIELD FLY!")
		out()
		wait()
	elif 84 <= rand <= 88:
		result = "Fly"
		outfieldfly()
		wait()
	elif 87 <= rand <= 93:
		result = "Single"
		print ("SINGLE!")
		single()
		wait()
	elif 92 <= rand <= 97:
		result = "Double"
		print ("DOUBLE!")
		double()
		wait()
	elif 96 <= rand <= 99:
		result = "Home run"
		print ("HOME RUN!")
		homerun()
		wait()
	elif 97 <= rand <= 101:
		result = "Hit by pitch"
		print ("HIT BY PITCH!")
		hit_by_pitch()
		wait()
	elif rand == 99:
		result = "Triple"
		print ("TRIPLE!")
		triplee()
		wait()
		
	if result == "Walk" or result == "Single" or result == "Double" or result == "Triple" or result == "Home run" or result == "Hit by pitch" or result == "Strikeout" or result == "Grounder" or result == "Fly" or result == "Sacrifice fly":
		#at-bat is over
		print ("")
		status()
		wait()
			
print("End has been reached.")
print("")
print("---Game Statistics---")
print("First pitch: " + (datetime.strftime(datetime.now(), "%Y")) + "-" + (datetime.strftime(datetime.now(), "%m")) + "-" + (datetime.strftime(datetime.now(), "%d")) + " at " + (datetime.strftime(datetime.now(), "%H")) + (datetime.strftime(datetime.now(), "%M"))) 
print("")
print("HOME batting:")
print("Strikeouts: " + str(home_strikeout_count))
print("Walks: " + str(home_walk_count))
print("Singles: " + str(home_single_count))
print("Doubles: " + str(home_double_count))
print("Triples: " + str(home_triple_count))
print("Home runs: " + str(home_homerun_count))
print("Hit by pitch: " + str(home_hbp_count))
print("")
print("AWAY batting:")
print("Strikeouts: " + str(away_strikeout_count))
print("Walks: " + str(away_walk_count))
print("Singles: " + str(away_single_count))
print("Doubles: " + str(away_double_count))
print("Triples: " + str(away_triple_count))
print("away runs: " + str(away_homerun_count))
print("Hit by pitch: " + str(away_hbp_count))

	
	
	
	
	
	
	
	
	
	
	
	
	
	
"""
ball 35% 1-35
strike 30% 36-65
foul 10% 67-76
ground out 6% 77-82
fly out 5% 83-87
single 5% 88-92
double 4% 93-96
home run 97-98
hit by pitch 99
triple  100
"""





