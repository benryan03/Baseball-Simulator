import time

def wait_short2():
	time.sleep(.5)  # default .5

def PrintBoxScore(teams, batters, pitchers_used):

    wait_short2()
    print("Batting")
    wait_short2()
    print("")
    wait_short2()

    ###########################################################
    # Box score - Away batting
    print(teams["away"].upper(), end="")
    for y in range(25 - len(teams["away"])):
        print(" ", end="")
    print("AB   R   H  RBI HR  BB  SO")

    for x in batters["away"]:
        # Player name
        wait_short2()
        print(x[0] + " ", end="")

        # Print correct amount of spaces
        for y in range(25 - len(str(x[0]))):
            print(" ", end="")

        # First column
        print("\033[1;93;40m" + str(x[2]) + "\033[0m", end="")

        # Columns 2-6
        for z in range(3, 8):
            if len(str(x[z])) > 1:
                print("  ", end="")
            else:
                print("   ", end="")
            if x[z] > 0:
                print("\033[1;93;40m" + str(x[z]) + "\033[0m", end="")
            else:
                print(str(x[z]), end="")

        # Last column
        if len(str(x[7])) > 1:
            print("  ", end="")
        else:
            print("   ", end="")
        if x[8] > 0:
            print("\033[1;93;40m" + str(x[8]) + "\033[0m")
        else:
            print(str(x[8]))

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

    wait_short2()
    print("Totals:                  " + str(away_total[0]), end="")

    # Totals, Columns 1-6
    for z in range(1, 6):
        if len(str(away_total[z])) > 1:
            print("  ", end="")
        else:
            print("   ", end="")

        if away_total[z] > 0:
            print("\033[1;93;40m" + str(away_total[z]) + "\033[0m", end="")
        else:
            print(str(away_total[z]), end="")

    # Totals, Column 7
    if len(str(away_total[6])) > 1:
        print("  ", end="")
    else:
        print("   ", end="")

    if away_total[6] > 0:
        print("\033[1;93;40m" + str(away_total[6]) + "\033[0m")
    else:
        print(str(away_total[6]))

    print("")

    ###########################################################
    # Box score - Home batting
    print(teams["home"].upper(), end="")
    for y in range(25 - len(teams["home"])):
        print(" ", end="")
    print("AB   R   H  RBI HR  BB  SO")

    for x in batters["home"]:
        # Player name
        wait_short2()
        print(x[0] + " ", end="")

        # Print correct amount of spaces
        for y in range(25 - len(str(x[0]))):
            print(" ", end="")

        # First column
        print("\033[1;93;40m" + str(x[2]) + "\033[0m", end="")

        # Columns 2-6
        for z in range(3, 8):
            if len(str(x[z])) > 1:
                print("  ", end="")
            else:
                print("   ", end="")
            if x[z] > 0:
                print("\033[1;93;40m" + str(x[z]) + "\033[0m", end="")
            else:
                print(str(x[z]), end="")

        # Last column
        if len(str(x[7])) > 1:
            print("  ", end="")
        else:
            print("   ", end="")
        if x[8] > 0:
            print("\033[1;93;40m" + str(x[8]) + "\033[0m")
        else:
            print(str(x[8]))

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

    wait_short2()
    print("Totals:                  " + str(home_total[0]), end="")

    # Totals, columns 1-6
    for z in range(1, 6):
        if len(str(home_total[z])) > 1:
            print("  ", end="")
        else:
            print("   ", end="")

        if home_total[z] > 0:
            print("\033[1;93;40m" + str(home_total[z]) + "\033[0m", end="")
        else:
            print(str(home_total[z]), end="")

    # Totals, column 7
    if len(str(home_total[6])) > 1:
        print("  ", end="")
    else:
        print("   ", end="")
    if home_total[6] > 0:
        print("\033[1;93;40m" + str(home_total[6]) + "\033[0m")
    else:
        print(str(home_total[6]))

    print("")
    wait_short2()
    print("Pitching")
    wait_short2()
    print("")
    wait_short2

    ###########################################################
    # Box score - Away pitching
    print(teams["away"].upper(), end="")
    for y in range(25 - len(teams["away"])):
        print(" ", end="")
    print("IP   R   H  ER  HR  BB  SO")

    wait_short2()
    for x in pitchers_used["away"]:
        # Player name
        print(x[0] + " ", end="")

        # Print correct amount of spaces
        for y in range(23 - len(str(x[0]))):
            print(" ", end="")

        # Column 1
        if len(str(round(x[2], 1))) == 1:
            print("  ", end="")
        print("\033[1;93;40m" + str(round(x[2], 1)) + "\033[0m", end="")

        # Columns 2-6
        for z in range(3, 8):
            if len(str(x[z])) > 1:
                print("  ", end="")
            else:
                print("   ", end="")

            if x[3] > 0:
                print("\033[1;93;40m" + str(x[3]) + "\033[0m", end="")
            else:
                print(str(x[3]), end="")

        # Last column
        if len(str(x[7])) > 1:
            print("  ", end="")
        else:
            print("   ", end="")
        if x[8] > 0:
            print("\033[1;93;40m" + str(x[8]) + "\033[0m")
        else:
            print(str(x[8]))

        wait_short2()

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

    wait_short2()
    print("Totals:                 " + str(round(away_total[0], 1)), end="")

    # Totals, columns 2-6
    for z in range(1, 6):
        if len(str(away_total[z])) > 1:
            print("  ", end="")
        else:
            print("   ", end="")

        if away_total[z] > 0:
            print("\033[1;93;40m" + str(away_total[z]) + "\033[0m", end="")
        else:
            print(str(away_total[z]), end="")

    # Totals, column 7
    if len(str(away_total[6])) > 1:
        print("  ", end="")
    else:
        print("   ", end="")
    if away_total[6] > 0:
        print("\033[1;93;40m" + str(away_total[6]) + "\033[0m")
    else:
        print(str(away_total[6]))

    print("")
    wait_short2()


    ###########################################################
    # Box score - Home pitching
    print(teams["home"].upper(), end="")
    for y in range(25 - len(teams["home"])):
        print(" ", end="")
    print("IP   R   H  ER  HR  BB  SO")

    wait_short2()
    for x in pitchers_used["home"]:
        # Player name
        print(x[0] + " ", end="")

        # Print correct amount of spaces
        for y in range(23 - len(str(x[0]))):
            print(" ", end="")

        # Column 1
        if len(str(round(x[2], 1))) == 1:
            print("  ", end="")
        print("\033[1;93;40m" + str(round(x[2], 1)) + "\033[0m", end="")

        # Columns 2-6
        for z in range(3, 8):
            if len(str(x[z])) > 1:
                print("  ", end="")
            else:
                print("   ", end="")

            if x[3] > 0:
                print("\033[1;93;40m" + str(x[3]) + "\033[0m", end="")
            else:
                print(str(x[3]), end="")

        # Last column
        if len(str(x[7])) > 1:
            print("  ", end="")
        else:
            print("   ", end="")
        if x[8] > 0:
            print("\033[1;93;40m" + str(x[8]) + "\033[0m")
        else:
            print(str(x[8]))

        wait_short2()

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

    wait_short2()
    print("Totals:                 " + str(round(home_total[0], 1)), end="")

    # Totals, columns 2-6
    for z in range(1, 6):
        if len(str(home_total[z])) > 1:
            print("  ", end="")
        else:
            print("   ", end="")

        if home_total[z] > 0:
            print("\033[1;93;40m" + str(home_total[z]) + "\033[0m", end="")
        else:
            print(str(home_total[z]), end="")

    # Totals, column 7
    if len(str(home_total[6])) > 1:
        print("  ", end="")
    else:
        print("   ", end="")
    if home_total[6] > 0:
        print("\033[1;93;40m" + str(home_total[6]) + "\033[0m")
    else:
        print(str(home_total[6]))

    print("")
    wait_short2()

    print("")
    wait_short2()
    wait_short2()
    print("")