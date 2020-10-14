# https://github.com/benryan03/baseball_simulator/

import random
import time
import math
from datetime import datetime

from CalculatePitchOutcome import *
from PrintBoxScore import *

# To scrape players and stats from baseball-reference
from lxml import html
import requests

# For text colors
from colorama import init, Fore, Back, Style
init()

home_score = 0
away_score = 0
half_inning = 1
balls = 0
strikes = 0
outs = 0
rand = 0
pitch_result = "_"
gameover = False
atbat_pitch_count = 1
pitch_count = {"home": 1, "away": -1}
current_batter = {"home": 0, "away": -1}
margin = 0
edge = ["", 0]
redo_pitch_loops = 0
runs_in_current_inning = 0
score_by_inning = {"home":[], "away":[]}
on_base = [-1, -1, -1, -1]
earned_runs = 0


def wait():  # Change both wait times to 0 for game to complete immediately
	time.sleep(2)  # default 2


def wait_short():
	time.sleep(.5)  # default .5


def batting_team():
	if half_inning % 2 == 0:
		return "home"
	else:
		return "away"


def pitching_team():
	if half_inning % 2 == 0:
		return "away"
	else:
		return "home"


def resetcount():
	global balls
	global strikes
	balls = 0
	strikes = 0


def status():  # Print number of outs, inning number, score, and on-base statuses

	wait()
	print("-------------------------------------------------------------")
	wait()

	print("Outs: " + str(outs) + " | Inning: ", end="")
	if half_inning % 2 != 0:
		print("Top ", end="")
	elif half_inning % 2 == 0:
		print("Bot ", end="")
	print(
		str(math.ceil(half_inning / 2))
		+ " | "
		+ abbrs["home"] 
		+ ": "
		+ str(home_score)
		+ " | "
		+ abbrs["away"] 
		+ ": "
		+ str(away_score)
		+ " | 3B: ",
		end="",
	)
	if on_base[3] > -1:
		print("\033[1;93;40mX\033[0m 2B: ", end="")
	elif on_base[3] == -1:
		print("  2B: ", end="")
	if on_base[2] > -1:
		print("\033[1;93;40mX\033[0m 1B: ", end="")
	elif on_base[2] == -1:
		print("  1B: ", end="")
	if on_base[1] > -1:
		print("\033[1;93;40mX\033[0m")
	elif on_base[1] == -1:
		print(" ")

	wait()
	now_batting()
	wait()


def format_batting_average(avg):
	avg_string = str(avg)

	# Remove leading 0
	avg_string = avg_string[1:]

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


def pitching_animation():
	# flush=True makes sure time.sleep instances do not occur all at once
	print("\033[1;30;40mPitch " + str(pitch_count[pitching_team()]) + " (" + current_pitcher[pitching_team()][0] + ") \033[0m", end = "", flush=True)
	for x in range(0, 3):
		wait_short()
		print("\033[1;30;40m. \033[0m", end="", flush=True)

	for x in range(0, redo_pitch_loops):
		wait_short()
		print("\033[1;30;40m. \033[0m", end="", flush=True)

	print("")


def ball_in_play_animation():
	# flush=True makes sure time.sleep instances do not occur all at once
	print("\033[1;97;100mBall in play!\033[0m", end="", flush=True)
	for x in range(0, 6):
		wait_short()
		print("\033[1;97;100m .\033[0m", end="", flush=True)
	print("")


def now_batting():
	global edge
	global edge_pos
	global margin
	global redo_pitch_loops
	global batters
	global batters

	# Print name and average of current batter
	print(
		"\033[1;93;40m"
		+ str(batters[batting_team()][current_batter[batting_team()]][0])
		+ "\033[0m is now batting for the "
		+ teams[batting_team()]
		+ ". "
		+ str(years[batting_team()])
		+ " AVG: "
		+ format_batting_average(batters[batting_team()][current_batter[batting_team()]][1])
	)
	batters[batting_team()][current_batter[batting_team()]][2] += 1  # Update at-bat count for box score

	redo_pitch_loops = 0

	# Determine edge
	avg = batters[batting_team()][current_batter[batting_team()]][1]
	era = current_pitcher[pitching_team()][1]

	x = avg / 0.250
	y = (2 - (era / 4)) - (pitch_count[pitching_team()] * 0.005)

	if x > y:
		# Batter has edge
		edge = batters[batting_team()][current_batter[batting_team()]][0]
		edge_pos = "Batter"
		margin = x - y

	elif x <= y:
		# Pitcher has edge
		edge = current_pitcher[pitching_team()][0]
		edge_pos = "Pitcher"
		margin = y - x
		
	# Print edge
	wait()
	margin = round(margin * 50, 1)
	print("Edge: " + edge + " - " + str(margin) + "%")	


def out(num):
	global outs
	global half_inning
	global gameover
	global balls
	global strikes
	global runs_in_current_inning
	global on_base
	for x in range(num):

		# For box score
		# Totals will get rounded to 1 decimal so .3333 is accurate enough :)
		if half_inning % 2 == 0:
			pitchers_used["away"][-1][2] = pitchers_used["away"][-1][2] + 0.3333
		elif half_inning % 2 != 0:
			pitchers_used["home"][-1][2] = pitchers_used["home"][-1][2] + 0.3333

		if outs <= 1:
			resetcount()
			outs += 1
		elif outs == 2 and half_inning < 17:
			# before 9th inning, no win possible
			outs = 3
			wait()
			half_inning += 1
			inning_status()
			outs = 0

			on_base = [-1, -1, -1, -1]
			balls = 0
			strikes = 0
			runs_in_current_inning = 0
			if half_inning == 2:
				print("\033[1;93;40m" + starting_pitchers["away"][0] + "\033[0m is now pitching for the " + teams["away"] + ".")
				wait()
				print(str(years["away"]) + " ERA: " + str(format_era(starting_pitchers["away"][1])))
				wait()
		elif (outs == 2 and half_inning >= 17 and half_inning % 2 != 0 and home_score <= away_score):
			# if 2 outs and 9th inning or later and end of top of inning and away team is ahead or tied
			outs = 3
			print("")
			wait()
			half_inning += 1
			inning_status()
			outs = 0

			on_base = [-1, -1, -1, -1]
			balls = 0
			strikes = 0
		elif (outs == 2 and half_inning >= 17 and half_inning % 2 == 0 and home_score == away_score):
			# if 2 outs and 9th inning or later and end of bottom of inning and score is tied
			outs = 3
			print("")
			wait()
			half_inning += 1
			inning_status()
			outs = 0

			on_base = [-1, -1, -1, -1]
			balls = 0
			strikes = 0
		else:
			# Game over
			gameover = True


