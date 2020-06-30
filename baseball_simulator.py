#https://github.com/benryan03/baseball_simulator/

import random
import time
import math
from datetime import datetime

#To scrape players and stats from baseball-reference
from lxml import html
import requests

from colorama import Fore, Back, Style 

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
pitch_result = "_"
gameover = False
atbat_pitch_count = 1
#home_pitcher_pitch_count = 1
#away_pitcher_pitch_count = 0




home_pitcher_pitch_count = 98
away_pitcher_pitch_count = 0





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

current_away_batter = 0
current_home_batter = 0

margin = 0
edge = ["", 0]

redo_pitch_loops = 0

runs_in_current_inning = 0

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
	global runs_in_current_inning
	for x in range (num):
		if outs <=1:
			resetcount()
			outs = outs + 1
		elif outs == 2 and half_inning < 17:
		#before 9th inning, no win possible
			outs = 3
			wait()
			half_inning = half_inning + 1
			inning_status()
			outs = 0
			first = False
			second = False
			third = False
			balls = 0
			strikes = 0
			runs_in_current_inning = 0
			if half_inning == 2:
				print("Starting pitcher for " + away_team + ": " + away_starting_pitcher[0])
				wait()
				print(str(away_year) + " ERA: " + str(format_era(away_starting_pitcher[1])))
				wait()
		elif outs == 2 and half_inning >= 17 and half_inning % 2 != 0: # if 2 outs and 9th inning or later and end of top of inning
			outs = 3
			print ("Half-inning has ended.")
			print("")
			wait()
			half_inning = half_inning + 1
			inning_status()
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
			inning_status()
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
	global runs_in_current_inning
	for x in range (num):
		if half_inning < 18 and half_inning % 2 != 0:
			#normal innings - run for away
			away_score = away_score + 1
			runs_in_current_inning = runs_in_current_inning + 1
			print ("Run scored by " + away_team + "!")
			wait_short()
		elif half_inning < 18 and half_inning % 2 == 0:
			#normal innings - run for home
			home_score = home_score + 1
			runs_in_current_inning = runs_in_current_inning + 1
			print ("Run scored by " + home_team + "!")
			wait_short()
		elif half_inning >= 18 and half_inning % 2 != 0: #odd/top of inning
			#extra innings - run for away
			away_score = away_score + 1
			runs_in_current_inning = runs_in_current_inning + 1
			print ("Run scored by " + away_team + "!")
			wait_short()
		elif half_inning >= 18 and half_inning % 2 == 0 and away_score > home_score: #even/bottom of inning
			#extra innings - run for home, no walkoff
			home_score = home_score + 1
			print ("Run scored by " + home_team + "!")
			runs_in_current_inning = runs_in_current_inning + 1
			wait_short()
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

	wait()

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

	wait()

	now_batting()
	
	wait()

def now_batting():
	global edge
	global edge_pos
	global margin
	global redo_pitch_loops

	if half_inning % 2 == 0:
		print ("Now batting for " + home_team + ": " + str(home_batters[current_home_batter][0]) + ". " + str(home_year) + " AVG: " + format_batting_average(home_batters[current_home_batter][1]))
	else:
		print ("Now batting for " + away_team + ": " + str(away_batters[current_away_batter][0]) + ". " + str(away_year) + " AVG: " + format_batting_average(away_batters[current_away_batter][1]))

	redo_pitch_loops = 0

	# Determine advantage
	if half_inning % 2 == 0: #Bottom half
		avg = home_batters[current_home_batter][1]
		era = current_away_pitcher[1]

		x = avg / .250
		y = (2 - (era / 4)) - (away_pitcher_pitch_count * .005)

		if x > y:
			#Batter has adventage
			edge = home_batters[current_home_batter][0]
			edge_pos = "Batter"
			margin = x - y

		elif x <= y:
			#Pitcher has advantage
			edge = current_away_pitcher[0]
			edge_pos = "Pitcher"
			margin = y - x

		wait()
		margin = round(margin*50,1)
		print("Edge: " + edge + " - " + str(margin) + "%")

	elif half_inning % 2 != 0: #Top half
		avg = away_batters[current_away_batter][1]
		era = current_home_pitcher[1]
		
		x = avg / .250
		#x = 1000
		y = (2 - (era / 4)) - (home_pitcher_pitch_count * .005)

		if x > y:
			#Batter has adventage
			edge = away_batters[current_away_batter][0]
			edge_pos = "Batter"
			margin = x - y

		elif x <= y:
			#Pitcher has advantage
			edge = current_home_pitcher[0]
			edge_pos = "Pitcher"
			margin = y - x

		wait()
		margin = round(margin*50,1)
		print("Edge: " + edge + " - " + str(margin) + "%")

