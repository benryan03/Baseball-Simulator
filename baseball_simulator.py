#https://github.com/benryan03/baseball_simulator/

import random
import time
import math
from datetime import datetime

#To scrape players and stats from baseball-reference
from lxml import html
import requests

from colorama import init, Fore, Back, Style
init()

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
home_pitcher_pitch_count = 1
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
current_home_batter = -1

margin = 0
edge = ["", 0]

redo_pitch_loops = 0

runs_in_current_inning = 0

home_score_by_inning = []
away_score_by_inning = []

runners_on_base = [-1, -1, -1, -1]

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
	global runners_on_base
	for x in range (num):
		
		if half_inning % 2 == 0:
			away_pitchers_used[-1][2] = away_pitchers_used[-1][2] + .3333
		elif half_inning % 2 != 0:
			home_pitchers_used[-1][2] = home_pitchers_used[-1][2] + .3333

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
			runners_on_base = [-1, -1, -1, -1]
			balls = 0
			strikes = 0
			runs_in_current_inning = 0
			if half_inning == 2:
				print("\033[1;93;40m" + away_starting_pitcher[0] + "\033[0m is now pitching for the " + away_team + ".")
				#print("Starting pitcher for " + away_team + ": \033[1;93;40m" + away_starting_pitcher[0] + "\033[0m")
				wait()
				print(str(away_year) + " ERA: " + str(format_era(away_starting_pitcher[1])))
				wait()
		elif outs == 2 and half_inning >= 17 and half_inning % 2 != 0 and home_score <= away_score:
		# if 2 outs and 9th inning or later and end of top of inning and away team is ahead or tied
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
			runners_on_base = [-1, -1, -1, -1]
			balls = 0
			strikes = 0
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
			runners_on_base = [-1, -1, -1, -1]
			balls = 0
			strikes = 0
		else:
			gameover = True

		#elif outs == 2 and half_inning >= 17 and half_inning % 2 != 0 and home_score > away_score:
		# if 2 outs and 9th inning or later and end of top of inning and home team is ahead
		#	gameover = True
		#elif outs == 2 and half_inning >= 17 and half_inning % 2 == 0 and home_score > away_score:
		# if 2 outs and 9th inning or later and end of bottom of inning and home team is ahead
		#	gameover = True
		#elif outs == 2 and half_inning >= 17 and half_inning % 2 == 0 and home_score < away_score:
		# if 2 outs and 9th inning or later and end of bottom of inning and away team is ahead
		#	gameover = True