def run(num):
	global away_score
	global home_score
	global gameover
	global runs_in_current_inning
	global score_by_inning
	global earned_runs
	global batters

	runners = {0: None, 1: None, 2: None, 3: None}

	# Determine and who scored the runs, and update their Run stats for box score
	if num == 1 and on_base[3] > -1:
		# 1 run scored from third
		batters[batting_team()][on_base[3]][3] += 1
		runners[0] = batters[batting_team()][on_base[3]]

	elif num == 1 and on_base[2] > -1:
		# 1 run scored from second
		batters[batting_team()][on_base[2]][3] += 1
		runners[0] = batters[batting_team()][on_base[2]]

	elif num == 1 and on_base[1] > -1:
		# 1 run scored from first
		batters[batting_team()][on_base[1]][3] += 1

	elif num == 1 and (on_base[3] == -1 and on_base[2] == -1 and on_base[1] == -1):
		# Solo home run
		batters[batting_team()][current_batter[batting_team()]][3] += 1
		runners[0] = batters[batting_team()][current_batter[batting_team()]]

	elif num == 2 and on_base[3] > -1 and on_base[2] > -1:
		# 2 runs scored from second and third
		batters[batting_team()][on_base[3]][3] += 1
		batters[batting_team()][on_base[2]][3] += 1
		runners[0] = batters[batting_team()][on_base[3]]
		runners[1] = batters[batting_team()][on_base[2]]

	elif num == 2 and on_base[3] > -1 and on_base[1] > -1:
		# 2 runs scored from first and third
		batters[batting_team()][on_base[3]][3] += 1
		batters[batting_team()][on_base[1]][3] += 1
		runners[0] = batters[batting_team()][on_base[3]]
		runners[1] = batters[batting_team()][on_base[1]]

	elif num == 2 and on_base[2] > -1 and on_base[1] > -1:
		# 2 runs scored from first and second
		batters[batting_team()][on_base[2]][3] += 1
		batters[batting_team()][on_base[1]][3] += 1
		runners[0] = batters[batting_team()][on_base[2]]
		runners[1] = batters[batting_team()][on_base[1]]

	elif num == 2 and (on_base[3] > -1 and on_base[2] == -1 and on_base[1] == -1):
		# 2 run HR with runner on third
		batters[batting_team()][on_base[3]][3] += 1
		batters[batting_team()][current_batter[batting_team()]][3] += 1
		runners[0] = batters[batting_team()][on_base[3]]
		runners[1] = batters[batting_team()][current_batter[batting_team()]]

	elif num == 2 and (on_base[3] == -1 and on_base[2] > -1 and on_base[1] == -1):
		# 2 run HR with runner on second
		batters[batting_team()][on_base[2]][3] += 1
		batters[batting_team()][current_batter[batting_team()]][3] += 1
		runners[0] = batters[batting_team()][on_base[2]]
		runners[1] = batters[batting_team()][current_batter[batting_team()]]

	elif num == 2 and (on_base[3] == -1 and on_base[2] == -1 and on_base[1] > -1):
		# 2 run HR with runner on first
		batters[batting_team()][on_base[1]][3] += 1
		batters[batting_team()][current_batter[batting_team()]][3] += 1
		runners[0] = batters[batting_team()][on_base[1]]
		runners[1] = batters[batting_team()][current_batter[batting_team()]]

	elif num == 3 and (on_base[3] > -1 and on_base[2] > -1 and on_base[1] > -1):
		# 3 runs scored from first, second, and third
		batters[batting_team()][on_base[3]][3] += 1
		batters[batting_team()][on_base[2]][3] += 1
		batters[batting_team()][on_base[1]][3] += 1
		runners[0] = batters[batting_team()][on_base[3]]
		runners[1] = batters[batting_team()][on_base[2]]
		runners[2] = batters[batting_team()][on_base[1]]

	elif num == 3 and on_base[3] > -1 and on_base[2] > -1:
		# 3 run HR, runners on second and third
		batters[batting_team()][on_base[3]][3] += 1
		batters[batting_team()][on_base[2]][3] += 1
		batters[batting_team()][current_batter[batting_team()]][3] += 1
		runners[0] = batters[batting_team()][on_base[3]]
		runners[1] = batters[batting_team()][on_base[2]]
		runners[2] = batters[batting_team()][current_batter[batting_team()]]

	elif num == 3 and on_base[3] > -1 and on_base[1] > -1:
		# 3 run HR, runners on first and third
		batters[batting_team()][on_base[3]][3] += 1
		batters[batting_team()][on_base[1]][3] += 1
		batters[batting_team()][current_batter[batting_team()]][3] += 1
		runners[0] = batters[batting_team()][on_base[3]]
		runners[1] = batters[batting_team()][on_base[1]]
		runners[2] = batters[batting_team()][current_batter[batting_team()]]

	elif num == 3 and on_base[2] > -1 and on_base[1] > -1:
		# 3 run HR, runners on first and second
		batters[batting_team()][on_base[2]][3] += 1
		batters[batting_team()][on_base[1]][3] += 1
		batters[batting_team()][current_batter[batting_team()]][3] += 1
		runners[0] = batters[batting_team()][on_base[2]]
		runners[1] = batters[batting_team()][on_base[1]]
		runners[2] = batters[batting_team()][current_batter[batting_team()]]

	elif num == 4: # Grand slam
		batters[batting_team()][on_base[3]][3] += 1
		batters[batting_team()][on_base[2]][3] += 1
		batters[batting_team()][on_base[1]][3] += 1
		batters[batting_team()][current_batter[batting_team()]][3] += 1
		runners[0] = batters[batting_team()][on_base[3]]
		runners[1] = batters[batting_team()][on_base[2]]
		runners[2] = batters[batting_team()][on_base[1]]
		runners[3] = batters[batting_team()][current_batter[batting_team()]]

	# Print who scored the runs
	for x in range(3):
		if runners[x] != None:
			wait()
			print("")
			wait()
			print("\033[1;30;102m" + runners[x][0] + " scored a run for the " + teams[batting_team()] + "!\033[0m")

	for x in range(num):

		# Line score
		inning = int((half_inning / 2) + 0.5)
		if len(score_by_inning[batting_team()]) < inning:
			score_by_inning[batting_team()].append(1)
		else:
			score_by_inning[batting_team()][-1] += 1

		# Box score - earned runs
		pitchers_used[pitching_team()][-1][3] += 1
		if earned_runs < 0:
			earned_runs += 1
		else:
			pitchers_used[pitching_team()][-1][5] += 1

		if half_inning < 18 and half_inning % 2 != 0:
			# normal innings - run for away
			away_score += 1
			runs_in_current_inning += 1  # For pitching change check
			batters["away"][current_batter["away"]][5] += 1  # RBI count for box score
			wait_short()
		elif half_inning < 18 and half_inning % 2 == 0:
			# normal innings - run for home
			home_score += 1
			runs_in_current_inning += 1  # For pitching change check
			batters["home"][current_batter["home"]][5] += 1  # RBI count for box score
			wait_short()
		elif half_inning >= 18 and half_inning % 2 != 0:
			# extra innings - run for away
			away_score += 1
			runs_in_current_inning += 1  # For pitching change check
			batters["away"][current_batter["away"]][5] += 1  # RBI count for box score
			wait_short()
		elif half_inning >= 18 and half_inning % 2 == 0 and away_score > home_score:
			# extra innings - run for home, no walkoff
			home_score += 1
			batters["home"][current_batter["home"]][5] += 1  # RBI count for box score
			runs_in_current_inning += 1  # For pitching change check
			wait_short()
		elif half_inning >= 18 and half_inning % 2 == 0 and away_score == home_score:
			# walkoff run!
			home_score += 1
			batters["home"][current_batter["home"]][5] += 1  # RBI count for box score
			print("\033[1;30;102mWALKOFF for the " + teams["home"] + "!\033[0m")
			wait()
			print("")
			wait()
			print("Game has ended. " + teams["home"] + " wins.")
			gameover = True


def check_if_pitching_change():

	if (current_pitcher[pitching_team()][0] == starting_pitchers[pitching_team()][0] and pitch_count[pitching_team()] >= 100):
		# Starter is still in and has thrown 100 pitches
		pitching_change()
	elif (current_pitcher[pitching_team()][0] == starting_pitchers[pitching_team()][0] and half_inning >= 13):
		# Starter is still in and it is the top of the 7th inning
		pitching_change()
	elif (current_pitcher[pitching_team()][0] == starting_pitchers[pitching_team()][0] and pitchers_used[pitching_team()][0][5] > 4):
		# Starter is still in and has allowed more than 4 runs
		pitching_change()
	elif (current_pitcher[pitching_team()][0] != starting_pitchers[pitching_team()][0] and half_inning <= 9 and runs_in_current_inning > 2 and len(relief_pitchers[pitching_team()]) > 0):
		# A reliever is in and has allowed more than 2 runs and it is before the 6th inning
		pitching_change()
	elif (current_pitcher[pitching_team()][0] != starting_pitchers[pitching_team()][0] and current_pitcher[pitching_team()][0] != closers[pitching_team()][0] and (half_inning == 17 or half_inning == 18)):
		# Top of 9th inning (Send in closer)
		pitching_change()
	elif (current_pitcher[pitching_team()][0] != starting_pitchers[pitching_team()][0] and half_inning > 9 and outs == 0 and on_base[1] == -1 and on_base[2] == -1 and on_base[3] == -1 and runs_in_current_inning == 0 and len(relief_pitchers[pitching_team()]) > 0):
		# A reliever is in and it is the start of an inning, 6th or later
		pitching_change()
	elif (current_pitcher[pitching_team()][0] != starting_pitchers[pitching_team()][0] and runs_in_current_inning > 2 and len(relief_pitchers[pitching_team()]) > 0):
		# A reliever is in and has allowed more than 2 runs
		pitching_change()