def next_batter():
	global half_inning
	global current_home_batter
	global current_away_batter

	if half_inning % 2 == 0 and current_home_batter < 8:
		current_home_batter = current_home_batter + 1
	elif half_inning % 2 == 0 and current_home_batter == 8:
		current_home_batter = 0
	elif half_inning % 2 != 0 and current_away_batter < 8:
		current_away_batter = current_away_batter + 1
	elif half_inning % 2 != 0 and current_away_batter == 8:
		current_away_batter = 0

def format_batting_average(avg):
	avg_string = str(avg)
	avg_string = avg_string[1:] # Remove leading 0

	# Add trailing 0s if necessary
	if len(avg_string) == 2:
		avg_string = avg_string + "00"
	elif len(avg_string) == 3:
		avg_string = avg_string + "0"
	
	return avg_string

def format_era(era):
	era_string = str(era)

	# Add trailing 0 if necessary
	if len(era_string) == 3:
		era_string = era_string + "0"
	
	return era_string

def wait(): #change these wait times to 0 for game to complete immediately
	time.sleep(.5) # 2

def wait_short():
	time.sleep(.2) # .2

def calculate_pitch_outcome(pitch, redo_pitch):
	global edge_pos
	global margin
	global redo_pitch_loops
	
	rand = random.randint(1, 100)

	pitch = 1

	if pitch == 1:
		if rand >= 1 and rand <= 25: #Ball
			print(Style.DIM + "init: ball" + Style.RESET_ALL)
			if edge_pos == "Pitcher":
				print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL)
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL)
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL)
					return "Ball"
			else:
				print(Style.DIM + "No redo attempt" + Style.RESET_ALL)
				return "Ball"
		elif rand >=26 and rand <= 50: #Called Strike
			print(Style.DIM + "init: called strike" + Style.RESET_ALL)
			if edge_pos == "Batter":
				print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL)
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL)
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL)
					return "Strike"
			else:
				print(Style.DIM + "No redo attempt" + Style.RESET_ALL)
				return "Strike"
		elif rand >= 51 and rand <= 75: #Foul
			print(Style.DIM + "init: foul" + Style.RESET_ALL)
			if edge_pos == "Batter":
				print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL)
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL)
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL)
					return "Foul"
			else:
				print(Style.DIM + "No redo attempt" + Style.RESET_ALL)
				return "Foul"
		else: #Ball in play
			print(Style.DIM + "init: ballinplay" + Style.RESET_ALL)
			if edge_pos == "Pitcher":
				print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL)
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL)
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL)
					return "Ball_in_play"
			else:
				print(Style.DIM + "No redo attempt" + Style.RESET_ALL)
				return "Ball_in_play"
		
	"""	
	if pitch == 1:
		if rand <= 1 and rand <= 43: #Ball
			#print(Style.DIM + "init: ball" + Style.RESET_ALL) #DEBUG
			if edge_pos == "Pitcher":
				#print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					#print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					calculate_pitch_outcome(pitch, True)
				else:
					#print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					return "Ball"
			else:
				#print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				return "Ball"
		elif rand <=44 and rand <= 72: #Called Strike
			#print(Style.DIM + "init: called strike" + Style.RESET_ALL) #DEBUG
			if edge_pos == "Batter":
				#print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					#print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					calculate_pitch_outcome(pitch, True)
				else:
					#print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					return "Strike"
			else:
				#print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				return "Strike"
		elif rand <= 73 and rand <= 82: #Foul
			#print(Style.DIM + "init: foul" + Style.RESET_ALL) #DEBUG
			if edge_pos == "Batter":
				#print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					#print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					calculate_pitch_outcome(pitch, True)
				else:
					#print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					return "Foul"
			else:
				#print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				return "Foul"
		elif rand <= 83 and rand <= 88: #Swinging Strike
			#print(Style.DIM + "init: swinging strike" + Style.RESET_ALL) #DEBUG
			if edge_pos == "Batter":
				#print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					#print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					calculate_pitch_outcome(pitch, True)
				else:
					#print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					return "Strike"
			else:
				#print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				return "Strike"
		else: #Ball in play
			#print(Style.DIM + "init: ballinplay" + Style.RESET_ALL) #DEBUG
			if edge_pos == "Pitcher":
				#print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					#print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					calculate_pitch_outcome(pitch, True)
				else:
					#print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					return "Ball_in_play"
			else:
				#print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				return "Ball_in_play"
	elif pitch == 2:
		if rand <= 1 and rand <= 40: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball"
		elif rand <=41 and rand <= 56: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		elif rand <= 57 and rand <= 72: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Foul"
		elif rand <= 73 and rand <= 81: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball_in_play"
	elif pitch == 3:
		if rand <= 1 and rand <= 39: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball"
		elif rand <=40 and rand <= 52: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		elif rand <= 53 and rand <= 70: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Foul"
		elif rand <= 71 and rand <= 80: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball_in_play"
	elif pitch == 4:
		if rand <= 1 and rand <= 35: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball"
		elif rand <=36 and rand <= 47: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		elif rand <= 48 and rand <= 68: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Foul"
		elif rand <= 69 and rand <= 80: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball_in_play"
	elif pitch == 5:
		if rand <= 1 and rand <= 31: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball"
		elif rand <=32 and rand <= 40: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		elif rand <= 41 and rand <= 61: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Foul"
		elif rand <= 62 and rand <= 73: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball_in_play"
	elif pitch == 6:
		if rand <= 1 and rand <= 26: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball"
		elif rand <=27 and rand <= 30: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		elif rand <= 31 and rand <= 53: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Foul"
		elif rand <= 54 and rand <= 65: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball_in_play"
	elif pitch == 7:
		if rand <= 1 and rand <= 25: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball"
		elif rand <=26 and rand <= 29: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		elif rand <= 30 and rand <= 57: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Foul"
		elif rand <= 58 and rand <= 69: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball_in_play"
	elif pitch == 8:
		if rand <= 1 and rand <= 24: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball"
		elif rand <=25 and rand <= 28: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		elif rand <= 29 and rand <= 57: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Foul"
		elif rand <= 58 and rand <= 68: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball_in_play"
	elif pitch == 9:
		if rand <= 1 and rand <= 23: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball"
		elif rand <=24 and rand <= 26: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		elif rand <= 27 and rand <= 57: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Foul"
		elif rand <= 58 and rand <= 68: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball_in_play"
	elif pitch == 10:
		if rand <= 1 and rand <= 22: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball"
		elif rand <=23 and rand <= 25: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		elif rand <= 26 and rand <= 57: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Foul"
		elif rand <= 58 and rand <= 68: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball_in_play"	
	elif pitch == 11:
		if rand <= 1 and rand <= 22: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball"
		elif rand <=23 and rand <= 25: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		elif rand <= 26 and rand <= 57: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Foul"
		elif rand <= 58 and rand <= 68: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball_in_play"
	elif pitch == 12:
		if rand <= 1 and rand <= 28: #Ball
			if edge_pos == "Pitch9er":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball"
		elif rand <=29 and rand <= 40: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		elif rand <= 41 and rand <= 58: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					calculate_pitch_outcome(pitch, True)
			return "Ball_in_play"
	"""