def run(num):
	global half_inning
	global away_score
	global home_score
	global gameover
	global runs_in_current_inning
	global home_score_by_inning
	global away_score_by_inning

	#print(str(runners_on_base)) #DEBUG

	runner1 = None
	runner2 = None
	runner3 = None
	runner4 = None

	#Determine and print who scored the run
	if half_inning % 2 != 0: #Top half
		if num == 1:
			if runners_on_base[3] > -1:
				away_batters[runners_on_base[3]][3] = away_batters[runners_on_base[3]][3] + 1
				runner1 = away_batters[runners_on_base[3]]

			elif runners_on_base[2] > -1:
				away_batters[runners_on_base[2]][3] = away_batters[runners_on_base[2]][3] + 1
				runner1 = away_batters[runners_on_base[2]]

			elif runners_on_base[1] > -1:
				away_batters[runners_on_base[1]][3] = away_batters[runners_on_base[1]][3] + 1

			elif runners_on_base[3] == -1 and runners_on_base[2] == -1 and runners_on_base[1] == -1:
				away_batters[current_away_batter][3] = away_batters[current_away_batter][3] + 1
				runner1 = away_batters[current_away_batter]

		elif num == 2:
			if runners_on_base[3] > -1 and runners_on_base[2] > -1:
				away_batters[runners_on_base[3]][3] = away_batters[runners_on_base[3]][3] + 1
				away_batters[runners_on_base[2]][3] = away_batters[runners_on_base[2]][3] + 1
				runner1 = away_batters[runners_on_base[3]]
				runner2 = away_batters[runners_on_base[2]]

			elif runners_on_base[3] > -1 and runners_on_base[1] > -1:
				away_batters[runners_on_base[3]][3] = away_batters[runners_on_base[3]][3] + 1
				away_batters[runners_on_base[1]][3] = away_batters[runners_on_base[1]][3] + 1
				runner1 = away_batters[runners_on_base[3]]
				runner2 = away_batters[runners_on_base[1]]

			elif runners_on_base[2] > -1 and runners_on_base[1] > -1:
				away_batters[runners_on_base[2]][3] = away_batters[runners_on_base[2]][3] + 1
				away_batters[runners_on_base[1]][3] = away_batters[runners_on_base[1]][3] + 1
				runner1 = away_batters[runners_on_base[2]]
				runner2 = away_batters[runners_on_base[1]]

			elif runners_on_base[3] > -1 and runners_on_base[2] == -1 and runners_on_base[1] == -1:
				away_batters[runners_on_base[3]][3] = away_batters[runners_on_base[3]][3] + 1
				away_batters[current_away_batter][3] = away_batters[current_away_batter][3] + 1
				runner1 = away_batters[runners_on_base[3]]
				runner2 = away_batters[current_away_batter]

			elif runners_on_base[3] == -1 and runners_on_base[2] > -1 and runners_on_base[1] == -1:
				away_batters[runners_on_base[2]][3] = away_batters[runners_on_base[2]][3] + 1
				away_batters[current_away_batter][3] = away_batters[current_away_batter][3] + 1
				runner1 = away_batters[runners_on_base[2]]
				runner2 = away_batters[current_away_batter]

			elif runners_on_base[3] == -1 and runners_on_base[2] == -1 and runners_on_base[1] > -1:
				away_batters[runners_on_base[1]][3] = away_batters[runners_on_base[1]][3] + 1
				away_batters[current_away_batter][3] = away_batters[current_away_batter][3] + 1
				runner1 = away_batters[runners_on_base[1]]
				runner2 = away_batters[current_away_batter]

		elif num == 3:
			if runners_on_base[3] > -1 and runners_on_base[2] > -1 and runners_on_base[1] > -1:
				away_batters[runners_on_base[3]][3] = away_batters[runners_on_base[3]][3] + 1
				away_batters[runners_on_base[2]][3] = away_batters[runners_on_base[2]][3] + 1
				away_batters[runners_on_base[1]][3] = away_batters[runners_on_base[1]][3] + 1
				runner1 = away_batters[runners_on_base[3]]
				runner2 = away_batters[runners_on_base[2]]
				runner3 = away_batters[runners_on_base[1]]

			elif runners_on_base[3] > -1 and runners_on_base[2] > -1:
				away_batters[runners_on_base[3]][3] = away_batters[runners_on_base[3]][3] + 1
				away_batters[runners_on_base[2]][3] = away_batters[runners_on_base[2]][3] + 1
				away_batters[current_away_batter][3] = away_batters[current_away_batter][3] + 1
				runner1 = away_batters[runners_on_base[3]]
				runner2 = away_batters[runners_on_base[2]]
				runner3 = away_batters[current_away_batter]

			elif runners_on_base[3] > -1 and runners_on_base[1] > -1:
				away_batters[runners_on_base[3]][3] = away_batters[runners_on_base[3]][3] + 1
				away_batters[runners_on_base[1]][3] = away_batters[runners_on_base[1]][3] + 1
				away_batters[current_away_batter][3] = away_batters[current_away_batter][3] + 1
				runner1 = away_batters[runners_on_base[3]]
				runner2 = away_batters[runners_on_base[1]]
				runner3 = away_batters[current_away_batter]

			elif runners_on_base[2] > -1 and runners_on_base[1] > -1:
				away_batters[runners_on_base[2]][3] = away_batters[runners_on_base[2]][3] + 1
				away_batters[runners_on_base[1]][3] = away_batters[runners_on_base[1]][3] + 1
				away_batters[current_away_batter][3] = away_batters[current_away_batter][3] + 1
				runner1 = away_batters[runners_on_base[2]]
				runner2 = away_batters[runners_on_base[1]]
				runner3 = away_batters[current_away_batter]

		elif num == 4:
			away_batters[runners_on_base[3]][3] = away_batters[runners_on_base[3]][3] + 1
			away_batters[runners_on_base[2]][3] = away_batters[runners_on_base[2]][3] + 1
			away_batters[runners_on_base[1]][3] = away_batters[runners_on_base[1]][3] + 1
			away_batters[current_away_batter][3] = away_batters[current_away_batter][3] + 1
			runner1 = away_batters[runners_on_base[3]]
			runner2 = away_batters[runners_on_base[2]]
			runner3 = away_batters[runners_on_base[1]]
			runner4 = away_batters[current_away_batter]

		if runner1 != None:
			wait_short()
			print("")
			wait_short()
			print ("\033[1;30;102m" + runner1[0] + " scored a run for the " + away_team + "!\033[0m")
		if runner2 != None:
			wait_short()
			print("")
			wait_short()
			print ("\033[1;30;102m" + runner2[0] + " scored a run for the " + away_team + "!\033[0m")
		if runner3 != None:
			wait_short()
			print("")
			wait_short()
			print ("\033[1;30;102m" + runner3[0] + " scored a run for the " + away_team + "!\033[0m")
		if runner4 != None:
			wait_short()
			print("")
			wait_short()
			print ("\033[1;30;102m" + runner4[0] + " scored a run for the " + away_team + "!\033[0m")

	elif half_inning % 2 == 0:
		if num == 1:
			if runners_on_base[3] > -1:
				home_batters[runners_on_base[3]][3] = home_batters[runners_on_base[3]][3] + 1
				runner1 = home_batters[runners_on_base[3]]
			elif runners_on_base[2] > -1:
				home_batters[runners_on_base[2]][3] = home_batters[runners_on_base[2]][3] + 1
				runner1 = home_batters[runners_on_base[2]]
			elif runners_on_base[1] > -1:
				home_batters[runners_on_base[1]][3] = home_batters[runners_on_base[1]][3] + 1
			elif runners_on_base[3] == -1 and runners_on_base[2] == -1 and runners_on_base[1] == -1:
				home_batters[current_home_batter][3] = home_batters[current_home_batter][3] + 1
				runner1 = home_batters[current_home_batter]
		elif num == 2:
			if runners_on_base[3] > -1 and runners_on_base[2] > -1:
				home_batters[runners_on_base[3]][3] = home_batters[runners_on_base[3]][3] + 1
				home_batters[runners_on_base[2]][3] = home_batters[runners_on_base[2]][3] + 1
				runner1 = home_batters[runners_on_base[3]]
				runner2 = home_batters[runners_on_base[2]]
			elif runners_on_base[3] > -1 and runners_on_base[1] > -1:
				home_batters[runners_on_base[3]][3] = home_batters[runners_on_base[3]][3] + 1
				home_batters[runners_on_base[1]][3] = home_batters[runners_on_base[1]][3] + 1
				runner1 = home_batters[runners_on_base[3]]
				runner2 = home_batters[runners_on_base[1]]
			elif runners_on_base[2] > -1 and runners_on_base[1] > -1:
				home_batters[runners_on_base[2]][3] = home_batters[runners_on_base[2]][3] + 1
				home_batters[runners_on_base[1]][3] = home_batters[runners_on_base[1]][3] + 1
				runner1 = home_batters[runners_on_base[2]]
				runner2 = home_batters[runners_on_base[1]]
			elif runners_on_base[3] > -1 and runners_on_base[2] == -1 and runners_on_base[1] == -1:
				home_batters[runners_on_base[3]][3] = home_batters[runners_on_base[3]][3] + 1
				home_batters[current_home_batter][3] = home_batters[current_home_batter][3] + 1
				runner1 = home_batters[runners_on_base[3]]
				runner2 = home_batters[current_home_batter]
			elif runners_on_base[3] == -1 and runners_on_base[2] > -1 and runners_on_base[1] == -1:
				home_batters[runners_on_base[2]][3] = home_batters[runners_on_base[2]][3] + 1
				home_batters[current_home_batter][3] = home_batters[current_home_batter][3] + 1
				runner1 = home_batters[runners_on_base[2]]
				runner2 = home_batters[current_home_batter]
			elif runners_on_base[3] == -1 and runners_on_base[2] == -1 and runners_on_base[1] > -1:
				home_batters[runners_on_base[1]][3] = home_batters[runners_on_base[1]][3] + 1
				home_batters[current_home_batter][3] = home_batters[current_home_batter][3] + 1
				runner1 = home_batters[runners_on_base[1]]
				runner2 = home_batters[current_home_batter]
		elif num == 3:
			if runners_on_base[3] > -1 and runners_on_base[2] > -1 and runners_on_base[1] > -1:
				home_batters[runners_on_base[3]][3] = home_batters[runners_on_base[3]][3] + 1
				home_batters[runners_on_base[2]][3] = home_batters[runners_on_base[2]][3] + 1
				home_batters[runners_on_base[1]][3] = home_batters[runners_on_base[1]][3] + 1
				runner1 = home_batters[runners_on_base[3]]
				runner2 = home_batters[runners_on_base[2]]
				runner3 = home_batters[runners_on_base[1]]
			elif runners_on_base[3] > -1 and runners_on_base[2] > -1:
				home_batters[runners_on_base[3]][3] = home_batters[runners_on_base[3]][3] + 1
				home_batters[runners_on_base[2]][3] = home_batters[runners_on_base[2]][3] + 1
				home_batters[current_home_batter][3] = home_batters[current_home_batter][3] + 1
				runner1 = home_batters[runners_on_base[3]]
				runner2 = home_batters[runners_on_base[2]]
				runner3 = home_batters[current_home_batter]
			elif runners_on_base[3] > -1 and runners_on_base[1] > -1:
				home_batters[runners_on_base[3]][3] = home_batters[runners_on_base[3]][3] + 1
				home_batters[runners_on_base[1]][3] = home_batters[runners_on_base[1]][3] + 1
				home_batters[current_home_batter][3] = home_batters[current_home_batter][3] + 1
				runner1 = home_batters[runners_on_base[3]]
				runner2 = home_batters[runners_on_base[1]]
				runner3 = home_batters[current_home_batter]
			elif runners_on_base[2] > -1 and runners_on_base[1] > -1:
				home_batters[runners_on_base[2]][3] = home_batters[runners_on_base[2]][3] + 1
				home_batters[runners_on_base[1]][3] = home_batters[runners_on_base[1]][3] + 1
				home_batters[current_home_batter][3] = home_batters[current_home_batter][3] + 1
				runner1 = home_batters[runners_on_base[2]]
				runner2 = home_batters[runners_on_base[1]]
				runner3 = home_batters[current_home_batter]
		elif num == 4:
			home_batters[runners_on_base[3]][3] = home_batters[runners_on_base[3]][3] + 1
			home_batters[runners_on_base[2]][3] = home_batters[runners_on_base[2]][3] + 1
			home_batters[runners_on_base[1]][3] = home_batters[runners_on_base[1]][3] + 1
			home_batters[current_home_batter][3] = home_batters[current_home_batter][3] + 1
			runner1 = home_batters[runners_on_base[3]]
			runner2 = home_batters[runners_on_base[2]]
			runner3 = home_batters[runners_on_base[1]]
			runner4 = home_batters[current_home_batter]

		if runner1 != None:
			wait_short()
			print("")
			wait_short()
			print ("\033[1;30;102m" + runner1[0] + " scored a run for the " + home_team + "!\033[0m")
		if runner2 != None:
			wait_short()
			print("")
			wait_short()
			print ("\033[1;30;102m" + runner2[0] + " scored a run for the " + home_team + "!\033[0m")
		if runner3 != None:
			wait_short()
			print("")
			wait_short()
			print ("\033[1;30;102m" + runner3[0] + " scored a run for the " + home_team + "!\033[0m")
		if runner4 != None:
			wait_short()
			print("")
			wait_short()
			print ("\033[1;30;102m" + runner4[0] + " scored a run for the " + home_team + "!\033[0m")
			
	for x in range (num):
		if half_inning % 2 != 0:
			#run for away - line score
			inning = int((half_inning/2) + .5)
			if len(away_score_by_inning) < inning:
				away_score_by_inning.append(1)
			else:
				away_score_by_inning[-1] = away_score_by_inning[-1] + 1



		elif half_inning % 2 == 0:
			#run for home - line score
			inning = int((half_inning/2) + .5)
			if len(home_score_by_inning) < inning:
				home_score_by_inning.append(1)
			else:
				home_score_by_inning[-1] = home_score_by_inning[-1] + 1


		if half_inning < 18 and half_inning % 2 != 0:
			#normal innings - run for away
			away_score = away_score + 1
			runs_in_current_inning = runs_in_current_inning + 1
			away_batters[current_away_batter][5] = away_batters[current_away_batter][5] + 1 #RBI count for box score
			#print ("\033[1;30;102mRun scored by " + away_team + "!\033[0m")
			#print ("Run scored by " + away_team + "!")
			wait_short()
		elif half_inning < 18 and half_inning % 2 == 0:
			#normal innings - run for home
			home_score = home_score + 1
			runs_in_current_inning = runs_in_current_inning + 1
			home_batters[current_home_batter][5] = home_batters[current_home_batter][5] + 1 #RBI count for box score
			#print ("\033[1;30;102mRun scored by " + home_team + "!\033[0m")
			#print ("Run scored by " + home_team + "!")
			wait_short()
		elif half_inning >= 18 and half_inning % 2 != 0: #odd/top of inning
			#extra innings - run for away
			away_score = away_score + 1
			runs_in_current_inning = runs_in_current_inning + 1
			away_batters[current_away_batter][5] = away_batters[current_away_batter][5] + 1 #RBI count for box score
			#print ("\033[1;30;102mRun scored by " + away_team + "!\033[0m")
			#print ("Run scored by " + away_team + "!")
			wait_short()
		elif half_inning >= 18 and half_inning % 2 == 0 and away_score > home_score: #even/bottom of inning
			#extra innings - run for home, no walkoff
			home_score = home_score + 1
			home_batters[current_home_batter][5] = home_batters[current_home_batter][5] + 1 #RBI count for box score
			#print ("\033[1;30;102mRun scored by " + home_team + "!\033[0m")
			#print ("Run scored by " + home_team + "!")
			runs_in_current_inning = runs_in_current_inning + 1
			wait_short()
		elif half_inning >= 18 and half_inning % 2 == 0 and away_score == home_score: #even/bottom of inning
			#walkoff run!
			home_score = home_score + 1
			home_batters[current_home_batter][5] = home_batters[current_home_batter][5] + 1 #RBI count for box score
			print ("\033[1;30;102mWALKOFF for the " + home_team + "!\033[0m")
			wait()
			print("")
			wait()
			#print ("WALKOFF RUN scored by " + home_team + "!")
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

	"""
	global runners_on_base
	if half_inning % 2 != 0:
		for x in runners_on_base:
			if x > -1:
				print(away_batters[x][0])
			else:
				print(str(x))
	elif half_inning % 2 == 0:
		for x in runners_on_base:
			if x > -1:
				print(home_batters[x][0])
			else:
				print(str(x))
	"""

	print("-------------------------------------------------------------")
	wait()
	print ("Outs: " + str(outs) + " | Inning: ", end ="")
	if half_inning % 2 != 0:
		print ("Top ", end ="")
	elif half_inning % 2 == 0:
		print ("Bot ", end ="")
	print (str(math.ceil(half_inning / 2)) + " | " + home_abbr + ": " + str(home_score) + " | " + away_abbr + ": " + str(away_score) + " | 3B: ", end ="")
	if third == True:
		print ("X 2B: ", end ="")
	elif third == False:
		print ("  2B: ", end ="")
	if second == True:
		print ("X 1B: ", end ="")
	elif second == False:
		print ("  1B: ", end ="")
	if first == True:
		print ("X")
	elif first == False:
		print (" ")

	wait()

	now_batting()
	
	wait()