def pitching_change():
	global relief_pitchers
	global current_pitcher
	global pitch_count
	global runs_in_current_inning
	global earned_runs

	runs_in_current_inning = 0

	# Used for Earned Runs in box score
	earned_runs = 0
	if on_base[1] > -1:
		earned_runs = earned_runs - 1
	if on_base[2] > -1:
		earned_runs = earned_runs - 1
	if on_base[3] > -1:
		earned_runs = earned_runs - 1

	if half_inning == 17 or half_inning == 18:
		# 9th inning - send in closer
		current_pitcher[pitching_team()] = closers[pitching_team()]
	else:
		# Not 9th inning - Choose a random relief pitcher
		x = len(relief_pitchers[pitching_team()])
		rand = random.randint(0, x - 1)
		current_pitcher[pitching_team()] = relief_pitchers[pitching_team()][rand]
		del relief_pitchers[pitching_team()][rand]
		pitch_count[pitching_team()] = 1

	pitchers_used[pitching_team()].append(current_pitcher[pitching_team()])  # Add pitcher to array for box score
	for x in range(10): # Generate blank stats for box score
		pitchers_used[pitching_team()][-1].append(0)

	# Print new pitcher
	wait()
	print("Pitching change!")
	wait()
	print("")
	wait()
	print("\033[1;93;40m" + current_pitcher[pitching_team()][0] + "\033[0m is now pitching for the " + teams[pitching_team()] + ".")
	wait()
	print(str(years[pitching_team()]) + " ERA: " + str(format_era(current_pitcher[pitching_team()][1])))
	wait()
	print("")
	wait()


def inning_status():

	# Update line score for end-of-game stats
	prev_half_inning = half_inning - 1
	if len(score_by_inning[batting_team()]) < prev_half_inning - 1:
		score_by_inning[batting_team()].append(0)

	# This will be accurate until the 21st inning - will fix eventually
	if half_inning == 1 or half_inning == 2:
		x = "st"
	elif half_inning == 3 or half_inning == 4:
		x = "nd"
	elif half_inning == 5 or half_inning == 6:
		x = "rd"
	else:
		x = "th"

	# Print inning status
	wait()
	print("")
	print("")
	print("------------------------------------")
	print(
		"It is now the ", end = "")
	if half_inning % 2 != 0:
		print("top", end = "")
	elif half_inning % 2 == 0:
		print("bottom", end = "")
	print(" of the "
		+ str((half_inning / 2) + 0.5).split(".")[0]
		+ x
		+ " inning."
	)
	print("------------------------------------")
	print("")
	wait()


def parse_input(input_team):

	input_team = input_team.lower().strip()

	if (
		input_team == "arizona diamondbacks"
		or input_team == "arizona"
		or input_team == "diamondbacks"
		or input_team == "ari"
	):
		return "Diamondbacks,ARI"
	elif (
		input_team == "atlanta braves"
		or input_team == "atlanta"
		or input_team == "braves"
		or input_team == "atl"
	):
		return "Braves,ATL"
	elif (
		input_team == "baltimore"
		or input_team == "orioles"
		or input_team == "baltimore"
		or input_team == "orioles"
		or input_team == "bal"
	):
		return "Orioles,BAL"
	elif (
		input_team == "boston red sox"
		or input_team == "boston"
		or input_team == "red sox"
		or input_team == "bos"
	):
		return "Red Sox,BOS"
	elif input_team == "chicago cubs" or input_team == "cubs" or input_team == "chc":
		return "Cubs,CHC"
	elif (
		input_team == "chicago white sox"
		or input_team == "white sox"
		or input_team == "chw"
	):
		return "White Sox,CHW"
	elif (
		input_team == "cincinnati reds"
		or input_team == "cincinnati"
		or input_team == "reds"
		or input_team == "cin"
	):
		return "Reds,CIN"
	elif (
		input_team == "cleveland indians"
		or input_team == "cleveland"
		or input_team == "indians"
		or input_team == "cle"
	):
		return "Indians,CLE"
	elif (
		input_team == "colorado rockies"
		or input_team == "colorado"
		or input_team == "rockies"
		or input_team == "col"
	):
		return "Rockies,COL"
	elif (
		input_team == "detroit tigers"
		or input_team == "detroit"
		or input_team == "tigers"
		or input_team == "det"
	):
		return "Tigers,DET"
	elif (
		input_team == "houston astros"
		or input_team == "houston"
		or input_team == "astros"
		or input_team == "hou"
	):
		return "Astros,HOU"
	elif (
		input_team == "kansas city royals"
		or input_team == "kansas city"
		or input_team == "royals"
		or input_team == "kcr"
	):
		return "Royals,KCR"
	elif (
		input_team == "los angeles angels"
		or input_team == "anaheim angels"
		or input_team == "anaheim"
		or input_team == "angels"
		or input_team == "ana"
	):
		return "Angels,ANA"
	elif (
		input_team == "los angeles dodgers"
		or input_team == "los angeles"
		or input_team == "dodgers"
		or input_team == "lad"
	):
		return "Dodgers,LAD"
	elif (
		input_team == "miami marlins"
		or input_team == "florida marlins"
		or input_team == "miami"
		or input_team == "florida"
		or input_team == "marlins"
		or input_team == "fla"
	):
		return "Marlins,FLA"
	elif (
		input_team == "milwaukee brewers"
		or input_team == "milwaukee"
		or input_team == "brewers"
		or input_team == "mil"
	):
		return "Brewers,MIL"
	elif (
		input_team == "minnesota twins"
		or input_team == "minnesota"
		or input_team == "twins"
		or input_team == "min"
	):
		return "Twins,MIN"
	elif input_team == "new york mets" or input_team == "mets" or input_team == "nym":
		return "Mets,NYM"
	elif (
		input_team == "new york yankees"
		or input_team == "yankees"
		or input_team == "nyy"
	):
		return "Yankees,NYY"
	elif (
		input_team == "oakland athletics"
		or input_team == "oakland"
		or input_team == "athletics"
		or input_team == "as"
		or input_team == "a's"
		or input_team == "oak"
	):
		return "Athletics,OAK"
	elif (
		input_team == "philadelphia phillies"
		or input_team == "philadelphia"
		or input_team == "phillies"
		or input_team == "phi"
	):
		return "Phillies,PHI"
	elif (
		input_team == "pittsburgh pirates"
		or input_team == "pittsburgh"
		or input_team == "pirates"
		or input_team == "pit"
	):
		return "Pirates,PIT"
	elif (
		input_team == "san diego padres"
		or input_team == "san diego"
		or input_team == "padres"
		or input_team == "sdp"
	):
		return "Padres,SDP"
	elif (
		input_team == "san francisco giants"
		or input_team == "san francisco"
		or input_team == "giants"
		or input_team == "sfg"
	):
		return "Giants,SFG"
	elif (
		input_team == "seattle mariners"
		or input_team == "seattle"
		or input_team == "mariners"
		or input_team == "sea"
	):
		return "Mariners,SEA"
	elif (
		input_team == "st louis cardinals"
		or input_team == "st. louis cardinals"
		or input_team == "st louis"
		or input_team == "st. louis"
		or input_team == "cardinals"
		or input_team == "stl"
	):
		return "Cardinals,STL"
	elif (
		input_team == "tampa bay rays"
		or input_team == "tampa bay"
		or input_team == "rays"
		or input_team == "tampa bay devil rays"
		or input_team == "devil rays"
		or input_team == "tbd"
	):
		return "Rays,TBD"
	elif (
		input_team == "texas rangers"
		or input_team == "texas"
		or input_team == "rangers"
		or input_team == "tex"
	):
		return "Rangers,TEX"
	elif (
		input_team == "toronto blue jays"
		or input_team == "toronto"
		or input_team == "blue jays"
		or input_team == "tor"
	):
		return "Blue Jays,TOR"
	elif (
		input_team == "washington nationals"
		or input_team == "washington"
		or input_team == "nationals"
		or input_team == "wsn"
	):
		return "Nationals,WSN"
	else:
		return "invalid"


#######################################################################################################################
#######################################################################################################################

# Program start

print("Welcome to Baseball Simulator")

###########################################################
# Get user inputs to choose teams

teams = {"home": None, "away": None}
abbrs = {"home": None, "away": None}
years = {"home": None, "away": None}

#teams = {"home": "Red Sox", "away": "Yankees"}
#abbrs = {"home": "BOS", "away": "NYY"}
#years = {"home": "2018", "away": "2018"}

home_team_error = True
while home_team_error == True:
	team = input("Enter the name of the home team: ")
	if parse_input(team) == "invalid":
		print("Invalid team.")
		continue
	else:
		teams["home"] = parse_input(team).split(",")[0]
		abbrs["home"]  = parse_input(team).split(",")[1]
		home_team_error = False

home_year_error = True
while home_year_error == True:
	years["home"] = input("Enter year: ")
	home_page = requests.get(
		"https://www.baseball-reference.com/teams/"
		+ abbrs["home"] 
		+ "/"
		+ years["home"]
		+ ".shtml"
	)
	if str(home_page) != "<Response [200]>":
		print("Invalid year.")
		continue
	else:
		home_year_error = False

