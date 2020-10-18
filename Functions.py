import time
import math

def wait():  # Change both wait times to 0 for game to complete immediately
	time.sleep(2)  # default 2

def wait_short():
	time.sleep(.5)  # default .5

def batting_team(half_inning):
	if half_inning % 2 == 0:
		return "home"
	else:
		return "away"

def pitching_team(half_inning):
	if half_inning % 2 == 0:
		return "away"
	else:
		return "home"

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

def ball_in_play_animation():
	# flush=True makes sure time.sleep instances do not occur all at once
	print("\033[1;97;100mBall in play!\033[0m", end="", flush=True)
	for x in range(0, 6):
		wait_short()
		print("\033[1;97;100m .\033[0m", end="", flush=True)
	print("")

def pitching_animation(pitch_count, half_inning, current_pitcher, redo_pitch_loops):
	# flush=True makes sure time.sleep instances do not occur all at once
	print("\033[1;30;40mPitch " + str(pitch_count[pitching_team(half_inning)]) + " (" + current_pitcher[pitching_team(half_inning)][0] + ") \033[0m", end = "", flush=True)
	for x in range(0, 3):
		wait_short()
		print("\033[1;30;40m. \033[0m", end="", flush=True)

	for x in range(0, redo_pitch_loops):
		wait_short()
		print("\033[1;30;40m. \033[0m", end="", flush=True)

	print("")