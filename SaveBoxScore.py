from datetime import datetime

def SaveLineScore(results_filename, first_pitch_time, away_score, home_score, score_by_inning, abbrs):

	file1 = open(results_filename, "w+")
	file1.write("---Box Score---\n")
	file1.write("First pitch: " + str(first_pitch_time) + "\n\n")

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


def SaveBoxScore(results_filename, teams, batters, pitchers_used):

	file1 = open(results_filename, "a")
	# Away batting
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

	# Home batting
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

	# Away pitching
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

	# Home pitching
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
