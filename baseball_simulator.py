#https://github.com/benryan03/baseball_simulator/

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
	
def resetcount():
	global balls
	global strikes
	balls = 0
	strikes = 0
	
def out(num):
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
	for x in range (num):
		if outs <=1:
			resetcount()
			outs = outs + 1
		elif outs == 2 and half_inning < 17:
		#before 9th inning, no win possible
			outs = 3
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
		elif outs == 2 and half_inning >= 17 and half_inning % 2 != 0: # if 2 outs and 9th inning or later and end of top of inning
			outs = 3
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
		elif outs == 2 and half_inning >= 17 and half_inning % 2 == 0 and home_score > away_score:
		# if 2 outs and 9th inning or later and end of bottom of inning and home team is ahead
			outs = 3
			print("Game has ended. " + home_team + " wins.")
			gameover = True
			return
		elif outs == 2 and half_inning >= 17 and half_inning % 2 == 0 and home_score < away_score:
		# if 2 outs and 9th inning or later and end of bottom of inning and away team is ahead
			outs = 3
			print("Game has ended. " + away_team + " wins.")
			gameover = True
			return
		elif outs == 2 and half_inning >= 17 and half_inning % 2 == 0 and home_score == away_score:
		# if 2 outs and 9th inning or later and end of bottom of inning and score is tied
			outs = 3
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

def run(num):
	global half_inning
	global away_score
	global home_score
	global gameover
	for x in range (num):
		if half_inning < 18 and half_inning % 2 != 0:
			#normal innings - run for away
			away_score = away_score + 1
			print ("Run scored by AWAY!")
		elif half_inning < 18 and half_inning % 2 == 0:
			#normal innings - run for home
			home_score = home_score + 1
			print ("Run scored by " + home_team + "!")
		elif half_inning >= 18 and half_inning % 2 != 0: #odd/top of inning
			#extra innings - run for away
			away_score = away_score + 1
			print ("Run scored by AWAY!")
		elif half_inning >= 18 and half_inning % 2 == 0 and away_score > home_score: #even/bottom of inning
			#extra innings - run for home, no walkoff
			home_score = home_score + 1
			print ("Run scored by HOME!")
		elif half_inning >= 18 and half_inning % 2 == 0 and away_score == home_score: #even/bottom of inning
			#walkoff run!
			home_score = home_score + 1
			print ("WALKOFF RUN scored by " + home_team + "!")
			print("Game has ended. " + home_team + " wins.")
			gameover = True

def status(): #print number of outs, inning number, score, and on-base statuses
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
	print (str(math.ceil(half_inning / 2)) + " | " + home_team + ": " + str(home_score) + " | " + away_team + ": " + str(away_score) + " | 3B: ", end ="")
	if third == True:
		print ("X 2B: ", end ="")
	elif third == False:
		print ("- 2B: ", end ="")
	if second == True:
		print ("X 1B: ", end ="")
	elif second == False:
		print ("- 1B: ", end ="")
	if first == True:
		print ("X")
	elif first == False:
		print ("-")

def wait(): #change these wait times to 0 for game to complete immediately
	time.sleep(2)

def wait_short():
	time.sleep(.2)

#program start
print ("Welcome to Baseball Simulator")
home_team = input("Enter the name of the home team: ")
away_team = input("Enter the name of the away team: ")
status()