def now_batting():
	global edge
	global edge_pos
	global margin
	global redo_pitch_loops
	






	if half_inning % 2 == 0:	
		print ("\033[1;93;40m" + str(home_batters[current_home_batter][0]) + "\033[0m is now batting for the " + home_team + ". " + str(home_year) + " AVG: " + format_batting_average(home_batters[current_home_batter][1]))
		home_batters[current_home_batter][2] = home_batters[current_home_batter][2] + 1 #At-bat count for box score
	else:
		print ("\033[1;93;40m" + str(away_batters[current_away_batter][0]) + "\033[0m is now batting for the " + away_team + ". " + str(home_year) + " AVG: " + format_batting_average(away_batters[current_away_batter][1]))
		away_batters[current_away_batter][2] = away_batters[current_away_batter][2] + 1 #At-bat count for box score

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
	time.sleep(0) # 2

def wait_short():
	time.sleep(0) # .5

def calculate_pitch_outcome(pitch, redo_pitch):
	global edge_pos
	global margin
	global redo_pitch_loops
	
	rand = random.randint(1, 100)



	"""
	pitch = 1
	if pitch == 1:
		if rand >= 1 and rand <= 25: #Ball
			#print(Style.DIM + "init: ball" + Style.RESET_ALL)
			if edge_pos == "Pitcher":
				#print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL)
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					#print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL)
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					#print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL)
					return "Ball"
			else:
				#print(Style.DIM + "No redo attempt" + Style.RESET_ALL)
				return "Ball"
		elif rand >=26 and rand <= 50: #Called Strike
			#print(Style.DIM + "init: called strike" + Style.RESET_ALL)
			if edge_pos == "Batter":
				#print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL)
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					#print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL)
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					#print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL)
					return "Strike"
			else:
				#print(Style.DIM + "No redo attempt" + Style.RESET_ALL)
				return "Strike"
		elif rand >= 51 and rand <= 75: #Foul
			#print(Style.DIM + "init: foul" + Style.RESET_ALL)
			if edge_pos == "Batter":
				#print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL)
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					#print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL)
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					#print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL)
					return "Foul"
			else:
				#print(Style.DIM + "No redo attempt" + Style.RESET_ALL)
				return "Foul"
		else: #Ball in play
			#print(Style.DIM + "init: ballinplay" + Style.RESET_ALL)
			if edge_pos == "Pitcher":
				#print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL)
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					#print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL)
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					#print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL)
					return "Ball_in_play"
			else:
				#print(Style.DIM + "No redo attempt" + Style.RESET_ALL)
				return "Ball_in_play"
	"""

	
	if pitch == 1:
		if rand >= 1 and rand <= 43: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >=44 and rand <= 72: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 73 and rand <= 82: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 83 and rand <= 88: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 2:
		if rand >= 1 and rand <= 40: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >=41 and rand <= 56: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 57 and rand <= 72: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 73 and rand <= 81: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 3:
		if rand >= 1 and rand <= 39: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >=40 and rand <= 52: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 53 and rand <= 70: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 71 and rand <= 80: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 4:
		if rand >= 1 and rand <= 35: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >=36 and rand <= 47: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 48 and rand <= 68: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 69 and rand <= 80: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 5:
		if rand >= 1 and rand <= 31: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >=32 and rand <= 40: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 41 and rand <= 61: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 62 and rand <= 73: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 6:
		if rand >= 1 and rand <= 26: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >=27 and rand <= 30: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 31 and rand <= 53: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 54 and rand <= 65: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 7:
		if rand >= 1 and rand <= 25: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >=26 and rand <= 29: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 30 and rand <= 57: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 58 and rand <= 69: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 8:
		if rand >= 1 and rand <= 24: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >=25 and rand <= 28: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 29 and rand <= 57: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 58 and rand <= 68: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 9:
		if rand >= 1 and rand <= 23: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >=24 and rand <= 26: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 27 and rand <= 57: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 58 and rand <= 68: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 10:
		if rand >= 1 and rand <= 22: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >= 23 and rand <= 25: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 26 and rand <= 57: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 58 and rand <= 68: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 11:
		if rand >= 1 and rand <= 22: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >=23 and rand <= 25: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 26 and rand <= 57: #Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 58 and rand <= 68: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 12:
		if rand >= 1 and rand <= 28: #Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >=29 and rand <= 40: #Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 41 and rand <= 58: #Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Strike"
			else:
				return "Strike"
		else: #Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					redo_pitch_loops = redo_pitch_loops + 1
					return calculate_pitch_outcome(pitch, True)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"

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

	print ("\033[1;30;40mPitch " + str(current_pitcher_pitch_count) + " (" + current_pitcher[0] + ") \033[0m", end="", flush=True)	# flush=True needs to be included, otherwise time.sleep instances will occur all at once
	for x in range (0, 3):
		wait_short()
		print ("\033[1;30;40m. \033[0m", end="", flush=True)

	for x in range (0, redo_pitch_loops):
		wait_short()
		print ("\033[1;30;40m. \033[0m", end="", flush=True)

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
			if home_score > 4:
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

		if half_inning == 17:
			current_home_pitcher = home_closer

		home_pitchers_used.append(current_home_pitcher)
		for x in range(10):
			home_pitchers_used[-1].append(0)

		wait()
		print("Pitching change!")
		wait()
		print("")
		wait()
		print("\033[1;93;40m" + current_home_pitcher[0] + "\033[0m is now pitching for the " + home_team + ".")
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

		if half_inning == 18:
			current_away_pitcher = away_closer

		away_pitchers_used.append(current_away_pitcher)
		for x in range(10):
			away_pitchers_used[-1].append(0)

		wait()
		print("Pitching change!")
		wait()
		print("")
		wait()
		print("\033[1;93;40m" + current_away_pitcher[0] + "\033[0m is now pitching for the " + away_team + ".")
		wait()
		print(str(away_year) + " ERA: " + str(format_era(current_away_pitcher[1])))
		wait()
		print("")
		wait()