away_team_error = True
while away_team_error == True:
	teams["away"] = input("Enter the name of the away team: ")
	if parse_input(teams["away"]) == "invalid":
		print("Invalid team.")
		continue
	else:
		teams["away"] = parse_input(teams["away"]).split(",")[0]
		abbrs["away"]  = parse_input(teams["away"]).split(",")[1]
		away_team_error = False

away_year_error = True
while away_year_error == True:
	years["away"] = input("Enter year: ")
	away_page = requests.get(
		"https://www.baseball-reference.com/teams/"
		+ abbrs["away"] 
		+ "/"
		+ years["away"]
		+ ".shtml"
	)
	if str(away_page) != "<Response [200]>":
		print("Invalid year.")
		continue
	else:
		away_year_error = False

print("")
print("Loading players...")

###########################################################
# Scrape top 9 batters and batting averages for specified team/year

# Load baseball-reference page for inputted team/year
# URL format: https://www.baseball-reference.com/teams/BOS/2004.shtml
home_page = requests.get(
	"https://www.baseball-reference.com/teams/" + abbrs["home"]  + "/" + years["home"] + ".shtml"
)
home_tree = html.fromstring(home_page.content)
away_page = requests.get(
	"https://www.baseball-reference.com/teams/" + abbrs["away"]  + "/" + years["away"] + ".shtml"
)
away_tree = html.fromstring(away_page.content)

batters = {"home": ["", "", "", "", "", "", "", "", ""], "away": ["", "", "", "", "", "", "", "", ""]}

# Scrape names of top 8 batters
for x in range(8):
	# Home
	fullname = home_tree.xpath(
		'//table[@id="team_batting"]/tbody/tr[' + str(x + 1) + "]/td[2]/@csk"
	)
	fname = str(fullname).partition(",")[2]
	lname = str(fullname).partition(",")[0]
	batters["home"][x] = fname.strip("[],'") + " " + lname.strip("[],'")

	# Away
	fullname = away_tree.xpath(
		'//table[@id="team_batting"]/tbody/tr[' + str(x + 1) + "]/td[2]/@csk"
	)
	fname = str(fullname).partition(",")[2]
	lname = str(fullname).partition(",")[0]
	batters["away"][x] = fname.strip("[],'") + " " + lname.strip("[],'")

# Scrape name of 9th batter (sometimes the formatting on baseball-reference skips the 9th row)
# Home
fullname = home_tree.xpath('//table[@id="team_batting"]/tbody/tr[9]/td[2]/@csk')
if fullname == []:
	fullname = home_tree.xpath('//table[@id="team_batting"]/tbody/tr[10]/td[2]/@csk')

fname = str(fullname).partition(",")[2]
lname = str(fullname).partition(",")[0]
batters["home"][8] = fname.strip("[],'") + " " + lname.strip("[],'")

# Away
fullname = away_tree.xpath('//table[@id="team_batting"]/tbody/tr[9]/td[2]/@csk')
if fullname == []:
	fullname = away_tree.xpath('//table[@id="team_batting"]/tbody/tr[10]/td[2]/@csk')

fname = str(fullname).partition(",")[2]
lname = str(fullname).partition(",")[0]
batters["away"][8] = fname.strip("[],'") + " " + lname.strip("[],'")

# Batting averages
home_avg = [0, 0, 0, 0, 0, 0, 0, 0, 0]
away_avg = [0, 0, 0, 0, 0, 0, 0, 0, 0]

# Scrape batting averages of first 8 batters
for x in range(8):
	avg = home_tree.xpath(
		'//table[@id="team_batting"]/tbody/tr[' + str(x + 1) + "]/td[17]/text()"
	)
	home_avg[x] = float(str(avg).strip("[]'"))
	avg = away_tree.xpath(
		'//table[@id="team_batting"]/tbody/tr[' + str(x + 1) + "]/td[17]/text()"
	)
	away_avg[x] = float(str(avg).strip("[]'"))

# Scrape batting average of 9th batter
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

# Add batting averages to batters array
batters["home"] = [
	[batters["home"][0], home_avg[0]],
	[batters["home"][1], home_avg[1]],
	[batters["home"][2], home_avg[2]],
	[batters["home"][3], home_avg[3]],
	[batters["home"][4], home_avg[4]],
	[batters["home"][5], home_avg[5]],
	[batters["home"][6], home_avg[6]],
	[batters["home"][7], home_avg[7]],
	[batters["home"][8], home_avg[8]],
]
batters["away"] = [
	[batters["away"][0], away_avg[0]],
	[batters["away"][1], away_avg[1]],
	[batters["away"][2], away_avg[2]],
	[batters["away"][3], away_avg[3]],
	[batters["away"][4], away_avg[4]],
	[batters["away"][5], away_avg[5]],
	[batters["away"][6], away_avg[6]],
	[batters["away"][7], away_avg[7]],
	[batters["away"][8], away_avg[8]],
]

# Fill in empty stats for box score
for x in range(9):
	batters["home"][x].append(0)
	batters["home"][x].append(0)
	batters["home"][x].append(0)
	batters["home"][x].append(0)
	batters["home"][x].append(0)
	batters["home"][x].append(0)
	batters["home"][x].append(0)
	batters["away"][x].append(0)
	batters["away"][x].append(0)
	batters["away"][x].append(0)
	batters["away"][x].append(0)
	batters["away"][x].append(0)
	batters["away"][x].append(0)
	batters["away"][x].append(0)

# Sort array by batting average to determine batting order
batters["home"] = sorted(batters["home"], key=lambda x: x[1], reverse=True)
batters["away"] = sorted(batters["away"], key=lambda x: x[1], reverse=True)

###########################################################
# Scrape top 12 pitchers and earned run averages for specified team/year

pitchers = {"home": 
				[
					[[""], [0]],
					[[""], [0]],
					[[""], [0]],
					[[""], [0]],
					[[""], [0]],
					[[""], [0]],
					[[""], [0]],
					[[""], [0]],
					[[""], [0]],
					[[""], [0]],
					[[""], [0]],
					[[""], [0]]
				], 
			"away": 
				[
					[[""], [0]],
					[[""], [0]],
					[[""], [0]],
					[[""], [0]],
					[[""], [0]],
					[[""], [0]],
					[[""], [0]],
					[[""], [0]],
					[[""], [0]],
					[[""], [0]],
					[[""], [0]],
					[[""], [0]]
				]
			}

starting_pitchers = {"home": ["", 0], "away": ["", 0]}

relief_pitchers = {"home": [[[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]]], "away": [[[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]]]}

closers = {"home": ["", 0], "away": ["", 0]}

pitchers_used = {"home": [], "away": []}

current_pitcher = {"home": ["", 0], "away": ["", 0]}

# Scrape names and Earned Run Averages of top 12 pitchers
# (Some extras because there are a variable number of blank/header lines mixed in)
for x in range(12):
	# Home
	fullname = home_tree.xpath(
		'//table[@id="team_pitching"]/tbody/tr[' + str(x + 1) + "]/td[2]/@csk"
	)
	position = home_tree.xpath(
		'//table[@id="team_pitching"]/tbody/tr['
		+ str(x + 1)
		+ "]/td[1]/descendant::strong/text()"
	)
	if str(fullname).strip("[],'") != "":
		fname = str(fullname).partition(",")[2]
		lname = str(fullname).partition(",")[0]
		if str(position).strip("[],'") == "CL":
			# Home closer detected
			closers["home"][0] = fname.strip("[],'") + " " + lname.strip("[],'")
			era = home_tree.xpath(
				'//table[@id="team_pitching"]/tbody/tr[' + str(x + 1) + "]/td[7]/text()"
			)
			closers["home"][1] = float(str(era).strip("[]'"))
			pitchers["home"][x][0] = "_EMPTY_"
		else:
			# Not closer
			pitchers["home"][x][0] = fname.strip("[],'") + " " + lname.strip("[],'")
			era = home_tree.xpath(
				'//table[@id="team_pitching"]/tbody/tr[' + str(x + 1) + "]/td[7]/text()"
			)
			pitchers["home"][x][1] = float(str(era).strip("[]'"))
	else:
		# Blank/header line
		pitchers["home"][x][0] = "_EMPTY_"

	# Away
	fullname = away_tree.xpath(
		'//table[@id="team_pitching"]/tbody/tr[' + str(x + 1) + "]/td[2]/@csk"
	)
	position = away_tree.xpath(
		'//table[@id="team_pitching"]/tbody/tr['
		+ str(x + 1)
		+ "]/td[1]/descendant::strong/text()"
	)
	if str(fullname).strip("[],'") != "":
		fname = str(fullname).partition(",")[2]
		lname = str(fullname).partition(",")[0]
		if str(position).strip("[],'") == "CL":
			# Away closer detected
			closers["away"][0] = fname.strip("[],'") + " " + lname.strip("[],'")
			era = away_tree.xpath(
				'//table[@id="team_pitching"]/tbody/tr[' + str(x + 1) + "]/td[7]/text()"
			)
			closers["away"][1] = float(str(era).strip("[]'"))
			pitchers["away"][x][0] = "_EMPTY_"
		else:  # Not closer
			pitchers["away"][x][0] = fname.strip("[],'") + " " + lname.strip("[],'")
			era = away_tree.xpath(
				'//table[@id="team_pitching"]/tbody/tr[' + str(x + 1) + "]/td[7]/text()"
			)
			pitchers["away"][x][1] = float(str(era).strip("[]'"))
	else:
		# Blank/header line
		pitchers["away"][x][0] = "_EMPTY_"