while gameover == False: #main program loop

	#pitching animation
	print ("Pitching ", end="", flush=True)	# flush=True needs to be included, otherwise time.sleep instances will occur all at once
	for x in range (0, 3):
		wait_short()
		print (". ", end="", flush=True)
	print("")

	rand = random.randint(1, 100) #generate random number to determine result of pitch
	
	if 0 <= rand <= 36 and balls < 3:
		result = "Ball"
		balls = balls + 1
		print ("Ball. (" + str(balls) + " - " + str(strikes) + ")")

	elif 0 <= rand <= 36 and balls == 3:
		result = "Ball"
		result = "Walk"
		print ("WALK!")
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
			run(1)
		elif first == True and second == False and third == True:
			second = True
		if half_inning % 2 != 0: #if top of inning
			away_walk_count = away_walk_count + 1
		elif half_inning % 2 ==	0: # if bottom of inning
			home_walk_count = home_walk_count + 1
		resetcount()

	elif 35 <= rand <= 67 and strikes <2:
		result = "Strike"
		strikes = strikes + 1
		print ("Strike. (" + str(balls) + " - " + str(strikes) + ")")

	elif 35 <= rand <= 67 and strikes ==2 and half_inning % 2 != 0: #if top of inning
		result = "Strike"
		result = "Strikeout"
		print ("STRIKEOUT!")
		away_strikeout_count = away_strikeout_count + 1
		out(1)

	elif 35 <= rand <= 67 and strikes ==2 and half_inning % 2 == 0: #if bottom of inning
		result = "Strike"
		result = "Strikeout"
		print ("STRIKEOUT!")
		home_strikeout_count = home_strikeout_count + 1
		out(1)

	elif 66 <= rand <= 77 and strikes < 2:
		result = "Foul"
		strikes = strikes + 1
		print ("Foul. (" + str(balls) + " - " + str(strikes) + ")")

	elif 66 <= rand <= 77 and strikes == 2:
		result = "Foul"
		print ("Foul. (" + str(balls) + " - " + str(strikes) + ")")

	elif 76 <= rand <= 83:
		result = "Grounder"	
		if first == False and second == False and third == False:
			print ("GROUND OUT!")
			out(1)	
		elif first == True and second == False and third == False and outs < 2:
			print ("DOUBLE PLAY!")
			out(2)
		elif first == True and second == False and third == False and outs == 2:
			out(1)
		elif first == False and second == True and third == False:
			print ("GROUND OUT!")
			out(1)	
		elif first == False and second == False and third == True:
			print ("GROUND OUT!")
			out(1)
		elif first == True and second == True and third == False and outs == 0:
			print ("TRIPLE PLAY!")
			out(3)
		elif first == True and second == True and third == False and outs == 1:
			print ("DOUBLE PLAY!")
			out(2)
		elif first == True and second == True and third == False and outs == 2:
			print ("GROUND OUT!")
			out(1)	
		elif first == False and second == True and third == True:
			print ("GROUND OUT!")
			out(1)
		elif first == True and second == True and third == True and outs == 0:
			print ("TRIPLE PLAY!")
			out(3)
		elif first == True and second == True and third == True and outs == 1:
			print ("DOUBLE PLAY!")
			out(2)
		elif first == True and second == True and third == True and outs == 2:
			print ("GROUND OUT!")
			out(1)
		elif first == True and second == False and third == True and outs <2:
			print ("DOUBLE PLAY!")
			out(2)    
		elif first == True and second == False and third == True and outs == 2:
			print ("GROUND OUT!")
			out(1)
		resetcount()

	elif 82 <= rand <= 85:
		result = "Fly"
		print ("POPPED UP!")
		out(1)

	elif 84 <= rand <= 88:
		result = "Fly"
		if first == False and second == False and third == False:
			print ("FLY OUT!")
			out(1)
		elif first == True and second == False and third == False:
			print ("FLY OUT!")
			out(1)
		elif first == False and second == True and third == False and outs < 2:
			print ("FLY OUT! RUNNER ADVANCED.")
			second = False
			third = True
			out(1)
		elif first == False and second == True and third == False and outs == 2:
			print ("FLY OUT!")
			out(1)
		elif first == False and second == False and third == True and outs < 2:
			print ("SACRIFICE FLY!")
			third = False
			out(1)
			run(1)
		elif first == False and second == False and third == True and outs == 2:
			print ("FLY OUT!")
			out(1)
		elif first == True and second == True and third == False and outs < 2:
			print ("FLY OUT! RUNNERS ADVANCED.")
			second = False
			third = True
			out(1)
		elif first == True and second == True and third == False and outs == 2:
			print ("FLY OUT!")
			out(1)
		elif first == False and second == True and third == True and outs < 2:
			print ("SACRIFICE FLY!")
			third = False
			out(1)
			run(1)
		elif first == False and second == True and third == True and outs == 2:
			print ("FLY OUT!")
			out(1)
		elif first == True and second == False and third == True and outs < 2:
			print ("SACRIFICE FLY!")
			third = False
			out(1)
			run(1)
		elif first == True and second == False and third == True and outs == 2:
			print ("FLY OUT!")
			out(1)
		elif first == True and second == True and third == True and outs < 2:
			print ("SACRIFICE FLY!")
			third = False
			out(1)
			run(1)
		elif first == True and second == True and third == True and outs < 2:
			print ("FLY OUT!")
			out(1)
		resetcount()

	elif 87 <= rand <= 93:
		result = "Single"
		print ("SINGLE!")
		if first == False and second == False and third == False:
			first = True
		elif first == True and second == False and third == False:
			second = True
		elif first == False and second == True and third == False:
			first = True
		elif first == False and second == False and third == True:
			first = True
			run(1)
		elif first == True and second == True and third == False:
			third = True
		elif first == False and second == True and third == True:
			first = True
			second = False
			run(1)
		elif first == True and second == True and third == True:
			run(1)
		elif first == True and second == False and third == True:
			second = True
			third = False
			run(1)
		if half_inning % 2 != 0: #if top of inning
			away_single_count = away_single_count + 1
		elif half_inning % 2 ==	0: # if bottom of inning
			home_single_count = home_single_count + 1
		resetcount()

	elif 92 <= rand <= 97:
		result = "Double"
		print ("DOUBLE!")
		if first == False and second == False and third == False:
			second = True
		elif first == True and second == False and third == False:
			second = True
			third = True
		elif first == False and second == True and third == False:
			run(1)
		elif first == False and second == False and third == True:
			run(1)
			third = False
			second = True
		elif first == True and second == True and third == False:
			first = False
			run(2)
		elif first == False and second == True and third == True:
			third = False
			run(2)
		elif first == True and second == True and third == True:
			first = False
			third = False
			run(3)
		elif first == True and second == False and third == True:
			second = True
			first = False
			third = False
			run(2)
		if half_inning % 2 != 0: #if top of inning
			away_double_count = away_double_count + 1
		elif half_inning % 2 ==	0: # if bottom of inning
			home_double_count = home_double_count + 1
			resetcount()
	
	elif 96 <= rand <= 99:
		result = "Home run"
		print ("HOME RUN!")
		if first == False and second == False and third == False:
			run(1)
		elif first == True and second == False and third == False:
			first = False
			run(2)
		elif first == False and second == True and third == False:
			second = False
			run(2)
		elif first == False and second == False and third == True:
			third = False
			run(1)
		elif first == True and second == True and third == False:
			first = False
			second = False
			run(2)
		elif first == False and second == True and third == True:
			third = False
			second = False
			run(3)
		elif first == True and second == True and third == True:
			first = False
			second = False
			third = False
			run(4)
		elif first == True and second == False and third == True:
			first = False
			third = False
			run(3)
		if half_inning % 2 != 0: #if top of inning
			away_homerun_count = away_homerun_count + 1
		elif half_inning % 2 ==	0: # if bottom of inning
			home_homerun_count = home_homerun_count + 1
		resetcount()

	elif 97 <= rand <= 101:
		result = "Hit by pitch"
		print ("HIT BY PITCH!")
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
			run(1)
		elif first == True and second == False and third == True:
			second = True
		if half_inning % 2 != 0: #if top of inning
			away_hbp_count = away_hbp_count + 1
		elif half_inning % 2 ==	0: # if bottom of inning
			home_hbp_count = home_hbp_count + 1
		resetcount()

	elif rand == 99:
		result = "Triple"
		print ("TRIPLE!")
		if first == False and second == False and third == False:
			third = True
		elif first == True and second == False and third == False:
			first = False
			third = True
			run(1)
		elif first == False and second == True and third == False:
			third = True
			second = False
			run(1)
		elif first == False and second == False and third == True:
			run(1)
		elif first == True and second == True and third == False:
			third = True
			first = False
			second = False
			run(2)
		elif first == False and second == True and third == True:
			second = False
			run(2)
		elif first == True and second == True and third == True:
			first = False
			second = False
			third = True
			run(3)
		elif first == True and second == False and third == True:
			first = False
			run(2)
		if half_inning % 2 != 0: #if top of inning
			away_triple_count = away_triple_count + 1
		elif half_inning % 2 ==	0: # if bottom of inning
			home_triple_count = home_triple_count + 1
		resetcount()

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
print(home_team + " batting:")
print("Strikeouts: " + str(home_strikeout_count))
print("Walks: " + str(home_walk_count))
print("Singles: " + str(home_single_count))
print("Doubles: " + str(home_double_count))
print("Triples: " + str(home_triple_count))
print("Home runs: " + str(home_homerun_count))
print("Hit by pitch: " + str(home_hbp_count))
print("")
print(away_team + " batting:")
print("Strikeouts: " + str(away_strikeout_count))
print("Walks: " + str(away_walk_count))
print("Singles: " + str(away_single_count))
print("Doubles: " + str(away_double_count))
print("Triples: " + str(away_triple_count))
print("away runs: " + str(away_homerun_count))
print("Hit by pitch: " + str(away_hbp_count))