def inning_status():
	global half_inning

	prev_half_inning = half_inning - 1






	if prev_half_inning % 2 == 0:
		#it is now bottom
		if len(away_score_by_inning) < prev_half_inning-1:
			away_score_by_inning.append(0)

	elif prev_half_inning % 2 != 0:
		#it is now top
		if len(home_score_by_inning) < prev_half_inning-1:
			home_score_by_inning.append(0)




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
		print("")
		print("------------------------------------")
		print ("It is now the top of the " + str((half_inning/2) + .5).split(".")[0] + x + " inning.")
		print("------------------------------------")
		print("")
		wait()

	elif half_inning % 2 == 0:
		wait()
		print("")
		print("")
		print("---------------------------------------")
		print ("It is now the bottom of the " + str(half_inning/2).split(".")[0] + x + " inning.")
		print("---------------------------------------")
		print("")
		#print("")
		wait()

def parse_input(input_team):
		
	input_team = input_team.lower().strip()

	if input_team == "arizona diamondbacks" or input_team == "arizona" or input_team == "diamondbacks" or input_team == "ari":
		return "Diamondbacks,ARI"
	elif input_team == "atlanta braves" or input_team == "atlanta" or input_team == "braves" or input_team == "atl":
		return "Braves,ATL"
	elif input_team == "baltimore" or input_team == "orioles" or input_team == "baltimore" or input_team == "orioles" or input_team == "bal":
		return "Orioles,BAL"
	elif input_team == "boston red sox" or input_team == "boston" or input_team == "red sox" or input_team == "bos":
		return "Red Sox,BOS"
	elif input_team == "chicago cubs" or input_team == "cubs" or input_team == "chc":
		return "Cubs,CHC"
	elif input_team == "chicago white sox" or input_team == "white sox" or input_team == "chw":
		return "White Sox,CHW"
	elif input_team == "cincinnati reds" or input_team == "cincinnati" or input_team == "reds" or input_team == "cin":
		return "Reds,CIN"
	elif input_team == "cleveland indians" or input_team == "cleveland" or input_team == "indians" or input_team == "cle":
		return "Indians,CLE"
	elif input_team == "colorado rockies" or input_team == "colorado" or input_team == "rockies" or input_team == "col":
		return "Rockies,COL"
	elif input_team == "detroit tigers" or input_team == "detroit" or input_team == "tigers" or input_team == "det":
		return "Tigers,DET"
	elif input_team == "houston astros" or input_team == "houston" or input_team == "astros" or input_team == "hou":
		return "Astros,HOU"
	elif input_team == "kansas city royals" or input_team == "kansas city" or input_team == "royals" or input_team == "kcr":
		return "Royals,KCR"
	elif input_team == "los angeles angels" or input_team == "anaheim angels" or input_team == "anaheim" or input_team == "angels" or input_team == "ana":
		return "Angels,ANA"
	elif input_team == "los angeles dodgers" or input_team == "los angeles" or input_team == "dodgers" or input_team == "lad":
		return "Dodgers,LAD"
	elif input_team == "miami marlins" or input_team == "florida marlins" or input_team == "miami" or input_team == "florida" or input_team == "marlins" or input_team == "fla":
		return "Marlins,FLA"
	elif input_team == "milwaukee brewers" or input_team == "milwaukee" or input_team == "brewers" or input_team == "mil":
		return "Brewers,MIL"
	elif input_team == "minnesota twins" or input_team == "minnesota" or input_team == "twins" or input_team == "min":
		return "Twins,MIN"
	elif input_team == "new york mets" or input_team == "mets" or input_team == "nym":
		return "Mets,NYM"
	elif input_team == "new york yankees" or input_team == "yankees" or input_team == "nyy":
		return "Yankees,NYY"
	elif input_team == "oakland athletics" or input_team == "oakland" or input_team == "athletics" or input_team == "as" or input_team == "a's" or input_team == "oak":
		return "Athletics,OAK"
	elif input_team == "philadelphia phillies" or input_team == "philadelphia" or input_team == "phillies" or input_team == "phi":
		return "Phillies,PHI"
	elif input_team == "pittsburgh pirates" or input_team == "pittsburgh" or input_team == "pirates" or input_team == "pit":
		return "Pirates,PIT"
	elif input_team == "san diego padres" or input_team == "san diego" or input_team == "padres" or input_team == "sdp":
		return "Padres,SDP"
	elif input_team == "san francisco giants" or input_team == "san francisco" or input_team == "giants" or input_team == "sfg":
		return "Giants,SFG"
	elif input_team == "seattle mariners" or input_team == "seattle" or input_team == "mariners" or input_team == "sea":
		return "Mariners,SEA"
	elif input_team == "st louis cardinals" or input_team == "st. louis cardinals" or input_team == "st louis" or input_team == "st. louis" or input_team == "cardinals" or input_team == "stl":
		return "Cardinals,STL"
	elif input_team == "tampa bay rays" or input_team == "tampa bay" or input_team == "rays" or input_team == "tampa bay devil rays" or input_team == "devil rays" or input_team == "tbd":
		return "Rays,TBD"
	elif input_team == "texas rangers" or input_team == "texas" or input_team == "rangers" or input_team == "tex":
		return "Rangers,TEX"
	elif input_team == "toronto blue jays" or input_team == "toronto" or input_team == "blue jays" or input_team == "tor":
		return "Blue Jays,TOR"
	elif input_team == "washington nationals" or input_team == "washington" or input_team == "nationals" or input_team == "wsn":
		return "Nationals,WSN"
	else:
		return "invalid"

