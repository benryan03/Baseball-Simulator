import random

def calculate_pitch_outcome(pitch, redo_pitch, edge_pos, margin, redo_pitch_loops): #Needs cleanup

	# This function attempts to replicate real-world outcomes as accurately as possible.
	# Probability data was taken from this post:
	# https://www.baseball-fever.com/forum/general-baseball/statistics-analysis-sabermetrics/81427-pitch-outcome-distribution-over-25-years
	# Pitches 1-12 of each at bat match the probability data.
	# If pitch 13 is reached, there is no foul outcome, to help prevent infinite at-bats.

	# For each pitch, a random number between from 1 to 100 is generated. That number is used to determine the pitch outcome.
	# If the pitcher has the "edge", and the outcome is a ball or a ball in play (or vice versa), a second random number from 1 to 100 is generated.
	# If the second random number is between 0 and the edge %, the pitch outcome is disregarded and starts over.

	# So, if the pitcher has a 20% edge over the batter, and the initial outcome was a ball, there is a 20% chance of a do-over.

	rand = random.randint(1, 100)

	if pitch == 1:
		if rand >= 1 and rand <= 43:  # Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):  # Do-over?
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >= 44 and rand <= 72:  # Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):  # Do-over?
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 73 and rand <= 82:  # Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):  # Do-over?
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 83 and rand <= 88:  # Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):  # Do-over?
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		else:  # Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):  # Do-over?
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 2:
		if rand >= 1 and rand <= 40:  # Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >= 41 and rand <= 56:  # Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 57 and rand <= 72:  # Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 73 and rand <= 81:  # Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		else:  # Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 3:
		if rand >= 1 and rand <= 39:  # Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >= 40 and rand <= 52:  # Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 53 and rand <= 70:  # Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 71 and rand <= 80:  # Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		else:  # Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 4:
		if rand >= 1 and rand <= 35:  # Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >= 36 and rand <= 47:  # Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 48 and rand <= 68:  # Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 69 and rand <= 80:  # Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		else:  # Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 5:
		if rand >= 1 and rand <= 31:  # Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >= 32 and rand <= 40:  # Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 41 and rand <= 61:  # Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 62 and rand <= 73:  # Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		else:  # Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 6:
		if rand >= 1 and rand <= 26:  # Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >= 27 and rand <= 30:  # Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 31 and rand <= 53:  # Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 54 and rand <= 65:  # Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		else:  # Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 7:
		if rand >= 1 and rand <= 25:  # Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >= 26 and rand <= 29:  # Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 30 and rand <= 57:  # Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 58 and rand <= 69:  # Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		else:  # Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 8:
		if rand >= 1 and rand <= 24:  # Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >= 25 and rand <= 28:  # Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 29 and rand <= 57:  # Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 58 and rand <= 68:  # Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		else:  # Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 9:
		if rand >= 1 and rand <= 23:  # Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >= 24 and rand <= 26:  # Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 27 and rand <= 57:  # Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 58 and rand <= 68:  # Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		else:  # Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 10:
		if rand >= 1 and rand <= 22:  # Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >= 23 and rand <= 25:  # Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 26 and rand <= 57:  # Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 58 and rand <= 68:  # Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		else:  # Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 11:
		if rand >= 1 and rand <= 22:  # Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >= 23 and rand <= 25:  # Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		elif rand >= 26 and rand <= 57:  # Foul
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 58 and rand <= 68:  # Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		else:  # Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"
	elif pitch == 12:
		if rand >= 1 and rand <= 28:  # Ball
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball"
			else:
				return "Ball"
		elif rand >= 29 and rand <= 40:  # Called Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Foul"
			else:
				return "Foul"
		elif rand <= 41 and rand <= 58:  # Swinging Strike
			if edge_pos == "Batter":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Strike"
			else:
				return "Strike"
		else:  # Ball in play
			if edge_pos == "Pitcher":
				rand = random.randint(1, 100)
				if 1 <= rand <= round(margin, 0):
					redo_pitch_loops += 1
					return calculate_pitch_outcome(pitch, True, edge_pos, margin, redo_pitch_loops)
				else:
					return "Ball_in_play"
			else:
				return "Ball_in_play"