# For some reason, these loops need to be run twice each to remove empty array elements
for x in pitchers["home"]:
	if "_EMPTY_" in x:
		pitchers["home"].remove(x)
for x in pitchers["home"]:
	if "_EMPTY_" in x:
		pitchers["home"].remove(x)
for x in pitchers["away"]:
	if "_EMPTY_" in x:
		pitchers["away"].remove(x)
for x in pitchers["away"]:
	if "_EMPTY_" in x:
		pitchers["away"].remove(x)

# Pitchers 5 through 9 are relief pitchers
for x in range(5, 9):
	relief_pitchers["home"][x - 5] = pitchers["home"][x]
	relief_pitchers["away"][x - 5] = pitchers["away"][x]

# Print sorterd batters for Home
print("\nStarting lineup for the " + str(years["home"]) + " " + teams["home"] + ":")
wait()
for x in batters["home"]:
	print(x[0] + " - " + format_batting_average(x[1]))
	wait_short()

# Print sorted batters for Away
print("\nStarting lineup for the " + str(years["away"]) + " " + teams["away"] + ":")
wait()
for x in batters["away"]:
	print(x[0] + " - " + format_batting_average(x[1]))
	wait_short()

# Choose a random starting pitcher for each team
pitcher_rand = random.randint(0, 4)
starting_pitchers["home"] = pitchers["home"][pitcher_rand]
current_pitcher["home"] = starting_pitchers["home"]

pitcher_rand = random.randint(0, 4)
starting_pitchers["away"] = pitchers["away"][pitcher_rand]
current_pitcher["away"] = starting_pitchers["away"]

# Keep track of what starting pitchers were used, for end-of-game box score
pitchers_used["home"].append(starting_pitchers["home"])
for x in range(10):
	pitchers_used["home"][-1].append(0)

pitchers_used["away"].append(starting_pitchers["away"])
for x in range(10):
	pitchers_used["away"][-1].append(0)

wait()
print("")
wait()
print("PLAY BALL!")
wait()
print("")
wait()
print(
	"\033[1;93;40m"
	+ starting_pitchers["home"][0]
	+ "\033[0m is now pitching for the "
	+ teams["home"]
	+ "."
)
wait()
print(str(years["home"]) + " ERA: " + str(format_era(starting_pitchers["home"][1])))
wait()
print()
wait()

status()

first_pitch_time = (
	(datetime.strftime(datetime.now(), "%Y"))
	+ "-"
	+ (datetime.strftime(datetime.now(), "%m"))
	+ "-"
	+ (datetime.strftime(datetime.now(), "%d"))
	+ " at "
	+ (datetime.strftime(datetime.now(), "%H"))
	+ ":"
	+ (datetime.strftime(datetime.now(), "%M"))
)

#######################################################################################################################
#######################################################################################################################