#######################################################################################################################
#######################################################################################################################

#program start

home_team = "Red Sox" #debug
home_abbr = "BOS" #debug
home_year = "2018" #debug
away_team = "Yankees" #debug
away_abbr = "NYY" #debug
away_year = "2018" #debug

print ("Welcome to Baseball Simulator")
"""
home_team = ""
home_abbr = ""
home_team_error = True
while home_team_error == True:
	home_team = input("Enter the name of the home team: ")
	if parse_input(home_team) == "invalid":
		print("Invalid team.")
		continue
	else:
		home_team = parse_input(home_team).split(",")[0]
		home_abbr = parse_input(home_team).split(",")[1]
		home_team_error = False

home_year = 0
home_year_error = True
while home_year_error == True:
	home_year = input("Enter year: ")
	home_page = requests.get("https://www.baseball-reference.com/teams/" + home_abbr + "/" + home_year + ".shtml")
	if str(home_page) != "<Response [200]>":
		print("Invalid year.")
		continue
	else:
		home_year_error = False

away_team = ""
away_abbr = ""
away_team_error = True
while away_team_error == True:
	away_team = input("Enter the name of the away team: ")
	if parse_input(away_team) == "invalid":
		print("Invalid team.")
		continue
	else:
		away_team = parse_input(away_team).split(",")[0]
		away_abbr = parse_input(away_team).split(",")[1]
		away_team_error = False

away_year = 0
away_year_error = True
while away_year_error == True:
	away_year = input("Enter year: ")
	away_page = requests.get("https://www.baseball-reference.com/teams/" + away_abbr + "/" + away_year + ".shtml")
	if str(away_page) != "<Response [200]>":
		print("Invalid year.")
		continue
	else:
		away_year_error = False
"""
print("")
print("Loading players...")

#Load baseball-reference page for inputted team/year
#URL format: https://www.baseball-reference.com/teams/BOS/2004.shtml
home_page = requests.get("https://www.baseball-reference.com/teams/" + home_abbr + "/" + home_year + ".shtml")
home_tree = html.fromstring(home_page.content)
away_page = requests.get("https://www.baseball-reference.com/teams/" + away_abbr + "/" + away_year + ".shtml")
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

#Empty stats for box score
for x in range(9):
	home_batters[x].append(0)
	home_batters[x].append(0)
	home_batters[x].append(0)
	home_batters[x].append(0)
	home_batters[x].append(0)
	home_batters[x].append(0)
	home_batters[x].append(0)
	away_batters[x].append(0)
	away_batters[x].append(0)
	away_batters[x].append(0)
	away_batters[x].append(0)
	away_batters[x].append(0)
	away_batters[x].append(0)
	away_batters[x].append(0)

#Sort array by batting average
home_batters = sorted(home_batters, key=lambda x: x[1], reverse=True)
away_batters = sorted(away_batters, key=lambda x: x[1], reverse=True)