def pitching_animation():
	global current_away_pitcher
	global current_home_pitcher
	global away_pitcher_pitch_count
	global home_pitcher_pitch_count

	if half_inning % 2 == 0:
		current_pitcher = current_away_pitcher
		current_pitcher_pitch_count = away_pitcher_pitch_count
	else:
		current_pitcher = current_home_pitcher
		current_pitcher_pitch_count = home_pitcher_pitch_count
	print ("Pitch " + str(current_pitcher_pitch_count) + " (" + current_pitcher[0] + ")", end="", flush=True)	# flush=True needs to be included, otherwise time.sleep instances will occur all at once
	for x in range (0, 3):
		wait_short()
		print (". ", end="", flush=True)

	for x in range (0, redo_pitch_loops):
		wait_short()
		print (". ", end="", flush=True)

	print("")

def check_if_pitching_change():
	global half_inning
	global current_home_pitcher
	global home_starting_pitcher
	global home_pitcher_pitch_count
	global home_score
	
	global current_away_pitcher
	global away_starting_pitcher
	global away_pitcher_pitch_count
	global away_score

	global outs
	global first
	global second
	global third


	if half_inning % 2 != 0: #Top half
		if current_home_pitcher == home_starting_pitcher:
			if home_pitcher_pitch_count >= 100:
				pitching_change()
			if half_inning >= 13:
				pitching_change()
			if away_score > 4:
				pitching_change()
		elif current_home_pitcher != home_starting_pitcher:
			if outs == 0 and first == False and second == False and third == False:
				if len(home_relief_pitchers) > 0:
					pitching_change()
			if runs_in_current_inning > 2:
				if len(home_relief_pitchers) > 0:
					pitching_change()

	elif half_inning % 2 == 0: #Bottom half
		if current_away_pitcher == away_starting_pitcher:
			if away_pitcher_pitch_count >= 100:
				pitching_change()
			if half_inning >= 14:
				pitching_change()
			if away_score > 4:
				pitching_change()
		elif current_away_pitcher != away_starting_pitcher:
			if outs == 0 and first == False and second == False and third == False:
				if len(away_relief_pitchers) > 0:
					pitching_change()
			if runs_in_current_inning > 2:
				if len(away_relief_pitchers) > 0:
					pitching_change()

	#else:

