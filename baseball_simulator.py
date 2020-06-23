#https://github.com/benryan03/baseball_simulator/

import random
import time
import math
from datetime import datetime

#To scrape players and stats from baseball-reference
from lxml import html
import requests

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

current_home_batter = 0
current_away_batter = 0
	
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

	wait()

	now_batting()
	
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

def now_batting():
	if half_inning % 2 == 0:
		print ("Now batting for " + home_team + ": " + str(home_batters[current_home_batter][0]) + ". " + str(home_year) + " AVG: " + format_batting_average(home_batters[current_home_batter][1]))
	else:
		print ("Now batting for " + away_team + ": " + str(away_batters[current_away_batter][0]) + ". " + str(away_year) + " AVG: " + format_batting_average(away_batters[current_away_batter][1]))

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

def wait(): #change these wait times to 0 for game to complete immediately
	time.sleep(2)

def wait_short():
	time.sleep(.2)

#######################################################################################################################
#######################################################################################################################

#program start

print ("Welcome to Baseball Simulator")
home_team = input("Enter the name of the home team: ")
home_year = input("Enter year: ")

away_team = input("Enter the name of the away team: ")
away_year = input("Enter year: ")

#home_team = "bos" #debug
#home_year = "2018" #debug
#away_team = "nyy" #debug
#away_year = "2018" #debug

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

home_closer = ["", ""]
away_closer = ["", ""]

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



print()
for x in home_pitchers:
	print(x)

print()
for x in away_pitchers:
	print(x)

print()
print(home_team + " closer: " + home_closer[0])

print()
print(away_team + " closer: " + away_closer[0])










print()
status()

while gameover == False: #main program loop

	#pitching animation
	print ("Pitching ", end="", flush=True)	# flush=True needs to be included, otherwise time.sleep instances will occur all at once
	for x in range (0, 3):
		wait_short()
		print (". ", end="", flush=True)
	print("")

	rand = random.randint(1, 100) #generate random number to determine result of pitch
	
	if 0 <= rand <= 36 and balls < 3: #Ball
		result = "Ball"
		balls = balls + 1
		print ("Ball. (" + str(balls) + " - " + str(strikes) + ")")

	elif 0 <= rand <= 36 and balls == 3: #Walk
		next_batter()
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

	elif 35 <= rand <= 67 and strikes <2: #Strike
		result = "Strike"
		strikes = strikes + 1
		print ("Strike. (" + str(balls) + " - " + str(strikes) + ")")

	elif 35 <= rand <= 67 and strikes ==2 and half_inning % 2 != 0: #Strikeout - away
		next_batter()
		result = "Strike"
		result = "Strikeout"
		print ("STRIKEOUT!")
		away_strikeout_count = away_strikeout_count + 1
		out(1)

	elif 35 <= rand <= 67 and strikes ==2 and half_inning % 2 == 0: #Strikeout - home
		next_batter()
		result = "Strike"
		result = "Strikeout"
		print ("STRIKEOUT!")
		home_strikeout_count = home_strikeout_count + 1
		out(1)

	elif 66 <= rand <= 77 and strikes < 2: #Foul
		result = "Foul"
		strikes = strikes + 1
		print ("Foul. (" + str(balls) + " - " + str(strikes) + ")")

	elif 66 <= rand <= 77 and strikes == 2: #Foul (with 2 strikes)
		result = "Foul"
		print ("Foul. (" + str(balls) + " - " + str(strikes) + ")")

	elif 76 <= rand <= 83: #Ground out
		next_batter()
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

	elif 82 <= rand <= 85: #Pop up
		next_batter()
		result = "Fly"
		print ("POPPED UP!")
		out(1)

	elif 84 <= rand <= 88: #Fly out
		next_batter()
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

	elif 87 <= rand <= 93: #Single
		next_batter()
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

	elif 92 <= rand <= 97: #Double
		next_batter()
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
	
	elif 96 <= rand <= 99: #Home run
		next_batter()
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

	elif 97 <= rand <= 101: #Hit by pitch
		next_batter()
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

	elif rand == 99: #Triple
		next_batter()
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