home_pitchers = [[[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], ]
away_pitchers = [[[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]], ]

home_relief_pitchers = [[[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]]]
away_relief_pitchers = [[[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]]]

home_closer = ["", 0]
away_closer = ["", 0]

home_pitchers_used = []
away_pitchers_used = []


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


print("\nStarting lineup for the " + home_team + ":")
#wait()
for x in home_batters:
	print(x[0] + " - " + format_batting_average(x[1]))
#	wait()

print("\nStarting lineup for the " + away_team + ":")
#wait()
for x in away_batters:
	print(x[0] + " - " + format_batting_average(x[1]))
#	wait()

#print("")
#for x in home_pitchers:
#	print(x)
#print("")
#for x in away_pitchers:
#	print(x)

#print("")
#for x in home_relief_pitchers:
#	print(x)
#print("")
#for x in away_relief_pitchers:
#	print(x)

#print("")
#print(home_team + " closer: " + home_closer[0] + " - " + str(home_closer[1]))
#print(away_team + " closer: " + away_closer[0] + " - " + str(away_closer[1]))


#Generate starting pitchers
pitcher_rand = random.randint(0, 4)
home_starting_pitcher = home_pitchers[pitcher_rand]
pitcher_rand = random.randint(0, 4)
away_starting_pitcher = away_pitchers[pitcher_rand]

current_home_pitcher = home_starting_pitcher
current_away_pitcher = away_starting_pitcher

#For end-of-game box score
home_pitchers_used.append(home_starting_pitcher)
for x in range(10):
	home_pitchers_used[-1].append(0)

away_pitchers_used.append(away_starting_pitcher)
for x in range(10):
	away_pitchers_used[-1].append(0)

wait()
print("")
wait()
print("PLAY BALL!")
wait()
print("")
wait()
print("\033[1;93;40m" + home_starting_pitcher[0] + "\033[0m is now pitching for the " + home_team + ".")
wait()
print(str(home_year) + " ERA: " + str(format_era(home_starting_pitcher[1])))
wait()
print()
wait()

status()

first_pitch_time = ((datetime.strftime(datetime.now(), "%Y")) + "-" + (datetime.strftime(datetime.now(), "%m")) + "-" + (datetime.strftime(datetime.now(), "%d")) + " at " + (datetime.strftime(datetime.now(), "%H")) + ":" + (datetime.strftime(datetime.now(), "%M")))


while gameover == False: #main game loop

	pitch_result = calculate_pitch_outcome(atbat_pitch_count, False)

	if pitch_result == "Ball":
		if balls < 3:
			balls = balls + 1
			pitching_animation()
			print ("Ball. (" + str(balls) + " - " + str(strikes) + ")")

		elif balls == 3: #Walk
			pitch_result = "Walk"
			pitching_animation()
			print ("\033[1;30;102mWALK!\033[0m")
			if first == False and second == False and third == False:
				first = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[1] = current_home_batter
			elif first == True and second == False and third == False:
				second = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_home_batter
			elif first == False and second == True and third == False:
				first = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[1] = current_home_batter
			elif first == False and second == False and third == True:
				first = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[1] = current_home_batter
			elif first == True and second == True and third == False:
				third = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = runners_on_base[2]
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = runners_on_base[2]
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_home_batter
			elif first == False and second == True and third == True:
				first = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[1] = current_home_batter
			elif first == True and second == True and third == True:
				run(1)
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = runners_on_base[2]
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = runners_on_base[2]
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_home_batter
			elif first == True and second == False and third == True:
				second = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_home_batter
			if half_inning % 2 != 0: #if top of inning
				#away_walk_count = away_walk_count + 1
				away_batters[current_away_batter][7] = away_batters[current_away_batter][7] + 1 #At-bat count for box score
			elif half_inning % 2 ==	0: # if bottom of inning
				#home_walk_count = home_walk_count + 1
				home_batters[current_home_batter][7] = home_batters[current_home_batter][7] + 1 #At-bat count for box score
			resetcount()
			#next_batter()

	elif pitch_result == "Strike":
		if strikes <2: #Strike
			strikes = strikes + 1
			pitching_animation()
			print ("Strike. (" + str(balls) + " - " + str(strikes) + ")")

		elif strikes ==2 and half_inning % 2 != 0: #Strikeout - away
			pitching_animation()
			print ("\033[1;97;101mSTRIKEOUT!\033[0m")
			pitch_result = "Strikeout"
			away_strikeout_count = away_strikeout_count + 1
			away_batters[current_away_batter][8] = away_batters[current_away_batter][8] + 1 #At-bat count for box score
			out(1)
			#next_batter()

		elif strikes ==2 and half_inning % 2 == 0: #Strikeout - home
			pitching_animation()
			print ("\033[1;97;101mSTRIKEOUT!\033[0m")
			#print ("STRIKEOUT!")
			pitch_result = "Strikeout"
			home_strikeout_count = home_strikeout_count + 1
			home_batters[current_home_batter][8] = home_batters[current_home_batter][8] + 1 #At-bat count for box score
			out(1)
			#next_batter()

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
			
			#print(Style.DIM + "init: fly out" + Style.RESET_ALL) #DEBUG
			if edge_pos == "Batter":
				#print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					#print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					redo_pitch_loops = redo_pitch_loops + 1
					continue
				else:
					#print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					pitch_result = "Fly"
			else:
				#print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				pitch_result == "Fly"




			
			#next_batter()
			if first == False and second == False and third == False:
				pitching_animation()
				print ("\033[1;97;101mFLY OUT!\033[0m")
				out(1)
			elif first == True and second == False and third == False:
				pitching_animation()
				print ("\033[1;97;101mFLY OUT!\033[0m")
				out(1)
			elif first == False and second == True and third == False and outs < 2:
				pitching_animation()
				print ("\033[1;30;103mFLY OUT! RUNNER ADVANCED.\033[0m")
				second = False
				third = True
				out(1)
				runners_on_base[3] = runners_on_base[2]
				runners_on_base[2] = -1
			elif first == False and second == True and third == False and outs == 2:
				pitching_animation()
				print ("\033[1;97;101mFLY OUT!\033[0m")
				out(1)
			elif first == False and second == False and third == True and outs < 2:
				pitching_animation()
				print ("\033[1;30;102mSACRIFICE FLY!\033[0m")
				third = False
				out(1)
				run(1)
				runners_on_base[3] = -1
			elif first == False and second == False and third == True and outs == 2:
				pitching_animation()
				print ("\033[1;97;101mFLY OUT!\033[0m")
				out(1)
			elif first == True and second == True and third == False and outs < 2:
				pitching_animation()
				print ("\033[1;30;103mFLY OUT! RUNNER ADVANCED.\033[0m")
				second = False
				third = True
				out(1)
				runners_on_base[3] = runners_on_base[2]
				runners_on_base[2] = -1
			elif first == True and second == True and third == False and outs == 2:
				pitching_animation()
				print ("\033[1;97;101mFLY OUT!\033[0m")
				out(1)
			elif first == False and second == True and third == True and outs < 2:
				pitching_animation()
				print ("\033[1;30;102mSACRIFICE FLY!\033[0m")
				third = False
				out(1)
				run(1)				
				runners_on_base[3] = -1
			elif first == False and second == True and third == True and outs == 2:
				pitching_animation()
				print ("\033[1;97;101mFLY OUT!\033[0m")
				out(1)
			elif first == True and second == False and third == True and outs < 2:
				pitching_animation()
				print ("\033[1;30;102mSACRIFICE FLY!\033[0m")
				third = False
				out(1)
				run(1)
				runners_on_base[3] = -1
			elif first == True and second == False and third == True and outs == 2:
				pitching_animation()
				print ("\033[1;97;101mFLY OUT!\033[0m")
				out(1)
			elif first == True and second == True and third == True and outs < 2:
				pitching_animation()
				print ("\033[1;30;102mSACRIFICE FLY!\033[0m")
				third = False
				out(1)
				run(1)
				runners_on_base[3] = -1
			elif first == True and second == True and third == True and outs < 2:
				pitching_animation()
				print ("\033[1;97;101mFLY OUT!\033[0m")
				out(1)
			resetcount()
			pitch_result = "Fly"
		elif 41 <= rand <= 70: #Ground out

			#print(Style.DIM + "init: ground out" + Style.RESET_ALL) #DEBUG
			if edge_pos == "Batter":
				#print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					#print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					redo_pitch_loops = redo_pitch_loops + 1
					continue
				else:
					#print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					pitch_result = "Grounder"
			else:
				#print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				pitch_result == "Grounder"




			#next_batter()
			if first == False and second == False and third == False:
				pitching_animation()
				print ("\033[1;97;101mGROUND OUT!\033[0m")
				out(1)	
			elif first == True and second == False and third == False and outs < 2:
				pitching_animation()
				print ("\033[1;97;101mDOUBLE PLAY!\033[0m")
				out(2)
				first = False
				runners_on_base[1] = -1
			elif first == True and second == False and third == False and outs == 2:
				pitching_animation()
				print ("\033[1;97;101mGROUND OUT!\033[0m")
				out(1)
			elif first == False and second == True and third == False:
				pitching_animation()
				print ("\033[1;97;101mGROUND OUT!\033[0m")
				out(1)	
			elif first == False and second == False and third == True:
				pitching_animation()
				print ("\033[1;97;101mGROUND OUT!\033[0m")
				out(1)
			elif first == True and second == True and third == False and outs == 0:
				pitching_animation()
				print ("\033[1;97;101mTRIPLE PLAY\033[0m")
				out(3)
			elif first == True and second == True and third == False and outs == 1:
				pitching_animation()
				print ("\033[1;97;101mDOUBLE PLAY!\033[0m")
				out(2)
			elif first == True and second == True and third == False and outs == 2:
				pitching_animation()
				print ("\033[1;97;101mGROUND OUT!\033[0m")
				out(1)	
			elif first == False and second == True and third == True:
				pitching_animation()
				print ("\033[1;97;101mGROUND OUT!\033[0m")
				out(1)
			elif first == True and second == True and third == True and outs == 0:
				pitching_animation()
				print ("\033[1;97;101mTRIPLE PLAY!\033[0m")
				out(3)
			elif first == True and second == True and third == True and outs == 1:
				pitching_animation()
				print ("\033[1;97;101mDOUBLE PLAY!\033[0m")
				out(2)
			elif first == True and second == True and third == True and outs == 2:
				pitching_animation()
				print ("\033[1;97;101mGROUND OUT!\033[0m")
				out(1)
			elif first == True and second == False and third == True and outs <2:
				pitching_animation()
				print ("\033[1;97;101mDOUBLE PLAY!\033[0m")
				out(2)    
				first = False
				runners_on_base[1] = -1
			elif first == True and second == False and third == True and outs == 2:
				pitching_animation()
				print ("\033[1;97;101mGROUND OUT!\033[0m")
				out(1)
			resetcount()
			pitch_result = "Grounder"	
		elif 71 <= rand <= 87: #Single

			#print(Style.DIM + "init: single" + Style.RESET_ALL) #DEBUG
			if edge_pos == "Pitcher":
				#print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					#print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					redo_pitch_loops = redo_pitch_loops + 1
					continue
				else:
					#print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					pitch_result = "Single"
			else:
				#print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				pitch_result == "Single"




			#next_batter()
			pitching_animation()
			print ("\033[1;30;102mSINGLE!\033[0m")
			if first == False and second == False and third == False:
				first = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[1] = current_home_batter
			elif first == True and second == False and third == False:
				second = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_home_batter
			elif first == False and second == True and third == False:
				first = True
				second = False
				third = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = runners_on_base[2]
					runners_on_base[2] = -1
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = runners_on_base[2]
					runners_on_base[2] = -1
					runners_on_base[1] = current_home_batter
			elif first == False and second == False and third == True:
				first = True
				third = False
				run(1)
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = -1
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = -1
					runners_on_base[1] = current_home_batter
			elif first == True and second == True and third == False:
				third = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = runners_on_base[2]
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = runners_on_base[2]
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_home_batter
			elif first == False and second == True and third == True:
				first = True
				second = False
				run(1)
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = runners_on_base[2]
					runners_on_base[2] = -1
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = runners_on_base[2]
					runners_on_base[2] = -1
					runners_on_base[1] = current_home_batter
			elif first == True and second == True and third == True:
				run(1)
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = runners_on_base[2]
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = runners_on_base[2]
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_home_batter
			elif first == True and second == False and third == True:
				second = True
				third = False
				run(1)
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = -1
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = -1
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_home_batter

			if half_inning % 2 != 0: #if top of inning
				away_single_count = away_single_count + 1
				away_batters[current_away_batter][4] = away_batters[current_away_batter][4] + 1 #Hit count for box score
				home_pitchers_used[-1][4] = home_pitchers_used[-1][3] + 1
			elif half_inning % 2 ==	0: # if bottom of inning
				home_single_count = home_single_count + 1
				home_batters[current_home_batter][4] = home_batters[current_home_batter][4] + 1 #Hit count for box score
				away_pitchers_used[-1][4] = away_pitchers_used[-1][3] + 1

			resetcount()
			pitch_result = "Single"
		elif 88 <= rand <= 93: #Double



			#print(Style.DIM + "init: double" + Style.RESET_ALL) #DEBUG
			if edge_pos == "Pitcher":
				#print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					#print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					redo_pitch_loops = redo_pitch_loops + 1
					continue
				else:
					#print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					pitch_result = "Double"
			else:
				#print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				pitch_result == "Double"




			#next_batter()
			pitching_animation()
			print ("\033[1;30;102mDOUBLE!\033[0m")
			if first == False and second == False and third == False:
				second = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[2] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[2] = current_home_batter
			elif first == True and second == False and third == False:
				first = False
				second = True
				third = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = runners_on_base[1]
					runners_on_base[2] = current_away_batter
					runners_on_base[1] = -1
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = runners_on_base[1]
					runners_on_base[2] = current_home_batter
					runners_on_base[1] = -1
			elif first == False and second == True and third == False:
				run(1)
				runners_on_base[2] = -1
			elif first == False and second == False and third == True:
				run(1)
				third = False
				second = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = -1
					runners_on_base[2] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = -1
					runners_on_base[2] = current_home_batter
			elif first == True and second == True and third == False:
				first = False
				run(2)
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[2] = current_away_batter
					runners_on_base[1] = -1
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[2] = current_home_batter
					runners_on_base[1] = -1
			elif first == False and second == True and third == True:
				third = False
				run(2)
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[2] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[2] = current_home_batter
			elif first == True and second == True and third == True:
				first = False
				third = False
				run(3)
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = runners_on_base[1]
					runners_on_base[2] = current_away_batter
					runners_on_base[1] = -1
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = runners_on_base[1]
					runners_on_base[2] = current_home_batter
					runners_on_base[1] = -1
			elif first == True and second == False and third == True:
				second = True
				first = False
				third = False
				run(2)
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = runners_on_base[1]
					runners_on_base[2] = current_away_batter
					runners_on_base[1] = -1
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = runners_on_base[1]
					runners_on_base[2] = current_home_batter
					runners_on_base[1] = -1
			if half_inning % 2 != 0: #if top of inning
				away_double_count = away_double_count + 1
				away_batters[current_away_batter][4] = away_batters[current_away_batter][4] + 1 #Hit count for box score
			elif half_inning % 2 ==	0: # if bottom of inning
				home_double_count = home_double_count + 1
				home_batters[current_home_batter][4] = home_batters[current_home_batter][4] + 1 #Hit count for box score
				resetcount()
			pitch_result = "Double"
		elif 94 <= rand <= 98: #Home run
			
			
			

			#print(Style.DIM + "init: home run" + Style.RESET_ALL) #DEBUG
			if edge_pos == "pitcher":
				#print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					#print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					redo_pitch_loops = redo_pitch_loops + 1
					continue
				else:
					#print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					pitch_result = "Home run"
			else:
				#print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				pitch_result == "Home run"




			
			#next_batter()
			pitching_animation()
			print ("\033[1;30;102mHOME RUN!\033[0m")
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
				run(2)
			elif first == True and second == True and third == False:
				first = False
				second = False
				run(3)
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
				away_batters[current_away_batter][4] = away_batters[current_away_batter][4] + 1 #Hit count for box score
				away_batters[current_away_batter][6] = away_batters[current_away_batter][6] + 1 #HR count for box score
			elif half_inning % 2 ==	0: # if bottom of inning
				home_homerun_count = home_homerun_count + 1
				home_batters[current_home_batter][4] = home_batters[current_home_batter][4] + 1 #Hit count for box score
				home_batters[current_home_batter][6] = home_batters[current_home_batter][6] + 1 #HR count for box score
			resetcount()
			pitch_result = "Home run"

			runners_on_base[1] = -1
			runners_on_base[2] = -1
			runners_on_base[3] = -1

		elif 97 <= rand <= 99: #Hit by pitch
			
			
			#print(Style.DIM + "hit by pitch" + Style.RESET_ALL) #DEBUG
			if edge_pos == "pitcher":
				#print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					#print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					redo_pitch_loops = redo_pitch_loops + 1
					continue
				else:
					#print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					pitch_result = "Hit by pitch"
			else:
				#print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				pitch_result == "Hit by pitch"



			#next_batter()
			pitching_animation()
			print ("\033[1;30;102mHIT BY PITCH!\033[0m")
			if first == False and second == False and third == False:
				first = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[1] = current_home_batter
			elif first == True and second == False and third == False:
				second = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_home_batter
			elif first == False and second == True and third == False:
				first = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[1] = current_home_batter
			elif first == False and second == False and third == True:
				first = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[1] = current_home_batter
			elif first == True and second == True and third == False:
				third = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = runners_on_base[2]
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = runners_on_base[2]
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_home_batter
			elif first == False and second == True and third == True:
				first = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[1] = current_home_batter
			elif first == True and second == True and third == True:
				run(1)
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = runners_on_base[2]
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = runners_on_base[2]
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_home_batter
			elif first == True and second == False and third == True:
				second = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[2] = runners_on_base[1]
					runners_on_base[1] = current_home_batter
			if half_inning % 2 != 0: #if top of inning
				away_hbp_count = away_hbp_count + 1
			elif half_inning % 2 ==	0: # if bottom of inning
				home_hbp_count = home_hbp_count + 1
			resetcount()
			pitch_result = "Hit by pitch"
		elif rand == 100: #Triple
			
			
			

			#print(Style.DIM + "init: triple" + Style.RESET_ALL) #DEBUG
			if edge_pos == "Batter":
				#print(Style.DIM + "Calculating whether to redo" + Style.RESET_ALL) #DEBUG
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin,0):
					#print(Style.DIM + "Redo pitch SUCCEEDED" + Style.RESET_ALL) #DEBUG
					redo_pitch_loops = redo_pitch_loops + 1
					continue
				else:
					#print(Style.DIM + "Redo pitch FAILED - " + str(rand) + ", " + str(round(margin,0)) + Style.RESET_ALL) #DEBUG
					pitch_result = "Triple"
			else:
				#print(Style.DIM + "No redo attempt" + Style.RESET_ALL) #DEBUG
				pitch_result == "Triple"



			#next_batter()
			pitching_animation()
			print ("\033[1;30;102mTRIPLE!\033[0m")
			if first == False and second == False and third == False:
				third = True
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = current_away_batter
			elif first == True and second == False and third == False:
				first = False
				third = True
				run(1)
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = current_away_batter
					runners_on_base[1] = -1
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = current_away_batter
					runners_on_base[1] = -1
			elif first == False and second == True and third == False:
				third = True
				second = False
				run(1)
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = current_away_batter
					runners_on_base[2] = -1
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = current_away_batter
					runners_on_base[2] = -1
			elif first == False and second == False and third == True:
				run(1)
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = current_away_batter
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = current_away_batter
			elif first == True and second == True and third == False:
				third = True
				first = False
				second = False
				run(2)
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = current_away_batter
					runners_on_base[2] = -1
					runners_on_base[1] = -1
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = current_away_batter
					runners_on_base[2] = -1
					runners_on_base[1] = -1
			elif first == False and second == True and third == True:
				second = False
				run(2)
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = current_away_batter
					runners_on_base[2] = -1
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = current_away_batter
					runners_on_base[2] = -1
			elif first == True and second == True and third == True:
				first = False
				second = False
				third = True
				run(3)
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = current_away_batter
					runners_on_base[2] = -1
					runners_on_base[1] = -1
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = current_away_batter
					runners_on_base[2] = -1
					runners_on_base[1] = -1
			elif first == True and second == False and third == True:
				first = False
				run(2)
				if half_inning % 2 != 0: #if top of inning
					runners_on_base[3] = current_away_batter
					runners_on_base[1] = -1
				elif half_inning % 2 == 0: #if bottom of inning
					runners_on_base[3] = current_away_batter
					runners_on_base[1] = -1
			if half_inning % 2 != 0: #if top of inning
				away_triple_count = away_triple_count + 1
				away_batters[current_away_batter][4] = away_batters[current_away_batter][4] + 1 #Hit count for box score
			elif half_inning % 2 ==	0: # if bottom of inning
				home_triple_count = home_triple_count + 1
				home_batters[current_home_batter][4] = home_batters[current_home_batter][4] + 1 #Hit count for box score
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
		next_batter()
		atbat_pitch_count = 1
		print ("")

		if gameover == True:
			break

		check_if_pitching_change()
		status()

	wait()