def pitching_change():
	global home_relief_pitchers
	global current_home_pitcher
	global home_pitcher_pitch_count
	global away_relief_pitchers
	global current_away_pitcher
	global away_pitcher_pitch_count

	if half_inning % 2 != 0: #Top half

		x = len(home_relief_pitchers)
		rand = random.randint(0, x-1)
		current_home_pitcher = home_relief_pitchers[rand]
		del home_relief_pitchers[rand]
		home_pitcher_pitch_count = 0

		wait()
		print("")
		print("Pitching change!")
		wait()
		print("")
		wait()
		print("Now pitching for " + home_team + ": " + current_home_pitcher[0])
		wait()
		print(str(home_year) + " ERA: " + str(format_era(current_home_pitcher[1])))
		wait()
		print("")
		wait()

	elif half_inning % 2 == 0: #Bottom half

		x = len(away_relief_pitchers)
		rand = random.randint(0, x-1)
		current_away_pitcher = away_relief_pitchers[rand]
		del away_relief_pitchers[rand]
		away_pitcher_pitch_count = 0

		print("\nPitching change!\n")
		wait()
		print("Now pitching for " + away_team + ": " + current_away_pitcher[0])
		wait()
		print(str(away_year) + " ERA: " + str(format_era(current_away_pitcher[1])))
		wait()

def inning_status():
	global half_inning

	if half_inning == 1 or half_inning == 2:
		x = "st"
	elif half_inning == 3  or half_inning == 4:
		x = "nd"
	elif half_inning == 5 or half_inning == 6:
		x = "rd"
	else:
		x = "th"

	if half_inning % 2 != 0:
		wait()
		print("")
		wait()
		print ("It is now the top of the " + str((half_inning/2) + .5)[0] + x + " inning.")
		wait()
		print("")
		wait()

	elif half_inning % 2 == 0:
		wait()
		print("")
		wait()
		print ("It is now the bottom of the " + str(half_inning/2)[0] + x + " inning.")
		wait()
		print("")
		wait()

#######################################################################################################################
#######################################################################################################################

#program start

home_team = "bos" #debug
home_year = "2018" #debug
away_team = "nyy" #debug
away_year = "2018" #debug

print ("Welcome to Baseball Simulator")
#home_team = input("Enter the name of the home team: ")
#home_year = input("Enter year: ")

#away_team = input("Enter the name of the away team: ")
#away_year = input("Enter year: ")

print("Loading players...")

#Load baseball-reference page for inputted team/year
#URL format: https://www.baseball-reference.com/teams/BOS/2004.shtml
home_page = requests.get("https://www.baseball-reference.com/teams/" + home_team + "/" + home_year + ".shtml")
home_tree = html.fromstring(home_page.content)
away_page = requests.get("https://www.baseball-reference.com/teams/" + away_team + "/" + away_year + ".shtml")
away_tree = html.fromstring(away_page.content)

home_batters = ["", "", "", "", "", "", "", "", ""]
away_batters = ["", "", "", "", "", "", "", "", ""]

#Scrape names of top 8 batters
for x in range(8):
	#Home
    fullname = home_tree.xpath('//table[@id="team_batting"]/tbody/tr[' + str(x+1) + ']/td[2]/@csk')
    fname = str(fullname).partition(",")[2]
    lname = str(fullname).partition(",")[0]
    home_batters[x] = fname.strip("[],'") + " " + lname.strip("[],'")

	#Away
    fullname = away_tree.xpath('//table[@id="team_batting"]/tbody/tr[' + str(x+1) + ']/td[2]/@csk')
    fname = str(fullname).partition(",")[2]
    lname = str(fullname).partition(",")[0]
    away_batters[x] = fname.strip("[],'") + " " + lname.strip("[],'")