while gameover == False:  # Main game loop

	pitch_result = calculate_pitch_outcome(atbat_pitch_count, False, edge_pos, margin, redo_pitch_loops)

	if pitch_result == "Ball" and balls < 3: # Ball
		balls += 1
		pitching_animation()
		print("Ball. (" + str(balls) + " - " + str(strikes) + ")")

	elif pitch_result == "Ball" and balls == 3:  # Walk
		pitch_result = "Walk"
		pitching_animation()
		print("\033[1;30;102mWALK!\033[0m")
		if (on_base[1] == -1 and on_base[2] == -1 and on_base[3] == -1):
			on_base[1] = current_batter[batting_team()]
		elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] == -1):
			on_base[2] = on_base[1]
			on_base[1] = current_batter[batting_team()]
		elif (on_base[1] == -1 and on_base[2] > -1 and on_base[3] == -1):
			on_base[1] = current_batter[batting_team()]
		elif (on_base[1] == -1 and on_base[2] == -1 and on_base[3] > -1):
			on_base[1] = current_batter[batting_team()]
		elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] == -1):
			on_base[3] = on_base[2]
			on_base[2] = on_base[1]
			on_base[1] = current_batter[batting_team()]
		elif (on_base[1] == -1 and on_base[2] > -1 and on_base[3] > -1):
			on_base[1] = current_batter[batting_team()]
		elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] > -1):
			run(1)
			on_base[3] = on_base[2]
			on_base[2] = on_base[1]
			on_base[1] = current_batter[batting_team()]
		elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] > -1):
			on_base[2] = on_base[1]
			on_base[1] = current_batter[batting_team()]

		batters[batting_team()][current_batter[batting_team()]][7] += 1  # Batter walk count for box score
		pitchers_used[pitching_team()][-1][7] += 1 # Pitcher walk count for box score

		resetcount()

	elif pitch_result == "Strike" and strikes < 2: #Strike
		strikes += 1
		pitching_animation()
		print("Strike. (" + str(balls) + " - " + str(strikes) + ")")

	elif pitch_result == "Strike" and strikes == 2: # Strikeout
		pitching_animation()
		print("\033[1;97;101mSTRIKEOUT!\033[0m")
		pitch_result = "Strikeout"
		batters[batting_team()][current_batter[batting_team()]][8] += 1  # Batter strikeout count for box score
		pitchers_used[pitching_team()][-1][8] += 1 # Pitcher strikeout count for box score
		out(1)

	elif pitch_result == "Foul" and strikes < 2: # Foul
		strikes += 1
		pitching_animation()
		print("Foul. (" + str(balls) + " - " + str(strikes) + ")")

	elif pitch_result == "Foul" and strikes == 2:  # Foul (with 2 strikes)
		pitching_animation()
		print("Foul. (" + str(balls) + " - " + str(strikes) + ")")

	elif pitch_result == "Ball_in_play":
		rand = random.randint(1, 100)

		if 1 <= rand <= 40:  # Fly out

			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					continue
				else:
					pitch_result = "Fly"
			else:
				pitch_result == "Fly"

			pitching_animation()
			ball_in_play_animation()

			if (on_base[1] == -1 and on_base[2] == -1 and on_base[3] == -1):
				# Bases empty
				print("\033[1;97;101mFLY OUT!\033[0m")
				out(1)
			elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] == -1):
				# Runner on first
				print("\033[1;97;101mFLY OUT!\033[0m")
				out(1)
			elif (on_base[1] == -1 and on_base[2] > -1 and on_base[3] == -1 and outs < 2):
				# Runner on and second, less than 2 outs
				print("\033[1;30;103mFLY OUT! RUNNER ADVANCED.\033[0m")
				out(1)
				on_base[3] = on_base[2]
				on_base[2] = -1
			elif (on_base[1] == -1 and on_base[2] > -1 and on_base[3] == -1 and outs == 2):
				# Runners on first and second, 2 outs
				print("\033[1;97;101mFLY OUT!\033[0m")
				out(1)
			elif (on_base[1] == -1 and on_base[2] == -1 and on_base[3] > -1 and outs < 2):
				#Runner on third, less than 2 outs
				print("\033[1;30;102mSACRIFICE FLY!\033[0m")
				out(1)
				run(1)
				on_base[3] = -1
			elif (on_base[1] == -1 and on_base[2] == -1 and on_base[3] > -1 and outs == 2):
				# Runner on third, 2 outs
				print("\033[1;97;101mFLY OUT!\033[0m")
				out(1)
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] == -1 and outs < 2):
				# Runners on first and second, less than 2 outs
				print("\033[1;30;103mFLY OUT! RUNNER ADVANCED.\033[0m")
				out(1)
				on_base[3] = on_base[2]
				on_base[2] = -1
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] == -1 and outs == 2):
				# Runners on first and second, 2 outs
				print("\033[1;97;101mFLY OUT!\033[0m")
				out(1)
			elif (on_base[1] == -1 and on_base[2] > -1 and on_base[3] > -1 and outs < 2):
				# Runners on second and third, less than 2 outs
				print("\033[1;30;102mSACRIFICE FLY!\033[0m")
				out(1)
				run(1)
				on_base[3] = -1
			elif (on_base[1] == -1 and on_base[2] > -1 and on_base[3] > -1 and outs == 2):
				# Runners on second and third, 2 outs
				print("\033[1;97;101mFLY OUT!\033[0m")
				out(1)
			elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] > -1 and outs < 2):
				# Runners on first and third, less than 2 outs
				print("\033[1;30;102mSACRIFICE FLY!\033[0m")
				out(1)
				run(1)
				on_base[3] = -1
			elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] > -1 and outs == 2):
				# Runners on first and third, 2 outs
				print("\033[1;97;101mFLY OUT!\033[0m")
				out(1)
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] > -1 and outs < 2):
				# Bases loaded, less than 2 outs
				print("\033[1;30;102mSACRIFICE FLY!\033[0m")
				out(1)
				run(1)
				on_base[3] = -1
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] > -1 and outs < 2):
				# Bases loaded, 2 outs
				print("\033[1;97;101mFLY OUT!\033[0m")
				out(1)
			resetcount()
			pitch_result = "Fly"
		elif 41 <= rand <= 70:  # Ground out

			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					continue
				else:
					pitch_result = "Grounder"
			else:
				pitch_result == "Grounder"

			pitching_animation()
			ball_in_play_animation()

			if (on_base[1] == -1 and on_base[2] == -1 and on_base[3] == -1):
				# Bases empty
				print("\033[1;97;101mGROUND OUT!\033[0m")
				out(1)
			elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] == -1 and outs < 2):
				# Runner on first, 0-1 outs
				print("\033[1;97;101mDOUBLE PLAY!\033[0m")
				out(2)
				on_base[1] = -1
			elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] == -1 and outs == 2):
				# Runner on first, 2 outs
				print("\033[1;97;101mGROUND OUT!\033[0m")
				out(1)
			elif (on_base[1] == -1 and on_base[2] > -1 and on_base[3] == -1):
				# Runner on second
				print("\033[1;97;101mGROUND OUT!\033[0m")
				out(1)
			elif (on_base[1] == -1 and on_base[2] == -1 and on_base[3] > -1):
				# Runner on third
				print("\033[1;97;101mGROUND OUT!\033[0m")
				out(1)
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] == -1 and outs == 0):
				# Runners on first and second, 0 outs
				print("\033[1;97;101mTRIPLE PLAY\033[0m")
				out(3)
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] == -1 and outs == 1):
				# Runners on first and second, 1 out
				print("\033[1;97;101mDOUBLE PLAY!\033[0m")
				out(2)
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] == -1 and outs == 2):
				# Runners on first and second, 2 outs
				print("\033[1;97;101mGROUND OUT!\033[0m")
				out(1)
			elif (on_base[1] == -1 and on_base[2] > -1 and on_base[3] > -1):
				# Runners on second and third
				print("\033[1;97;101mGROUND OUT!\033[0m")
				out(1)
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] > -1 and outs == 0):
				# Bases loaded, no outs
				print("\033[1;97;101mTRIPLE PLAY!\033[0m")
				out(3)
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] > -1 and outs == 1):
				# Bases loaded, 2 out
				print("\033[1;97;101mDOUBLE PLAY!\033[0m")
				out(2)
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] > -1 and outs == 2):
				# Bases loaded, 2 outs
				print("\033[1;97;101mGROUND OUT!\033[0m")
				out(1)
			elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] > -1 and outs < 2):
				# Runners on first and third, 0-1 outs
				print("\033[1;97;101mDOUBLE PLAY!\033[0m")
				out(2)
				on_base[1] = -1
			elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] > -1 and outs == 2):
				# Runners on first and third, 2 outs
				print("\033[1;97;101mGROUND OUT!\033[0m")
				out(1)
			resetcount()
			pitch_result = "Grounder"
		elif 71 <= rand <= 87:  # Single

			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					continue
				else:
					pitch_result = "Single"
			else:
				pitch_result == "Single"

			pitching_animation()
			ball_in_play_animation()

			print("\033[1;30;102mSINGLE!\033[0m")
			if (on_base[1] == -1 and on_base[2] == -1 and on_base[3] == -1):
				# Bases empty
				on_base[1] = current_batter[batting_team()]
			elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] == -1):
				# Runner on first
				on_base[2] = on_base[1]
				on_base[1] = current_batter[batting_team()]
			elif (on_base[1] == -1 and on_base[2] > -1 and on_base[3] == -1):
				# Runner on second
				on_base[3] = on_base[2]
				on_base[2] = -1
				on_base[1] = current_batter[batting_team()]
			elif (on_base[1] == -1 and on_base[2] == -1 and on_base[3] > -1):
				# Runner on third
				run(1)
				on_base[3] = -1
				on_base[1] = current_batter[batting_team()]
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] == -1):
				# Runners on first and second
				on_base[3] = on_base[2]
				on_base[2] = on_base[1]
				on_base[1] = current_batter[batting_team()]
			elif (on_base[1] == -1 and on_base[2] > -1 and on_base[3] > -1):
				# Runners on second and third
				run(1)
				on_base[3] = on_base[2]
				on_base[2] = -1
				on_base[1] = current_batter[batting_team()]
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] > -1):
				# Bases loaded
				run(1)
				on_base[3] = on_base[2]
				on_base[2] = on_base[1]
				on_base[1] = current_batter[batting_team()]
			elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] > -1):
				# Runners on first and third
				run(1)
				on_base[3] = -1
				on_base[2] = on_base[1]
				on_base[1] = current_batter[batting_team()]

			batters[batting_team()][current_batter[batting_team()]][4] += 1  # Batter hit count for box score
			pitchers_used[pitching_team()][-1][4] += 1 # Pitcher hit count for box score

			resetcount()
			pitch_result = "Single"
		elif 88 <= rand <= 93:  # Double

			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					continue
				else:
					pitch_result = "Double"
			else:
				pitch_result == "Double"

			pitching_animation()
			ball_in_play_animation()
			print("\033[1;30;102mDOUBLE!\033[0m")
			if (on_base[1] == -1 and on_base[2] == -1 and on_base[3] == -1):
				# Bases empty
				on_base[2] = current_batter[batting_team()]
			elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] == -1):
				# Runner on first
				on_base[3] = on_base[1]
				on_base[2] = current_batter[batting_team()]
				on_base[1] = -1
			elif (on_base[1] == -1 and on_base[2] > -1 and on_base[3] == -1):
				# Runner on second
				run(1)
				on_base[2] = -1
			elif (on_base[1] == -1 and on_base[2] == -1 and on_base[3] > -1):
				# Runner on third
				run(1)
				on_base[3] = -1
				on_base[2] = current_batter[batting_team()]
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] == -1):
				# Runners on first and second
				run(2)
				on_base[2] = current_batter[batting_team()]
				on_base[1] = -1
			elif (on_base[1] == -1 and on_base[2] > -1 and on_base[3] > -1):
				# Runners on second and third
				run(2)
				on_base[2] = current_batter[batting_team()]
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] > -1):
				# Bases loaded
				run(3)
				on_base[3] = on_base[1]
				on_base[2] = current_batter[batting_team()]
				on_base[1] = -1
			elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] > -1):
				# Runners on first and third
				run(2)
				on_base[3] = on_base[1]
				on_base[2] = current_batter[batting_team()]
				on_base[1] = -1

			batters[batting_team()][current_batter[batting_team()]][4] += 1  # Batter hit count for box score
			pitchers_used[pitching_team()][-1][4] += 1 # Pitcher hit count for box score

			resetcount()
			pitch_result = "Double"

		elif 94 <= rand <= 98:  # Home run

			if edge_pos == "pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					continue
				else:
					pitch_result = "Home run"
			else:
				pitch_result == "Home run"

			pitching_animation()
			ball_in_play_animation()
			print("\033[1;30;102mHOME RUN!\033[0m")
			if (on_base[1] == -1 and on_base[2] == -1 and on_base[3] == -1):
				# Bases empty
				run(1)
			elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] == -1):
				# Runner on first
				run(2)
			elif (on_base[1] == -1 and on_base[2] > -1 and on_base[3] == -1):
				# Runner on second
				run(2)
			elif (on_base[1] == -1 and on_base[2] == -1 and on_base[3] > -1):
				# Runner on third
				run(2)
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] == -1):
				# Runners on first and second
				run(3)
			elif (on_base[1] == -1 and on_base[2] > -1 and on_base[3] > -1):
				# Runners on second and third
				run(3)
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] > -1):
				# Bases loaded
				run(4)
			elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] > -1):
				# Runners on first and third
				run(3)

			batters[batting_team()][current_batter[batting_team()]][4] += 1  # Hit count for box score
			batters[batting_team()][current_batter[batting_team()]][6] += 1  # HR count for box score
			pitchers_used[pitching_team()][-1][4] += 1 # Pitcher hit count for box scoure
			pitchers_used[pitching_team()][-1][6] += 1 # Pitcher HR count for box score

			resetcount()
			pitch_result = "Home run"

			on_base[1] = -1
			on_base[2] = -1
			on_base[3] = -1

		elif 97 <= rand <= 99:  # Hit by pitch

			if edge_pos == "pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					continue
				else:
					pitch_result = "Hit by pitch"
			else:
				pitch_result == "Hit by pitch"

			pitching_animation()
			print("\033[1;30;102mHIT BY PITCH!\033[0m")
			if (on_base[1] == -1 and on_base[2] == -1 and on_base[3] == -1):
				# Bases empty
				on_base[1] = current_batter[batting_team()]
			elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] == -1):
				# Runner on first
				on_base[2] = on_base[1]
				on_base[1] = current_batter[batting_team()]
			elif (on_base[1] == -1 and on_base[2] > -1 and on_base[3] == -1):
				# Runner on second
				on_base[1] = current_batter[batting_team()]
			elif (on_base[1] == -1 and on_base[2] == -1 and on_base[3] > -1):
				# Runner on third
				on_base[1] = current_batter[batting_team()]
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] == -1):
				# Runners on first and second
				on_base[3] = on_base[2]
				on_base[2] = on_base[1]
				on_base[1] = current_batter[batting_team()]
			elif (on_base[1] == -1 and on_base[2] > -1 and on_base[3] > -1):
				# Runners on second and third
				on_base[1] = current_batter[batting_team()]
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] > -1):
				# Bases loaded
				run(1)
				on_base[3] = on_base[2]
				on_base[2] = on_base[1]
				on_base[1] = current_batter[batting_team()]
			elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] > -1):
				# Runners on first and third
				on_base[2] = on_base[1]
				on_base[1] = current_batter[batting_team()]
				resetcount()
			pitch_result = "Hit by pitch"
		else:  # Triple

			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					continue
				else:
					pitch_result = "Triple"
			else:
				pitch_result == "Triple"

			pitching_animation()
			ball_in_play_animation()
			print("\033[1;30;102mTRIPLE!\033[0m")
			if (on_base[1] == -1 and on_base[2] == -1 and on_base[3] == -1):
				# Bases empty
				on_base[3] = current_batter[batting_team()]
			elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] == -1):
				# Runner on first
				run(1)
				on_base[3] = current_batter[batting_team()]
				on_base[1] = -1
			elif (on_base[1] == -1 and on_base[2] > -1 and on_base[3] == -1):
				# Runner on second
				run(1)
				on_base[3] = current_batter[batting_team()]
				on_base[2] = -1
			elif (on_base[1] == -1 and on_base[2] == -1 and on_base[3] > -1):
				# Runner on third
				run(1)
				on_base[3] = current_batter[batting_team()]
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] == -1):
				# Runners on first and second
				run(2)
				on_base[3] = current_batter[batting_team()]
				on_base[2] = -1
				on_base[1] = -1
			elif (on_base[1] == -1 and on_base[2] > -1 and on_base[3] > -1):
				# Runners on second and third
				run(2)
				on_base[3] = current_batter[batting_team()]
				on_base[2] = -1
			elif (on_base[1] > -1 and on_base[2] > -1 and on_base[3] > -1):
				# Bases loaded
				run(3)
				on_base[3] = current_batter[batting_team()]
				on_base[2] = -1
				on_base[1] = -1
			elif (on_base[1] > -1 and on_base[2] == -1 and on_base[3] > -1):
				# Runners on first and third
				run(2)
				on_base[3] = current_batter[batting_team()]
				on_base[1] = -1

				batters[batting_team()][current_batter[batting_team()]][4] += 1  # Batter hit count for box score
				pitchers_used[pitching_team()][-1][4] += 1 # Pitcher hit count for box score

			resetcount()
			pitch_result = "Triple"

	atbat_pitch_count += 1
	redo_pitch_loops = 0
	pitch_count[pitching_team()] += 1

	if (
		pitch_result == "Walk"
		or pitch_result == "Single"
		or pitch_result == "Double"
		or pitch_result == "Triple"
		or pitch_result == "Home run"
		or pitch_result == "Hit by pitch"
		or pitch_result == "Strikeout"
		or pitch_result == "Grounder"
		or pitch_result == "Fly"
		or pitch_result == "Sacrifice fly"
	):
		# At-bat is over

		# Determine and set who the next batter is
		if current_batter[batting_team()] < 8:
			current_batter[batting_team()] += 1
		elif current_batter[batting_team()] == 8:
			current_batter[batting_team()] = 0

		atbat_pitch_count = 1

		print("")

		if gameover == True:
			break

		check_if_pitching_change()

		status()

	wait()