#######################################################################################################################
#######################################################################################################################

#Game over

if home_score > away_score:
	print("Game has ended. " + home_team + " win!")
elif home_score < away_score:
	print("Game has ended. " + away_team + " win!")

wait_short()
print("")
wait_short()
print("---Box Score---")
wait_short()
print("First pitch: " + str(first_pitch_time)) 
wait_short()
print("")
wait_short()

#Line score
print(away_abbr + " ",end="")
for x in away_score_by_inning:
	wait_short()
	print(str(x) + " " ,end="")
wait_short()
print("- \033[1;93;40m" + str(away_score) + "\033[0m")

wait_short()
print( home_abbr + " ",end="")
for x in home_score_by_inning:
	wait_short()
	print(str(x) + " " ,end="")
if len(home_score_by_inning) < len(away_score_by_inning):
	print("  ",end="")
wait_short()
print("- \033[1;93;40m" + str(home_score) + "\033[0m\n")

#Away batting
wait_short()
print(away_team + "                  AB   R   H  RBI HR  BB  SO")
for x in away_batters:
	wait_short()
	print(x[0] + " ",end="")
	for y in range(25 - len(str(x[0]))):
		print(" ",end="")





	#Make sure the columns align
	#This is messy :(
	print(str(x[2]),end="")
	
	if len(str(x[3])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[3]),end="")
	if len(str(x[4])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")
	
	print(str(x[4]),end="")
	if len(str(x[5])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[5]),end="")
	if len(str(x[6])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[6]),end="")
	if len(str(x[7])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[7]),end="")
	if len(str(x[8])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[8]))