#Scrape name of 9th batter (sometimes the formatting on baseball-reference skips the 9th row)
#Home
fullname = home_tree.xpath('//table[@id="team_batting"]/tbody/tr[9]/td[2]/@csk')
if fullname == []:
    fullname = home_tree.xpath('//table[@id="team_batting"]/tbody/tr[10]/td[2]/@csk')

fname = str(fullname).partition(",")[2]
lname = str(fullname).partition(",")[0]
home_batters[8] = fname.strip("[],'") + " " + lname.strip("[],'")

#Away
fullname = away_tree.xpath('//table[@id="team_batting"]/tbody/tr[9]/td[2]/@csk')
if fullname == []:
    fullname = away_tree.xpath('//table[@id="team_batting"]/tbody/tr[10]/td[2]/@csk')

fname = str(fullname).partition(",")[2]
lname = str(fullname).partition(",")[0]
away_batters[8] = fname.strip("[],'") + " " + lname.strip("[],'")

#Batting averages
home_avg = [0, 0, 0, 0, 0, 0, 0, 0, 0]
away_avg = [0, 0, 0, 0, 0, 0, 0, 0, 0]

#Scrape batting averages of first 8 batters
for x in range(8):
	avg = home_tree.xpath('//table[@id="team_batting"]/tbody/tr[' + str(x+1) + ']/td[17]/text()')
	home_avg[x] = float(str(avg).strip("[]'"))
	avg = away_tree.xpath('//table[@id="team_batting"]/tbody/tr[' + str(x+1) + ']/td[17]/text()')
	away_avg[x] = float(str(avg).strip("[]'"))

#Scrape batting average of 9th batter
avg = home_tree.xpath('//table[@id="team_batting"]/tbody/tr[9]/td[17]/text()')
if avg == []:
	avg = home_tree.xpath('//table[@id="team_batting"]/tbody/tr[10]/td[17]/text()')
	home_avg[8] = float(str(avg).strip("[]'"))
else:
	home_avg[8] = float(str(avg).strip("[]'"))
	
avg = away_tree.xpath('//table[@id="team_batting"]/tbody/tr[9]/td[17]/text()')
if avg == []:
	avg = away_tree.xpath('//table[@id="team_batting"]/tbody/tr[10]/td[17]/text()')
	away_avg[8] = float(str(avg).strip("[]'"))
else:
	away_avg[8] = float(str(avg).strip("[]'"))

#Add batting averages to batters array
home_batters = [[home_batters[0], home_avg[0]], [home_batters[1], home_avg[1]], [home_batters[2], home_avg[2]], [home_batters[3], home_avg[3]], [home_batters[4], home_avg[4]], [home_batters[5], home_avg[5]], [home_batters[6], home_avg[6]], [home_batters[7], home_avg[7]], [home_batters[8], home_avg[8]]]
away_batters = [[away_batters[0], away_avg[0]], [away_batters[1], away_avg[1]], [away_batters[2], away_avg[2]], [away_batters[3], away_avg[3]], [away_batters[4], away_avg[4]], [away_batters[5], away_avg[5]], [away_batters[6], away_avg[6]], [away_batters[7], away_avg[7]], [away_batters[8], away_avg[8]]]

#Sort array by batting average
home_batters = sorted(home_batters, key=lambda x: x[1], reverse=True)
away_batters = sorted(away_batters, key=lambda x: x[1], reverse=True)