#######################################################################################################################
#######################################################################################################################

# Game over

wait_short()
print("")
wait_short()
print("")
wait_short()
print("")

if home_score > away_score:
	print("Game has ended. \033[1;93;40m" + teams["home"] + " win!\033[0m")
elif home_score < away_score:
	print("Game has ended. \033[1;93;40m" + teams["away"] + " win!\033[0m")

wait()
print("")
wait_short()
print("")

wait_short()
print("")
wait_short()
print("---Box Score---")
wait_short()
print("First pitch: " + str(first_pitch_time))
wait_short()
print("")
wait_short()

###########################################################
##Line score

if away_score > home_score:
	# Away won
	if len(score_by_inning["home"]) < len(score_by_inning["away"]):
		score_by_inning["home"].append(0)

print(abbrs["away"]  + " ", end="")
#for x in away_score_by_inning:
for x in score_by_inning["away"]:
	wait_short()
	print(str(x) + " ", end="")
wait_short()
print("- \033[1;93;40m" + str(away_score) + "\033[0m")

wait_short()
print(abbrs["home"]  + " ", end="")
for x in score_by_inning["home"]:
	wait_short()
	print(str(x) + " ", end="")

if len(score_by_inning["away"]) < len(score_by_inning["home"]):
	print("  ", end="")
wait_short()
print("- \033[1;93;40m" + str(home_score) + "\033[0m\n")




PrintBoxScore(teams, batters, pitchers_used)



save_results = input("Save box score to a text file? (Y/N)")

#######################################################################################################################
#######################################################################################################################