away_ab_total = 0
away_r_total = 0
away_h_total = 0
away_rbi_total = 0
away_hr_total = 0
away_bb_total = 0
away_so_total = 0

for x in range (0, 9):
	away_ab_total = away_ab_total + away_batters[x][2]
	away_r_total = away_r_total + away_batters[x][3]
	away_h_total = away_h_total + away_batters[x][4]
	away_rbi_total = away_rbi_total + away_batters[x][5]
	away_hr_total = away_hr_total + away_batters[x][6]
	away_bb_total = away_bb_total + away_batters[x][7]
	away_so_total = away_so_total + away_batters[x][8]

wait_short()
print("Totals:                  " + str(away_ab_total),end="")

if len(str(away_r_total)) > 1:
	print("  ",end="")
else:
	print("   ",end="")
print(str(away_r_total),end="")

if len(str(away_h_total)) > 1:
	print("  ",end="")
else:
	print("   ",end="")
print(str(away_h_total),end="")

if len(str(away_rbi_total)) > 1:
	print("  ",end="")
else:
	print("   ",end="")
print(str(away_rbi_total),end="")

if len(str(away_hr_total)) > 1:
	print("  ",end="")
else:
	print("   ",end="")
print(str(away_hr_total),end="")

if len(str(away_bb_total)) > 1:
	print("  ",end="")
else:
	print("   ",end="")
print(str(away_bb_total),end="")

if len(str(away_so_total)) > 1:
	print("  ",end="")
else:
	print("   ",end="")
print(str(away_so_total))

print("")

#Home batting
print(home_team + "                  AB   R   H  RBI HR  BB  SO")
for x in home_batters:
	wait_short()
	print(x[0] + " ",end="")
	for y in range(25 - len(str(x[0]))):
		print(" ",end="")
	
	
	#Make sure the columns align
	#This is messy :(
	print(str(x[2]),end="")
	
	if len(str(x[3])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[3]),end="")
	if len(str(x[4])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")
	
	print(str(x[4]),end="")
	if len(str(x[5])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[5]),end="")
	if len(str(x[6])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[6]),end="")
	if len(str(x[7])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[7]),end="")
	if len(str(x[8])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[8]))

	
	
	
	
	

home_ab_total = 0
home_r_total = 0
home_h_total = 0
home_rbi_total = 0
home_hr_total = 0
home_bb_total = 0
home_so_total = 0

for x in range (0, 9):
	home_ab_total = home_ab_total + home_batters[x][2]
	home_r_total = home_r_total + home_batters[x][3]
	home_h_total = home_h_total + home_batters[x][4]
	home_rbi_total = home_rbi_total + home_batters[x][5]
	home_hr_total = home_hr_total + home_batters[x][6]
	home_bb_total = home_bb_total + home_batters[x][7]
	home_so_total = home_so_total + home_batters[x][8]

wait_short()
print("Totals:                  " + str(home_ab_total),end="")

if len(str(home_r_total)) > 1:
	print("  ",end="")
else:
	print("   ",end="")
print(str(home_r_total),end="")

if len(str(home_h_total)) > 1:
	print("  ",end="")
else:
	print("   ",end="")
print(str(home_h_total),end="")

if len(str(home_rbi_total)) > 1:
	print("  ",end="")
else:
	print("   ",end="")
print(str(home_rbi_total),end="")

if len(str(home_hr_total)) > 1:
	print("  ",end="")
else:
	print("   ",end="")
print(str(home_hr_total),end="")

if len(str(home_bb_total)) > 1:
	print("  ",end="")
else:
	print("   ",end="")
print(str(home_bb_total),end="")

if len(str(home_so_total)) > 1:
	print("  ",end="")
else:
	print("   ",end="")
print(str(home_so_total))

wait_short()
print("")
wait_short()
print("")
wait_short()




print("Pitchers")
wait_short()
print("")
wait_short

print(away_team + "                  IP   R   H  ER  HR  BB  SO")
wait_short()
for x in away_pitchers_used:
	print(x[0] + " ",end="")
	for y in range(23 - len(str(x[0]))):
		print(" ",end="")
	
	#Make sure the columns align
	#This is messy :(
	if len(str(round(x[2],1))) == 1:
		print("  ",end="")
	print(str(round(x[2],1)),end="")

	if len(str(x[3])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[3]),end="")
	if len(str(x[4])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")
	
	print(str(x[4]),end="")
	if len(str(x[5])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[5]),end="")
	if len(str(x[6])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[6]),end="")
	if len(str(x[7])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[7]),end="")
	if len(str(x[8])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[8]))





















	wait_short()
print("Totals: ")
wait_short()
print("")
wait_short()

print(home_team + "                  IP   R   H  ER  HR  BB  SO")
wait_short()
for x in home_pitchers_used:
	print(x[0] + " ",end="")
	for y in range(23 - len(str(x[0]))):
		print(" ",end="")

	#Make sure the columns align
	#This is messy :(
	if len(str(round(x[2],1))) == 1:
		print("  ",end="")
	print(str(round(x[2],1)),end="")

	if len(str(x[3])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[3]),end="")
	if len(str(x[4])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")
	
	print(str(x[4]),end="")
	if len(str(x[5])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[5]),end="")
	if len(str(x[6])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[6]),end="")
	if len(str(x[7])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[7]),end="")
	if len(str(x[8])) > 1:
		print("  ",end="")
	else:
		print("   ",end="")

	print(str(x[8]))

wait_short()
print("Totals: ")
wait_short()
print("")


"""
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
"""
save_results = input("Save box score to a text file? (Y/N)")

"""
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
"""