home_pitchers = [[[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], ]
away_pitchers = [[[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], ]

home_relief_pitchers = [[[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]]]
away_relief_pitchers = [[[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]]]

home_closer = ["", 0]
away_closer = ["", 0]

#Scrape names and Earned Run Averages of top 12 pitchers
for x in range(12):
	#Home
	fullname = home_tree.xpath('//table[@id="team_pitching"]/tbody/tr[' + str(x+1) + ']/td[2]/@csk')
	position = home_tree.xpath('//table[@id="team_pitching"]/tbody/tr[' + str(x+1) + ']/td[1]/descendant::strong/text()')
	if str(fullname).strip("[],'") != "":
		fname = str(fullname).partition(",")[2]
		lname = str(fullname).partition(",")[0]
		if str(position).strip("[],'") == "CL":
			home_closer[0] = fname.strip("[],'") + " " + lname.strip("[],'")
			era = home_tree.xpath('//table[@id="team_pitching"]/tbody/tr[' + str(x+1) + ']/td[7]/text()')
			home_closer[1] = float(str(era).strip("[]'"))
			home_pitchers[x][0] = "_EMPTY_"
		else: #Not Closer
			home_pitchers[x][0] = fname.strip("[],'") + " " + lname.strip("[],'")
			era = home_tree.xpath('//table[@id="team_pitching"]/tbody/tr[' + str(x+1) + ']/td[7]/text()')
			home_pitchers[x][1] = float(str(era).strip("[]'"))
	else:
		home_pitchers[x][0] = "_EMPTY_"

	#away
	fullname = away_tree.xpath('//table[@id="team_pitching"]/tbody/tr[' + str(x+1) + ']/td[2]/@csk')
	position = away_tree.xpath('//table[@id="team_pitching"]/tbody/tr[' + str(x+1) + ']/td[1]/descendant::strong/text()')
	if str(fullname).strip("[],'") != "":
		fname = str(fullname).partition(",")[2]
		lname = str(fullname).partition(",")[0]
		if str(position).strip("[],'") == "CL":
			away_closer[0] = fname.strip("[],'") + " " + lname.strip("[],'")
			era = away_tree.xpath('//table[@id="team_pitching"]/tbody/tr[' + str(x+1) + ']/td[7]/text()')
			away_closer[1] = float(str(era).strip("[]'"))
			away_pitchers[x][0] = "_EMPTY_"
		else: #Not Closer
			away_pitchers[x][0] = fname.strip("[],'") + " " + lname.strip("[],'")
			era = away_tree.xpath('//table[@id="team_pitching"]/tbody/tr[' + str(x+1) + ']/td[7]/text()')
			away_pitchers[x][1] = float(str(era).strip("[]'"))
	else:
		away_pitchers[x][0] = "_EMPTY_"

#For some reason, these loops need to be run twice each
for x in home_pitchers:
	if "_EMPTY_" in x:
		home_pitchers.remove(x)
for x in home_pitchers:
	if "_EMPTY_" in x:
		home_pitchers.remove(x)
for x in away_pitchers:
	if "_EMPTY_" in x:
		away_pitchers.remove(x)
for x in away_pitchers:
	if "_EMPTY_" in x:
		away_pitchers.remove(x)

for x in range (5,9):
	home_relief_pitchers[x-5] = home_pitchers[x]
	away_relief_pitchers[x-5] = away_pitchers[x]


print("\nStarting lineup for " + home_team + ":")
#wait()
for x in home_batters:
	print(x[0] + " - " + format_batting_average(x[1]))
#	wait()

print("\nStarting lineup for " + away_team + ":")
#wait()
for x in away_batters:
	print(x[0] + " - " + format_batting_average(x[1]))
#	wait()

print("")
for x in home_pitchers:
	print(x)
print("")
for x in away_pitchers:
	print(x)

print("")
for x in home_relief_pitchers:
	print(x)
print("")
for x in away_relief_pitchers:
	print(x)

print("")
print(home_team + " closer: " + home_closer[0] + " - " + str(home_closer[1]))
print(away_team + " closer: " + away_closer[0] + " - " + str(away_closer[1]))

print()

wait()
pitcher_rand = random.randint(0, 4)
home_starting_pitcher = home_pitchers[pitcher_rand]
pitcher_rand = random.randint(0, 4)
away_starting_pitcher = away_pitchers[pitcher_rand]

current_home_pitcher = home_starting_pitcher
current_away_pitcher = away_starting_pitcher

print("Starting pitcher for " + home_team + ": " + home_starting_pitcher[0])
wait()
print(str(home_year) + " ERA: " + str(format_era(home_starting_pitcher[1])))
wait()
print()
print("PLAY BALL!")
wait()

print()
status()

while gameover == False: #main game loop

	pitch_result = calculate_pitch_outcome(atbat_pitch_count, False)

	#pitching_animation()

	if pitch_result == "Ball":
		if balls < 3:
			balls = balls + 1
			pitching_animation()
			print ("Ball. (" + str(balls) + " - " + str(strikes) + ")")

		elif balls == 3: #Walk
			pitch_result = "Walk"
			pitching_animation()
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
			next_batter()

	elif pitch_result == "Strike":
		if strikes <2: #Strike
			strikes = strikes + 1
			pitching_animation()
			print ("Strike. (" + str(balls) + " - " + str(strikes) + ")")

		elif strikes ==2 and half_inning % 2 != 0: #Strikeout - away
			pitching_animation()
			print ("STRIKEOUT!")
			pitch_result = "Strikeout"
			away_strikeout_count = away_strikeout_count + 1
			out(1)
			next_batter()

		elif strikes ==2 and half_inning % 2 == 0: #Strikeout - home
			pitching_animation()
			print ("STRIKEOUT!")
			pitch_result = "Strikeout"
			home_strikeout_count = home_strikeout_count + 1
			out(1)
			next_batter()

	elif pitch_result == "Foul":
		if strikes < 2: #Foul
			strikes = strikes + 1
			pitching_animation()
			print ("Foul. (" + str(balls) + " - " + str(strikes) + ")")

		elif strikes == 2: #Foul (with 2 strikes)
			pitching_animation()
			print ("Foul. (" + str(balls) + " - " + str(strikes) + ")")

	elif pitch_result == "Ball_in_play":
		rand = random.randint(1, 100)

		if 1 <= rand <= 40: #Fly out
			
			print(Style.DIM + "init: fly out" + Style.RESET_ALL) #DEBUG
			if edge_pos == "Batter":
				print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					#pitch_result = calculate_pitch_outcome(atbat_pitch_count, True)
					redo_pitch_loops = redo_pitch_loops + 1
					continue
				else:
					print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					pitch_result = "Fly"
			else:
				print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				pitch_result == "Fly"




			
			next_batter()
			if first == False and second == False and third == False:
				pitching_animation()
				print ("FLY OUT!")
				out(1)
			elif first == True and second == False and third == False:
				pitching_animation()
				print ("FLY OUT!")
				out(1)
			elif first == False and second == True and third == False and outs < 2:
				pitching_animation()
				print ("FLY OUT! RUNNER ADVANCED.")
				second = False
				third = True
				out(1)
			elif first == False and second == True and third == False and outs == 2:
				pitching_animation()
				print ("FLY OUT!")
				out(1)
			elif first == False and second == False and third == True and outs < 2:
				pitching_animation()
				print ("SACRIFICE FLY!")
				third = False
				out(1)
				run(1)
			elif first == False and second == False and third == True and outs == 2:
				pitching_animation()
				print ("FLY OUT!")
				out(1)
			elif first == True and second == True and third == False and outs < 2:
				pitching_animation()
				print ("FLY OUT! RUNNERS ADVANCED.")
				second = False
				third = True
				out(1)
			elif first == True and second == True and third == False and outs == 2:
				pitching_animation()
				print ("FLY OUT!")
				out(1)
			elif first == False and second == True and third == True and outs < 2:
				pitching_animation()
				print ("SACRIFICE FLY!")
				third = False
				out(1)
				run(1)
			elif first == False and second == True and third == True and outs == 2:
				pitching_animation()
				print ("FLY OUT!")
				out(1)
			elif first == True and second == False and third == True and outs < 2:
				pitching_animation()
				print ("SACRIFICE FLY!")
				third = False
				out(1)
				run(1)
			elif first == True and second == False and third == True and outs == 2:
				pitching_animation()
				print ("FLY OUT!")
				out(1)
			elif first == True and second == True and third == True and outs < 2:
				pitching_animation()
				print ("SACRIFICE FLY!")
				third = False
				out(1)
				run(1)
			elif first == True and second == True and third == True and outs < 2:
				pitching_animation()
				print ("FLY OUT!")
				out(1)
			resetcount()
			pitch_result = "Fly"



		elif 41 <= rand <= 70: #Ground out

			print(Style.DIM + "init: ground out" + Style.RESET_ALL) #DEBUG
			if edge_pos == "Batter":
				print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					#pitch_result = calculate_pitch_outcome(atbat_pitch_count, True)
					redo_pitch_loops = redo_pitch_loops + 1
					continue
				else:
					print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					pitch_result = "Grounder"
			else:
				print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				pitch_result == "Grounder"




			next_batter()
			if first == False and second == False and third == False:
				pitching_animation()
				print ("GROUND OUT!")
				out(1)	
			elif first == True and second == False and third == False and outs < 2:
				pitching_animation()
				print ("DOUBLE PLAY!")
				out(2)
			elif first == True and second == False and third == False and outs == 2:
				pitching_animation()
				print ("GROUND OUT!")
				out(1)
			elif first == False and second == True and third == False:
				pitching_animation()
				print ("GROUND OUT!")
				out(1)	
			elif first == False and second == False and third == True:
				pitching_animation()
				print ("GROUND OUT!")
				out(1)
			elif first == True and second == True and third == False and outs == 0:
				pitching_animation()
				print ("TRIPLE PLAY!")
				out(3)
			elif first == True and second == True and third == False and outs == 1:
				pitching_animation()
				print ("DOUBLE PLAY!")
				out(2)
			elif first == True and second == True and third == False and outs == 2:
				pitching_animation()
				print ("GROUND OUT!")
				out(1)	
			elif first == False and second == True and third == True:
				pitching_animation()
				print ("GROUND OUT!")
				out(1)
			elif first == True and second == True and third == True and outs == 0:
				pitching_animation()
				print ("TRIPLE PLAY!")
				out(3)
			elif first == True and second == True and third == True and outs == 1:
				pitching_animation()
				print ("DOUBLE PLAY!")
				out(2)
			elif first == True and second == True and third == True and outs == 2:
				pitching_animation()
				print ("GROUND OUT!")
				out(1)
			elif first == True and second == False and third == True and outs <2:
				pitching_animation()
				print ("DOUBLE PLAY!")
				out(2)    
			elif first == True and second == False and third == True and outs == 2:
				pitching_animation()
				print ("GROUND OUT!")
				out(1)
			resetcount()
			pitch_result = "Grounder"	
		elif 71 <= rand <= 87: #Single

			print(Style.DIM + "init: single" + Style.RESET_ALL) #DEBUG
			if edge_pos == "Pitcher":
				print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					#pitch_result = calculate_pitch_outcome(atbat_pitch_count, True)
					redo_pitch_loops = redo_pitch_loops + 1
					continue
				else:
					print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					pitch_result = "Single"
			else:
				print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				pitch_result == "Single"




			next_batter()
			pitching_animation()
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
			pitch_result = "Single"
		elif 88 <= rand <= 93: #Double



			print(Style.DIM + "init: double" + Style.RESET_ALL) #DEBUG
			if edge_pos == "Pitcher":
				print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					#pitch_result = calculate_pitch_outcome(atbat_pitch_count, True)
					redo_pitch_loops = redo_pitch_loops + 1
					continue
				else:
					print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					pitch_result = "Double"
			else:
				print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				pitch_result == "Double"




			next_batter()
			pitching_animation()
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
			pitch_result = "Double"



		elif 94 <= rand <= 98: #Home run
			
			
			

			print(Style.DIM + "init: home run" + Style.RESET_ALL) #DEBUG
			if edge_pos == "pitcher":
				print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					#pitch_result = calculate_pitch_outcome(atbat_pitch_count, True)
					redo_pitch_loops = redo_pitch_loops + 1
					continue
				else:
					print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					pitch_result = "Home run"
			else:
				print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				pitch_result == "Home run"



			
			
			next_batter()
			pitching_animation()
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
			pitch_result = "Home run"



		elif 97 <= rand <= 99: #Hit by pitch
			
			
			print(Style.DIM + "hit by pitch" + Style.RESET_ALL) #DEBUG
			if edge_pos == "pitcher":
				print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					#pitch_result = calculate_pitch_outcome(atbat_pitch_count, True)
					redo_pitch_loops = redo_pitch_loops + 1
					continue
				else:
					print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					pitch_result = "Hit by pitch"
			else:
				print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				pitch_result == "Hit by pitch"



			next_batter()
			pitching_animation()
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
			pitch_result = "Hit by pitch"


		elif rand == 100: #Triple
			
			
			

			print(Style.DIM + "init: triple" + Style.RESET_ALL) #DEBUG
			if edge_pos == "Batter":
				print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					#pitch_result = calculate_pitch_outcome(atbat_pitch_count, True)
					redo_pitch_loops = redo_pitch_loops + 1
					continue
				else:
					print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					pitch_result = "Triple"
			else:
				print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				pitch_result == "Triple"



			next_batter()
			pitching_animation()
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
			pitch_result = "Triple"

	atbat_pitch_count = atbat_pitch_count + 1
	redo_pitch_loops = 0

	if half_inning % 2 == 0:
		away_pitcher_pitch_count = away_pitcher_pitch_count + 1
	else:
		home_pitcher_pitch_count = home_pitcher_pitch_count + 1

	if pitch_result == "Walk" or pitch_result == "Single" or pitch_result == "Double" or pitch_result == "Triple" or pitch_result == "Home run" or pitch_result == "Hit by pitch" or pitch_result == "Strikeout" or pitch_result == "Grounder" or pitch_result == "Fly" or pitch_result == "Sacrifice fly":
		#at-bat is over
		atbat_pitch_count = 1
		print ("")

		check_if_pitching_change()

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

save_results = input("Save results to a text file? (Y/N)")
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