if save_results == "y" or save_results == "Y":

	results_filename = (
		"Game on "
		+ (datetime.strftime(datetime.now(), "%Y"))
		+ "-"
		+ (datetime.strftime(datetime.now(), "%m"))
		+ "-"
		+ (datetime.strftime(datetime.now(), "%d"))
		+ " at "
		+ (datetime.strftime(datetime.now(), "%H"))
		+ (datetime.strftime(datetime.now(), "%M"))
		+ ".txt"
	)
	file1 = open(results_filename, "w+")
	file1.write("---Box Score---\n")
	file1.write("First pitch: " + str(first_pitch_time) + "\n\n")

	###########################################################
	##Line score
	file1.write(abbrs["away"]  + " ")
	for x in score_by_inning["away"]:
		file1.write(str(x) + " ")
	file1.write("- " + str(away_score) + "\n")

	file1.write(abbrs["home"]  + " ")
	for x in score_by_inning["home"]:
		file1.write(str(x) + " ")
	if len(score_by_inning["home"]) < len(score_by_inning["away"]):
		file1.write("  ")
	file1.write("- " + str(home_score) + "\n\n")

	file1.write("Batting\n\n")

	###########################################################
	# Box score - Away batting
	file1.write(teams["away"].upper())
	for y in range(25 - len(teams["away"])):
		file1.write(" ")
	file1.write("AB   R   H  RBI HR  BB  SO\n")

	for x in batters["away"]:
		# Player name

		file1.write(x[0] + " ")

		# Print correct amount of spaces
		for y in range(25 - len(str(x[0]))):
			file1.write(" ")

		# First column
		file1.write(str(x[2]))

		# Columns 2-6
		for z in range(3, 8):
			if len(str(x[z])) > 1:
				file1.write("  ")
			else:
				file1.write("   ")
			if x[z] > 0:
				file1.write(str(x[z]))
			else:
				file1.write(str(x[z]))

		# Last column
		if len(str(x[7])) > 1:
			file1.write("  ")
		else:
			file1.write("   ")
		file1.write(str(x[8]) + "\n")

	# Add up away batting totals
	away_total = [0, 0, 0, 0, 0, 0, 0]
	for x in range(0, 9):
		away_total[0] = away_total[0] + batters["away"][x][2]  # AB
		away_total[1] = away_total[1] + batters["away"][x][3]  # R
		away_total[2] = away_total[2] + batters["away"][x][4]  # H
		away_total[3] = away_total[3] + batters["away"][x][5]  # RBI
		away_total[4] = away_total[4] + batters["away"][x][6]  # HR
		away_total[5] = away_total[5] + batters["away"][x][7]  # BB
		away_total[6] = away_total[6] + batters["away"][x][8]  # SO

	file1.write("Totals:                  " + str(away_total[0]))

	# Totals, Columns 1-6
	for z in range(1, 6):
		if len(str(away_total[z])) > 1:
			file1.write("  ")
		else:
			file1.write("   ")

		if away_total[z] > 0:
			file1.write(str(away_total[z]))
		else:
			file1.write(str(away_total[z]))

	# Totals, Column 7
	if len(str(away_total[6])) > 1:
		file1.write("  ")
	else:
		file1.write("   ")
	file1.write(str(away_total[6]) + "\n\n")

	###########################################################
	# Box score - Home batting
	file1.write(teams["home"].upper())
	for y in range(25 - len(teams["home"])):
		file1.write(" ")
	file1.write("AB   R   H  RBI HR  BB  SO\n")

	for x in batters["home"]:
		# Player name

		file1.write(x[0] + " ")

		# Print correct amount of spaces
		for y in range(25 - len(str(x[0]))):
			file1.write(" ")

		# First column
		file1.write(str(x[2]))

		# Columns 2-6
		for z in range(3, 8):
			if len(str(x[z])) > 1:
				file1.write("  ")
			else:
				file1.write("   ")
			if x[z] > 0:
				file1.write(str(x[z]))
			else:
				file1.write(str(x[z]))

		# Last column
		if len(str(x[7])) > 1:
			file1.write("  ")
		else:
			file1.write("   ")
		file1.write(str(x[8]) + "\n")

	# Add up home batting totals
	home_total = [0, 0, 0, 0, 0, 0, 0]
	for x in range(0, 9):
		home_total[0] = home_total[0] + batters["home"][x][2]  # AB
		home_total[1] = home_total[1] + batters["home"][x][3]  # R
		home_total[2] = home_total[2] + batters["home"][x][4]  # H
		home_total[3] = home_total[3] + batters["home"][x][5]  # RBI
		home_total[4] = home_total[4] + batters["home"][x][6]  # HR
		home_total[5] = home_total[5] + batters["home"][x][7]  # BB
		home_total[6] = home_total[6] + batters["home"][x][8]  # SO

	file1.write("Totals:                  " + str(home_total[0]))

	# Totals, columns 1-6
	for z in range(1, 6):
		if len(str(home_total[z])) > 1:
			file1.write("  ")
		else:
			file1.write("   ")

		if home_total[z] > 0:
			file1.write(str(home_total[z]))
		else:
			file1.write(str(home_total[z]))

	# Totals, column 7
	if len(str(home_total[6])) > 1:
		file1.write("  ")
	else:
		file1.write("   ")
	file1.write(str(home_total[6]) + "\n\n")

	file1.write("Pitching\n\n")

	###########################################################
	# Box score - Away pitching
	file1.write(teams["away"].upper())
	for y in range(25 - len(teams["away"])):
		file1.write(" ")
	file1.write("IP   R   H  ER  HR  BB  SO\n")

	for x in pitchers_used["away"]:
		# Player name
		file1.write(x[0] + " ")

		# Print correct amount of spaces
		for y in range(23 - len(str(x[0]))):
			file1.write(" ")

		# Column 1
		if len(str(round(x[2], 1))) == 1:
			file1.write("  ")
		file1.write(str(round(x[2], 1)))

		# Columns 2-6
		for z in range(3, 8):
			if len(str(x[z])) > 1:
				file1.write("  ")
			else:
				file1.write("   ")

			if x[3] > 0:
				file1.write(str(x[3]))
			else:
				file1.write(str(x[3]))

		# Last column
		if len(str(x[7])) > 1:
			file1.write("  ")
		else:
			file1.write("   ")
		file1.write(str(x[8]) + "\n")

	# Add up away pitching totals
	away_total = [0, 0, 0, 0, 0, 0, 0]
	for x in range(0, len(pitchers_used["away"])):
		away_total[0] = away_total[0] + pitchers_used["away"][x][2]  # IP
		away_total[1] = away_total[1] + pitchers_used["away"][x][3]  # R
		away_total[2] = away_total[2] + pitchers_used["away"][x][4]  # H
		away_total[3] = away_total[3] + pitchers_used["away"][x][5]  # ER
		away_total[4] = away_total[4] + pitchers_used["away"][x][6]  # HR
		away_total[5] = away_total[5] + pitchers_used["away"][x][7]  # BB
		away_total[6] = away_total[6] + pitchers_used["away"][x][8]  # SO

	file1.write("Totals:                 " + str(round(away_total[0], 1)))

	# Totals, columns 2-6
	for z in range(1, 6):
		if len(str(away_total[z])) > 1:
			file1.write("  ")
		else:
			file1.write("   ")

		if away_total[z] > 0:
			file1.write(str(away_total[z]))
		else:
			file1.write(str(away_total[z]))

	# Totals, column 7
	if len(str(away_total[6])) > 1:
		file1.write("  ")
	else:
		file1.write("   ")
	file1.write(str(away_total[6]) + "\n\n")

	###########################################################
	# Box score - Home pitching
	file1.write(teams["home"].upper())
	for y in range(25 - len(teams["home"])):
		file1.write(" ")
	file1.write("IP   R   H  ER  HR  BB  SO\n")

	for x in pitchers_used["home"]:
		# Player name
		file1.write(x[0] + " ")

		# Print correct amount of spaces
		for y in range(23 - len(str(x[0]))):
			file1.write(" ")

		# Column 1
		if len(str(round(x[2], 1))) == 1:
			file1.write("  ")
		file1.write(str(round(x[2], 1)))

		# Columns 2-6
		for z in range(3, 8):
			if len(str(x[z])) > 1:
				file1.write("  ")
			else:
				file1.write("   ")

			if x[3] > 0:
				file1.write(str(x[3]))
			else:
				file1.write(str(x[3]))

		# Last column
		if len(str(x[7])) > 1:
			file1.write("  ")
		else:
			file1.write("   ")
		file1.write(str(x[8]) + "\n")

	# Add up home pitching totals
	home_total = [0, 0, 0, 0, 0, 0, 0]
	for x in range(0, len(pitchers_used["home"])):
		home_total[0] = home_total[0] + pitchers_used["home"][x][2]  # IP
		home_total[1] = home_total[1] + pitchers_used["home"][x][3]  # R
		home_total[2] = home_total[2] + pitchers_used["home"][x][4]  # H
		home_total[3] = home_total[3] + pitchers_used["home"][x][5]  # ER
		home_total[4] = home_total[4] + pitchers_used["home"][x][6]  # HR
		home_total[5] = home_total[5] + pitchers_used["home"][x][7]  # BB
		home_total[6] = home_total[6] + pitchers_used["home"][x][8]  # SO

	file1.write("Totals:                 " + str(round(home_total[0], 1)))

	# Totals, columns 2-6
	for z in range(1, 6):
		if len(str(home_total[z])) > 1:
			file1.write("  ")
		else:
			file1.write("   ")

		if home_total[z] > 0:
			file1.write(str(home_total[z]))
		else:
			file1.write(str(home_total[z]))

	# Totals, column 7
	if len(str(home_total[6])) > 1:
		file1.write("  ")
	else:
		file1.write("   ")
	file1.write(str(home_total[6]))
	print("Box score saved to " + results_filename)