save_results = input("Save results to text file? (Y/N)")
if save_results == "y" or save_results == "Y":

	results_filename = ("Game on " + (datetime.strftime(datetime.now(), "%Y")) + "-" + (datetime.strftime(datetime.now(), "%m")) + "-" + (datetime.strftime(datetime.now(), "%d")) + " at " + (datetime.strftime(datetime.now(), "%H")) + (datetime.strftime(datetime.now(), "%M")) + ".txt")
	
	file1 = open(results_filename, "w+")

	if home_score > away_score:
		file1.write(home_team + " won with a score of " + str(home_score) + "-" + str(away_score) + ".\n")
	elif away_score > home_score:
		file1.write(away_team + " won with a score of " + str(home_score) + "-" + str(away_score) + ".\n")

	file1.write("\n")
	file1.write("First pitch: " + (datetime.strftime(datetime.now(), "%Y")) + "-" + (datetime.strftime(datetime.now(), "%m")) + "-" + (datetime.strftime(datetime.now(), "%d")) + " at " + (datetime.strftime(datetime.now(), "%H")) + ":" + (datetime.strftime(datetime.now(), "%M\n")))
	file1.write("\n")
	file1.write(home_team + " batting:\n")
	file1.write("Strikeouts: " + str(home_strikeout_count) + "\n")
	file1.write("Walks: " + str(home_walk_count) + "\n")
	file1.write("Singles: " + str(home_single_count) + "\n")
	file1.write("Doubles: " + str(home_double_count) + "\n")
	file1.write("Triples: " + str(home_triple_count) + "\n")
	file1.write("Home runs: " + str(home_homerun_count) + "\n")
	file1.write("Hit by pitch: " + str(home_hbp_count) + "\n")
	file1.write("\n")
	file1.write(away_team + " batting:" + "\n")
	file1.write("Strikeouts: " + str(away_strikeout_count) + "\n")
	file1.write("Walks: " + str(away_walk_count) + "\n")
	file1.write("Singles: " + str(away_single_count) + "\n")
	file1.write("Doubles: " + str(away_double_count) + "\n")
	file1.write("Triples: " + str(away_triple_count) + "\n")
	file1.write("away runs: " + str(away_homerun_count) + "\n")
	file1.write("Hit by pitch: " + str(away_hbp_count))

	print("Results saved to " + results_filename)
