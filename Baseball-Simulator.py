# https://github.com/benryan03/baseball_simulator/

import random
import time
import math
from datetime import datetime

# To scrape players and stats from baseball-reference
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

current_away_batter = 0
current_home_batter = -1

margin = 0
edge = ["", 0]

redo_pitch_loops = 0

runs_in_current_inning = 0

home_score_by_inning = []
away_score_by_inning = []

runners_on_base = [-1, -1, -1, -1]

earned_runs = 0


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
    global gameover
    global balls
    global strikes
    global runs_in_current_inning
    global runners_on_base
    for x in range(num):

        # For box score
        # Totals will get rounded to 1 decimal so .3333 is accurate enough :)
        if half_inning % 2 == 0:
            away_pitchers_used[-1][2] = away_pitchers_used[-1][2] + 0.3333
        elif half_inning % 2 != 0:
            home_pitchers_used[-1][2] = home_pitchers_used[-1][2] + 0.3333

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
            first = False
            second = False
            third = False
            runners_on_base = [-1, -1, -1, -1]
            balls = 0
            strikes = 0
            runs_in_current_inning = 0
            if half_inning == 2:
                print(
                    "\033[1;93;40m"
                    + away_starting_pitcher[0]
                    + "\033[0m is now pitching for the "
                    + away_team
                    + "."
                )
                wait()
                print(
                    str(away_year)
                    + " ERA: "
                    + str(format_era(away_starting_pitcher[1]))
                )
                wait()
        elif (
            outs == 2
            and half_inning >= 17
            and half_inning % 2 != 0
            and home_score <= away_score
        ):
            # if 2 outs and 9th inning or later and end of top of inning and away team is ahead or tied
            outs = 3
            print("")
            wait()
            half_inning += 1
            inning_status()
            outs = 0
            first = False
            second = False
            third = False
            runners_on_base = [-1, -1, -1, -1]
            balls = 0
            strikes = 0
        elif (
            outs == 2
            and half_inning >= 17
            and half_inning % 2 == 0
            and home_score == away_score
        ):
            # if 2 outs and 9th inning or later and end of bottom of inning and score is tied
            outs = 3
            print("")
            wait()
            half_inning += 1
            inning_status()
            outs = 0
            first = False
            second = False
            third = False
            runners_on_base = [-1, -1, -1, -1]
            balls = 0
            strikes = 0
        else:
            # Game over

            # This fixes a bug where sometimes the top of the 9th would not be shown in the line score
            if (
                half_inning % 2 != 0
                and home_score > away_score
                and len(away_score_by_inning) == len(home_score_by_inning)
            ):
                # Previous half inning was top
                if len(away_score_by_inning) < half_inning - 1:
                    away_score_by_inning.append(0)

            gameover = True


def run(num):  # Needs cleanup
    global half_inning
    global away_score
    global home_score
    global gameover
    global runs_in_current_inning
    global home_score_by_inning
    global away_score_by_inning
    global earned_runs

    runner1 = None
    runner2 = None
    runner3 = None
    runner4 = None

    # Determine and print who scored the run

    if half_inning % 2 != 0:  # Top half
        if num == 1:
            if runners_on_base[3] > -1:
                away_batters[runners_on_base[3]][3] += 1
                runner1 = away_batters[runners_on_base[3]]

            elif runners_on_base[2] > -1:
                away_batters[runners_on_base[2]][3] += 1
                runner1 = away_batters[runners_on_base[2]]

            elif runners_on_base[1] > -1:
                away_batters[runners_on_base[1]][3] += 1

            elif (
                runners_on_base[3] == -1
                and runners_on_base[2] == -1
                and runners_on_base[1] == -1
            ):
                away_batters[current_away_batter][3] += 1
                runner1 = away_batters[current_away_batter]

        elif num == 2:
            if runners_on_base[3] > -1 and runners_on_base[2] > -1:
                away_batters[runners_on_base[3]][3] += 1
                away_batters[runners_on_base[2]][3] += 1
                runner1 = away_batters[runners_on_base[3]]
                runner2 = away_batters[runners_on_base[2]]

            elif runners_on_base[3] > -1 and runners_on_base[1] > -1:
                away_batters[runners_on_base[3]][3] += 1
                away_batters[runners_on_base[1]][3] += 1
                runner1 = away_batters[runners_on_base[3]]
                runner2 = away_batters[runners_on_base[1]]

            elif runners_on_base[2] > -1 and runners_on_base[1] > -1:
                away_batters[runners_on_base[2]][3] += 1
                away_batters[runners_on_base[1]][3] += 1
                runner1 = away_batters[runners_on_base[2]]
                runner2 = away_batters[runners_on_base[1]]

            elif (
                runners_on_base[3] > -1
                and runners_on_base[2] == -1
                and runners_on_base[1] == -1
            ):
                away_batters[runners_on_base[3]][3] += 1
                away_batters[current_away_batter][3] += 1
                runner1 = away_batters[runners_on_base[3]]
                runner2 = away_batters[current_away_batter]

            elif (
                runners_on_base[3] == -1
                and runners_on_base[2] > -1
                and runners_on_base[1] == -1
            ):
                away_batters[runners_on_base[2]][3] += 1
                away_batters[current_away_batter][3] += 1
                runner1 = away_batters[runners_on_base[2]]
                runner2 = away_batters[current_away_batter]

            elif (
                runners_on_base[3] == -1
                and runners_on_base[2] == -1
                and runners_on_base[1] > -1
            ):
                away_batters[runners_on_base[1]][3] += 1
                away_batters[current_away_batter][3] += 1
                runner1 = away_batters[runners_on_base[1]]
                runner2 = away_batters[current_away_batter]

        elif num == 3:
            if (
                runners_on_base[3] > -1
                and runners_on_base[2] > -1
                and runners_on_base[1] > -1
            ):
                away_batters[runners_on_base[3]][3] += 1
                away_batters[runners_on_base[2]][3] += 1
                away_batters[runners_on_base[1]][3] += 1
                runner1 = away_batters[runners_on_base[3]]
                runner2 = away_batters[runners_on_base[2]]
                runner3 = away_batters[runners_on_base[1]]

            elif runners_on_base[3] > -1 and runners_on_base[2] > -1:
                away_batters[runners_on_base[3]][3] += 1
                away_batters[runners_on_base[2]][3] += 1
                away_batters[current_away_batter][3] += 1
                runner1 = away_batters[runners_on_base[3]]
                runner2 = away_batters[runners_on_base[2]]
                runner3 = away_batters[current_away_batter]

            elif runners_on_base[3] > -1 and runners_on_base[1] > -1:
                away_batters[runners_on_base[3]][3] += 1
                away_batters[runners_on_base[1]][3] += 1
                away_batters[current_away_batter][3] += 1
                runner1 = away_batters[runners_on_base[3]]
                runner2 = away_batters[runners_on_base[1]]
                runner3 = away_batters[current_away_batter]

            elif runners_on_base[2] > -1 and runners_on_base[1] > -1:
                away_batters[runners_on_base[2]][3] += 1
                away_batters[runners_on_base[1]][3] += 1
                away_batters[current_away_batter][3] += 1
                runner1 = away_batters[runners_on_base[2]]
                runner2 = away_batters[runners_on_base[1]]
                runner3 = away_batters[current_away_batter]

        elif num == 4:
            away_batters[runners_on_base[3]][3] += 1
            away_batters[runners_on_base[2]][3] += 1
            away_batters[runners_on_base[1]][3] += 1
            away_batters[current_away_batter][3] += 1
            runner1 = away_batters[runners_on_base[3]]
            runner2 = away_batters[runners_on_base[2]]
            runner3 = away_batters[runners_on_base[1]]
            runner4 = away_batters[current_away_batter]

        if runner1 != None:
            wait()
            print("")
            wait()
            print(
                "\033[1;30;102m"
                + runner1[0]
                + " scored a run for the "
                + away_team
                + "!\033[0m"
            )
        if runner2 != None:
            wait()
            print("")
            wait()
            print(
                "\033[1;30;102m"
                + runner2[0]
                + " scored a run for the "
                + away_team
                + "!\033[0m"
            )
        if runner3 != None:
            wait()
            print("")
            wait()
            print(
                "\033[1;30;102m"
                + runner3[0]
                + " scored a run for the "
                + away_team
                + "!\033[0m"
            )
        if runner4 != None:
            wait()
            print("")
            wait()
            print(
                "\033[1;30;102m"
                + runner4[0]
                + " scored a run for the "
                + away_team
                + "!\033[0m"
            )
    elif half_inning % 2 == 0:
        if num == 1:
            if runners_on_base[3] > -1:
                home_batters[runners_on_base[3]][3] += 1
                runner1 = home_batters[runners_on_base[3]]
            elif runners_on_base[2] > -1:
                home_batters[runners_on_base[2]][3] += 1
                runner1 = home_batters[runners_on_base[2]]
            elif runners_on_base[1] > -1:
                home_batters[runners_on_base[1]][3] += 1
            elif (
                runners_on_base[3] == -1
                and runners_on_base[2] == -1
                and runners_on_base[1] == -1
            ):
                home_batters[current_home_batter][3] += 1
                runner1 = home_batters[current_home_batter]
        elif num == 2:
            if runners_on_base[3] > -1 and runners_on_base[2] > -1:
                home_batters[runners_on_base[3]][3] += 1
                home_batters[runners_on_base[2]][3] += 1
                runner1 = home_batters[runners_on_base[3]]
                runner2 = home_batters[runners_on_base[2]]
            elif runners_on_base[3] > -1 and runners_on_base[1] > -1:
                home_batters[runners_on_base[3]][3] += 1
                home_batters[runners_on_base[1]][3] += 1
                runner1 = home_batters[runners_on_base[3]]
                runner2 = home_batters[runners_on_base[1]]
            elif runners_on_base[2] > -1 and runners_on_base[1] > -1:
                home_batters[runners_on_base[2]][3] += 1
                home_batters[runners_on_base[1]][3] += 1
                runner1 = home_batters[runners_on_base[2]]
                runner2 = home_batters[runners_on_base[1]]
            elif (
                runners_on_base[3] > -1
                and runners_on_base[2] == -1
                and runners_on_base[1] == -1
            ):
                home_batters[runners_on_base[3]][3] += 1
                home_batters[current_home_batter][3] += 1
                runner1 = home_batters[runners_on_base[3]]
                runner2 = home_batters[current_home_batter]
            elif (
                runners_on_base[3] == -1
                and runners_on_base[2] > -1
                and runners_on_base[1] == -1
            ):
                home_batters[runners_on_base[2]][3] += 1
                home_batters[current_home_batter][3] += 1
                runner1 = home_batters[runners_on_base[2]]
                runner2 = home_batters[current_home_batter]
            elif (
                runners_on_base[3] == -1
                and runners_on_base[2] == -1
                and runners_on_base[1] > -1
            ):
                home_batters[runners_on_base[1]][3] += 1
                home_batters[current_home_batter][3] += 1
                runner1 = home_batters[runners_on_base[1]]
                runner2 = home_batters[current_home_batter]
        elif num == 3:
            if (
                runners_on_base[3] > -1
                and runners_on_base[2] > -1
                and runners_on_base[1] > -1
            ):
                home_batters[runners_on_base[3]][3] += 1
                home_batters[runners_on_base[2]][3] += 1
                home_batters[runners_on_base[1]][3] += 1
                runner1 = home_batters[runners_on_base[3]]
                runner2 = home_batters[runners_on_base[2]]
                runner3 = home_batters[runners_on_base[1]]
            elif runners_on_base[3] > -1 and runners_on_base[2] > -1:
                home_batters[runners_on_base[3]][3] += 1
                home_batters[runners_on_base[2]][3] += 1
                home_batters[current_home_batter][3] += 1
                runner1 = home_batters[runners_on_base[3]]
                runner2 = home_batters[runners_on_base[2]]
                runner3 = home_batters[current_home_batter]
            elif runners_on_base[3] > -1 and runners_on_base[1] > -1:
                home_batters[runners_on_base[3]][3] += 1
                home_batters[runners_on_base[1]][3] += 1
                home_batters[current_home_batter][3] += 1
                runner1 = home_batters[runners_on_base[3]]
                runner2 = home_batters[runners_on_base[1]]
                runner3 = home_batters[current_home_batter]
            elif runners_on_base[2] > -1 and runners_on_base[1] > -1:
                home_batters[runners_on_base[2]][3] += 1
                home_batters[runners_on_base[1]][3] += 1
                home_batters[current_home_batter][3] += 1
                runner1 = home_batters[runners_on_base[2]]
                runner2 = home_batters[runners_on_base[1]]
                runner3 = home_batters[current_home_batter]
        elif num == 4:
            home_batters[runners_on_base[3]][3] += 1
            home_batters[runners_on_base[2]][3] += 1
            home_batters[runners_on_base[1]][3] += 1
            home_batters[current_home_batter][3] += 1
            runner1 = home_batters[runners_on_base[3]]
            runner2 = home_batters[runners_on_base[2]]
            runner3 = home_batters[runners_on_base[1]]
            runner4 = home_batters[current_home_batter]

        if runner1 != None:
            wait_short()
            print("")
            wait_short()
            print(
                "\033[1;30;102m"
                + runner1[0]
                + " scored a run for the "
                + home_team
                + "!\033[0m"
            )
        if runner2 != None:
            wait_short()
            print("")
            wait_short()
            print(
                "\033[1;30;102m"
                + runner2[0]
                + " scored a run for the "
                + home_team
                + "!\033[0m"
            )
        if runner3 != None:
            wait_short()
            print("")
            wait_short()
            print(
                "\033[1;30;102m"
                + runner3[0]
                + " scored a run for the "
                + home_team
                + "!\033[0m"
            )
        if runner4 != None:
            wait_short()
            print("")
            wait_short()
            print(
                "\033[1;30;102m"
                + runner4[0]
                + " scored a run for the "
                + home_team
                + "!\033[0m"
            )

    for x in range(num):
        if half_inning % 2 != 0:
            # run for away - line/box score
            home_pitchers_used[-1][3] += 1
            inning = int((half_inning / 2) + 0.5)
            if len(away_score_by_inning) < inning:
                away_score_by_inning.append(1)
            else:
                away_score_by_inning[-1] += 1

            if earned_runs < 0:
                earned_runs += 1
            else:
                home_pitchers_used[-1][5] += 1

        elif half_inning % 2 == 0:
            # run for home - line/box score
            away_pitchers_used[-1][3] += 1
            inning = int((half_inning / 2) + 0.5)
            if len(home_score_by_inning) < inning:
                home_score_by_inning.append(1)
            else:
                home_score_by_inning[-1] += 1

            if earned_runs < 0:
                earned_runs += 1
            else:
                away_pitchers_used[-1][5] += 1

        if half_inning < 18 and half_inning % 2 != 0:
            # normal innings - run for away
            away_score += 1
            runs_in_current_inning += (
                1  # For determining if there should be a pitching change
            )
            away_batters[current_away_batter][5] += 1  # RBI count for box score
            wait_short()
        elif half_inning < 18 and half_inning % 2 == 0:
            # normal innings - run for home
            home_score += 1
            runs_in_current_inning += (
                1  # For determining if there should be a pitching change
            )
            home_batters[current_home_batter][5] += 1  # RBI count for box score
            wait_short()
        elif half_inning >= 18 and half_inning % 2 != 0:
            # extra innings - run for away
            away_score += 1
            runs_in_current_inning += (
                1  # For determining if there should be a pitching change
            )
            away_batters[current_away_batter][5] += 1  # RBI count for box score
            wait_short()
        elif half_inning >= 18 and half_inning % 2 == 0 and away_score > home_score:
            # extra innings - run for home, no walkoff
            home_score += 1
            home_batters[current_home_batter][5] += 1  # RBI count for box score
            runs_in_current_inning += (
                1  # For determining if there should be a pitching change
            )
            wait_short()
        elif half_inning >= 18 and half_inning % 2 == 0 and away_score == home_score:
            # walkoff run!
            home_score += 1
            home_batters[current_home_batter][5] += 1  # RBI count for box score
            print("\033[1;30;102mWALKOFF for the " + home_team + "!\033[0m")
            wait()
            print("")
            wait()
            print("Game has ended. " + home_team + " wins.")
            gameover = True


def status():  # print number of outs, inning number, score, and on-base statuses

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
        + home_abbr
        + ": "
        + str(home_score)
        + " | "
        + away_abbr
        + ": "
        + str(away_score)
        + " | 3B: ",
        end="",
    )
    if third == True:
        print("\033[1;93;40mX\033[0m 2B: ", end="")
    elif third == False:
        print("  2B: ", end="")
    if second == True:
        print("\033[1;93;40mX\033[0m 1B: ", end="")
    elif second == False:
        print("  1B: ", end="")
    if first == True:
        print("\033[1;93;40mX\033[0m")
    elif first == False:
        print(" ")

    wait()
    now_batting()
    wait()


def now_batting():
    global edge
    global edge_pos
    global margin
    global redo_pitch_loops
    global home_batters
    global away_batters

    # Print name and average of current batter
    if half_inning % 2 == 0:
        print(
            "\033[1;93;40m"
            + str(home_batters[current_home_batter][0])
            + "\033[0m is now batting for the "
            + home_team
            + ". "
            + str(home_year)
            + " AVG: "
            + format_batting_average(home_batters[current_home_batter][1])
        )

        home_batters[current_home_batter][2] += 1  # Update at-bat count for box score
    else:
        print(
            "\033[1;93;40m"
            + str(away_batters[current_away_batter][0])
            + "\033[0m is now batting for the "
            + away_team
            + ". "
            + str(away_year)
            + " AVG: "
            + format_batting_average(away_batters[current_away_batter][1])
        )

        away_batters[current_away_batter][2] += 1  # Update at-bat count for box score

    redo_pitch_loops = 0

    # Determine advantage
    if half_inning % 2 == 0:  # Bottom half
        avg = home_batters[current_home_batter][1]
        era = current_away_pitcher[1]

        x = avg / 0.250
        y = (2 - (era / 4)) - (away_pitcher_pitch_count * 0.005)

        if x > y:
            # Batter has adventage
            edge = home_batters[current_home_batter][0]
            edge_pos = "Batter"
            margin = x - y

        elif x <= y:
            # Pitcher has advantage
            edge = current_away_pitcher[0]
            edge_pos = "Pitcher"
            margin = y - x

        wait()
        margin = round(margin * 50, 1)
        print("Edge: " + edge + " - " + str(margin) + "%")

    elif half_inning % 2 != 0:  # Top half
        avg = away_batters[current_away_batter][1]
        era = current_home_pitcher[1]

        x = avg / 0.250
        y = (2 - (era / 4)) - (home_pitcher_pitch_count * 0.005)

        if x > y:
            # Batter has adventage
            edge = away_batters[current_away_batter][0]
            edge_pos = "Batter"
            margin = x - y

        elif x <= y:
            # Pitcher has advantage
            edge = current_home_pitcher[0]
            edge_pos = "Pitcher"
            margin = y - x

        # Print edge
        wait()
        margin = round(margin * 50, 1)
        print("Edge: " + edge + " - " + str(margin) + "%")


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


def wait():  # change these wait times to 0 for game to complete immediately
    time.sleep(0)  # default 2


def wait_short():
    time.sleep(0)  # default .5


def calculate_pitch_outcome(pitch, redo_pitch):

    # This function attempts to replicate real-world outcomes as accurately as possible.
    # Probability data was taken from this post:
    # https://www.baseball-fever.com/forum/general-baseball/statistics-analysis-sabermetrics/81427-pitch-outcome-distribution-over-25-years
    # Pitches 1-12 of each at bat match the probability data.
    # If pitch 13 is reached, there is no foul outcome, to help prevent infinite at-bats.

    # For each pitch, a random number between from 1 to 100 is generated. That number is used to determine the pitch outcome.
    # If the pitcher has the "edge", and the outcome is a ball or a ball in play (or vice versa), a second random number from 1 to 100 is generated.
    # If the second random number is between 0 and the edge %, the pitch outcome is disregarded and starts over.

    # So, if the pitcher has a 20% edge over the batter, and the initial outcome was a ball, there is a 20% chance of a do-over.

    global redo_pitch_loops

    rand = random.randint(1, 100)

    if pitch == 1:
        if rand >= 1 and rand <= 43:  # Ball
            if edge_pos == "Pitcher":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):  # Do-over?
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Ball"
            else:
                return "Ball"
        elif rand >= 44 and rand <= 72:  # Called Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):  # Do-over?
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        elif rand >= 73 and rand <= 82:  # Foul
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):  # Do-over?
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Foul"
            else:
                return "Foul"
        elif rand <= 83 and rand <= 88:  # Swinging Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):  # Do-over?
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        else:  # Ball in play
            if edge_pos == "Pitcher":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):  # Do-over?
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
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
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Ball"
            else:
                return "Ball"
        elif rand >= 41 and rand <= 56:  # Called Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        elif rand >= 57 and rand <= 72:  # Foul
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Foul"
            else:
                return "Foul"
        elif rand <= 73 and rand <= 81:  # Swinging Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        else:  # Ball in play
            if edge_pos == "Pitcher":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
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
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Ball"
            else:
                return "Ball"
        elif rand >= 40 and rand <= 52:  # Called Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        elif rand >= 53 and rand <= 70:  # Foul
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Foul"
            else:
                return "Foul"
        elif rand <= 71 and rand <= 80:  # Swinging Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        else:  # Ball in play
            if edge_pos == "Pitcher":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
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
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Ball"
            else:
                return "Ball"
        elif rand >= 36 and rand <= 47:  # Called Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        elif rand >= 48 and rand <= 68:  # Foul
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Foul"
            else:
                return "Foul"
        elif rand <= 69 and rand <= 80:  # Swinging Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        else:  # Ball in play
            if edge_pos == "Pitcher":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
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
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Ball"
            else:
                return "Ball"
        elif rand >= 32 and rand <= 40:  # Called Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        elif rand >= 41 and rand <= 61:  # Foul
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Foul"
            else:
                return "Foul"
        elif rand <= 62 and rand <= 73:  # Swinging Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        else:  # Ball in play
            if edge_pos == "Pitcher":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
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
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Ball"
            else:
                return "Ball"
        elif rand >= 27 and rand <= 30:  # Called Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        elif rand >= 31 and rand <= 53:  # Foul
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Foul"
            else:
                return "Foul"
        elif rand <= 54 and rand <= 65:  # Swinging Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        else:  # Ball in play
            if edge_pos == "Pitcher":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
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
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Ball"
            else:
                return "Ball"
        elif rand >= 26 and rand <= 29:  # Called Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        elif rand >= 30 and rand <= 57:  # Foul
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Foul"
            else:
                return "Foul"
        elif rand <= 58 and rand <= 69:  # Swinging Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        else:  # Ball in play
            if edge_pos == "Pitcher":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
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
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Ball"
            else:
                return "Ball"
        elif rand >= 25 and rand <= 28:  # Called Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        elif rand >= 29 and rand <= 57:  # Foul
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Foul"
            else:
                return "Foul"
        elif rand <= 58 and rand <= 68:  # Swinging Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        else:  # Ball in play
            if edge_pos == "Pitcher":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
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
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Ball"
            else:
                return "Ball"
        elif rand >= 24 and rand <= 26:  # Called Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        elif rand >= 27 and rand <= 57:  # Foul
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Foul"
            else:
                return "Foul"
        elif rand <= 58 and rand <= 68:  # Swinging Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        else:  # Ball in play
            if edge_pos == "Pitcher":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
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
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Ball"
            else:
                return "Ball"
        elif rand >= 23 and rand <= 25:  # Called Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        elif rand >= 26 and rand <= 57:  # Foul
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Foul"
            else:
                return "Foul"
        elif rand <= 58 and rand <= 68:  # Swinging Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        else:  # Ball in play
            if edge_pos == "Pitcher":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
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
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Ball"
            else:
                return "Ball"
        elif rand >= 23 and rand <= 25:  # Called Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        elif rand >= 26 and rand <= 57:  # Foul
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Foul"
            else:
                return "Foul"
        elif rand <= 58 and rand <= 68:  # Swinging Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        else:  # Ball in play
            if edge_pos == "Pitcher":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
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
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Ball"
            else:
                return "Ball"
        elif rand >= 29 and rand <= 40:  # Called Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Foul"
            else:
                return "Foul"
        elif rand <= 41 and rand <= 58:  # Swinging Strike
            if edge_pos == "Batter":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
                    return calculate_pitch_outcome(pitch, True)
                else:
                    return "Strike"
            else:
                return "Strike"
        else:  # Ball in play
            if edge_pos == "Pitcher":
                rand = random.randint(1, 100)
                if 1 <= rand <= round(margin, 0):
                    redo_pitch_loops += 1
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

    print(
        "\033[1;30;40mPitch "
        + str(current_pitcher_pitch_count)
        + " ("
        + current_pitcher[0]
        + ") \033[0m",
        end="",
        flush=True,
    )  # flush=True makes sure time.sleep instances do not occur all at once
    for x in range(0, 3):
        wait_short()
        print("\033[1;30;40m. \033[0m", end="", flush=True)

    for x in range(0, redo_pitch_loops):
        wait_short()
        print("\033[1;30;40m. \033[0m", end="", flush=True)

    print("")


def ball_in_play_animation():

    print(
        "\033[1;97;100mBall in play!\033[0m", end="", flush=True
    )  # flush=True makes sure time.sleep instances do not occur all at once
    for x in range(0, 6):
        wait_short()
        print("\033[1;97;100m .\033[0m", end="", flush=True)
    print("")


def check_if_pitching_change():

    # Top half of inning
    if (
        half_inning % 2 != 0
        and current_home_pitcher == home_starting_pitcher
        and home_pitcher_pitch_count >= 100
    ):
        # Starter is still in and has thrown 100 pitches
        pitching_change()
    elif (
        half_inning % 2 != 0
        and current_home_pitcher == home_starting_pitcher
        and half_inning >= 13
    ):
        # Starter is still in and it is the top of the 7th inning
        pitching_change()
    elif (
        half_inning % 2 != 0
        and current_home_pitcher == home_starting_pitcher
        and away_score > 4
    ):
        # Starter is still in and has allowed more than 4 runs
        pitching_change()
    elif (
        half_inning % 2 != 0
        and current_home_pitcher != home_starting_pitcher
        and half_inning <= 9
        and runs_in_current_inning > 2
        and len(home_relief_pitchers) > 0
    ):
        # A reliever is in and has allowed more than 2 runs and it is before the 6th inning
        pitching_change()
    elif (
        half_inning % 2 != 0
        and current_home_pitcher != home_starting_pitcher
        and half_inning == 17
        and current_home_pitcher != home_closer
    ):
        # Top of 9th inning (Send in closer)
        pitching_change()
    elif (
        half_inning % 2 != 0
        and current_home_pitcher != home_starting_pitcher
        and half_inning > 9
        and outs == 0
        and first == False
        and second == False
        and third == False
        and runs_in_current_inning == 0
        and len(home_relief_pitchers) > 0
    ):
        # A reliever is in and it is the start of an inning, 6th or later
        pitching_change()
    elif (
        half_inning % 2 != 0
        and current_home_pitcher != home_starting_pitcher
        and runs_in_current_inning > 2
        and len(home_relief_pitchers) > 0
    ):
        # A reliever is in and has allowed more than 2 runs
        pitching_change()

    # Bottom half of inning
    elif (
        half_inning % 2 == 0
        and current_away_pitcher == away_starting_pitcher
        and away_pitcher_pitch_count >= 100
    ):
        # Starter is still in and has thrown 100 pitches
        pitching_change()
    elif (
        half_inning % 2 == 0
        and current_away_pitcher == away_starting_pitcher
        and half_inning >= 14
    ):
        # Starter is still in and it is the bottom of the 7th inning
        pitching_change()
    elif (
        half_inning % 2 == 0
        and current_away_pitcher == away_starting_pitcher
        and home_score > 4
    ):
        # Starter is still in and has allowed more than 4 runs
        pitching_change()
    elif (
        half_inning % 2 == 0
        and current_away_pitcher != away_starting_pitcher
        and half_inning <= 10
        and runs_in_current_inning > 2
        and len(away_relief_pitchers) > 0
    ):
        # A reliever is in and has allowed more than 2 runs and it is before the 6th inning
        pitching_change()
    elif (
        half_inning % 2 == 0
        and current_away_pitcher != away_starting_pitcher
        and half_inning == 17
        and current_away_pitcher != away_closer
    ):
        # Bottom of 9th inning (Send in closer)
        pitching_change()
    elif (
        half_inning % 2 == 0
        and current_away_pitcher != away_starting_pitcher
        and half_inning > 10
        and outs == 0
        and first == False
        and second == False
        and third == False
        and runs_in_current_inning == 0
        and len(away_relief_pitchers) > 0
    ):
        # A reliever is in and it is the start of an inning, 6th or later
        pitching_change()
    elif (
        half_inning % 2 == 0
        and current_away_pitcher != away_starting_pitcher
        and runs_in_current_inning > 2
        and len(away_relief_pitchers) > 0
    ):
        # A reliever is in and has allowed more than 2 runs
        pitching_change()


def pitching_change():
    global home_relief_pitchers
    global current_home_pitcher
    global home_pitcher_pitch_count
    global away_relief_pitchers
    global current_away_pitcher
    global away_pitcher_pitch_count
    global runs_in_current_inning
    global earned_runs

    # For determining if there should be a pitching change
    runs_in_current_inning = 0

    # Used for Earned Runs in box score
    earned_runs = 0
    if first == True:
        earned_runs = earned_runs - 1
    if second == True:
        earned_runs = earned_runs - 1
    if third == True:
        earned_runs = earned_runs - 1

    if half_inning % 2 != 0:  # Top of inning

        if half_inning == 17:
            # Top of 9th inning
            current_home_pitcher = home_closer
        else:
            # Choose a random relief pitcher
            x = len(home_relief_pitchers)
            rand = random.randint(0, x - 1)
            current_home_pitcher = home_relief_pitchers[rand]
            del home_relief_pitchers[rand]
            home_pitcher_pitch_count = 1

        home_pitchers_used.append(
            current_home_pitcher
        )  # Add pitcher to array for box score
        for x in range(10):  # Generate blank stats for box score
            home_pitchers_used[-1].append(0)

        # Print new pitcher
        wait()
        print("Pitching change!")
        wait()
        print("")
        wait()
        print(
            "\033[1;93;40m"
            + current_home_pitcher[0]
            + "\033[0m is now pitching for the "
            + home_team
            + "."
        )
        wait()
        print(str(home_year) + " ERA: " + str(format_era(current_home_pitcher[1])))
        wait()
        print("")
        wait()

    elif half_inning % 2 == 0:  # Bottom of inning

        if half_inning == 18:
            # Bottom of 9th inning
            current_away_pitcher = away_closer
        else:
            # Choose a random relief pitcher
            x = len(away_relief_pitchers)
            rand = random.randint(0, x - 1)
            current_away_pitcher = away_relief_pitchers[rand]
            del away_relief_pitchers[rand]
            away_pitcher_pitch_count = 1

        away_pitchers_used.append(
            current_away_pitcher
        )  # Add pitcher to array for box score
        for x in range(10):  # Generate blank stats for box score
            away_pitchers_used[-1].append(0)

        # Print new pitcher
        wait()
        print("Pitching change!")
        wait()
        print("")
        wait()
        print(
            "\033[1;93;40m"
            + current_away_pitcher[0]
            + "\033[0m is now pitching for the "
            + away_team
            + "."
        )
        wait()
        print(str(away_year) + " ERA: " + str(format_era(current_away_pitcher[1])))
        wait()
        print("")
        wait()


def inning_status():
    global half_inning

    # Update line score
    prev_half_inning = half_inning - 1
    if prev_half_inning % 2 == 0:  # it is now bottom of inning
        if len(away_score_by_inning) < prev_half_inning - 1:
            away_score_by_inning.append(0)
    elif prev_half_inning % 2 != 0:  # it is now top of inning
        if len(home_score_by_inning) < prev_half_inning - 1:
            home_score_by_inning.append(0)

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
    if half_inning % 2 != 0:
        wait()
        print("")
        print("")
        print("------------------------------------")
        print(
            "It is now the top of the "
            + str((half_inning / 2) + 0.5).split(".")[0]
            + x
            + " inning."
        )
        print("------------------------------------")
        print("")
        wait()

    elif half_inning % 2 == 0:
        wait()
        print("")
        print("")
        print("---------------------------------------")
        print(
            "It is now the bottom of the "
            + str(half_inning / 2).split(".")[0]
            + x
            + " inning."
        )
        print("---------------------------------------")
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
    home_page = requests.get(
        "https://www.baseball-reference.com/teams/"
        + home_abbr
        + "/"
        + home_year
        + ".shtml"
    )
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
    away_page = requests.get(
        "https://www.baseball-reference.com/teams/"
        + away_abbr
        + "/"
        + away_year
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
    "https://www.baseball-reference.com/teams/" + home_abbr + "/" + home_year + ".shtml"
)
home_tree = html.fromstring(home_page.content)
away_page = requests.get(
    "https://www.baseball-reference.com/teams/" + away_abbr + "/" + away_year + ".shtml"
)
away_tree = html.fromstring(away_page.content)

home_batters = ["", "", "", "", "", "", "", "", ""]
away_batters = ["", "", "", "", "", "", "", "", ""]

# Scrape names of top 8 batters
for x in range(8):
    # Home
    fullname = home_tree.xpath(
        '//table[@id="team_batting"]/tbody/tr[' + str(x + 1) + "]/td[2]/@csk"
    )
    fname = str(fullname).partition(",")[2]
    lname = str(fullname).partition(",")[0]
    home_batters[x] = fname.strip("[],'") + " " + lname.strip("[],'")

    # Away
    fullname = away_tree.xpath(
        '//table[@id="team_batting"]/tbody/tr[' + str(x + 1) + "]/td[2]/@csk"
    )
    fname = str(fullname).partition(",")[2]
    lname = str(fullname).partition(",")[0]
    away_batters[x] = fname.strip("[],'") + " " + lname.strip("[],'")

# Scrape name of 9th batter (sometimes the formatting on baseball-reference skips the 9th row)
# Home
fullname = home_tree.xpath('//table[@id="team_batting"]/tbody/tr[9]/td[2]/@csk')
if fullname == []:
    fullname = home_tree.xpath('//table[@id="team_batting"]/tbody/tr[10]/td[2]/@csk')

fname = str(fullname).partition(",")[2]
lname = str(fullname).partition(",")[0]
home_batters[8] = fname.strip("[],'") + " " + lname.strip("[],'")

# Away
fullname = away_tree.xpath('//table[@id="team_batting"]/tbody/tr[9]/td[2]/@csk')
if fullname == []:
    fullname = away_tree.xpath('//table[@id="team_batting"]/tbody/tr[10]/td[2]/@csk')

fname = str(fullname).partition(",")[2]
lname = str(fullname).partition(",")[0]
away_batters[8] = fname.strip("[],'") + " " + lname.strip("[],'")

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
home_batters = [
    [home_batters[0], home_avg[0]],
    [home_batters[1], home_avg[1]],
    [home_batters[2], home_avg[2]],
    [home_batters[3], home_avg[3]],
    [home_batters[4], home_avg[4]],
    [home_batters[5], home_avg[5]],
    [home_batters[6], home_avg[6]],
    [home_batters[7], home_avg[7]],
    [home_batters[8], home_avg[8]],
]
away_batters = [
    [away_batters[0], away_avg[0]],
    [away_batters[1], away_avg[1]],
    [away_batters[2], away_avg[2]],
    [away_batters[3], away_avg[3]],
    [away_batters[4], away_avg[4]],
    [away_batters[5], away_avg[5]],
    [away_batters[6], away_avg[6]],
    [away_batters[7], away_avg[7]],
    [away_batters[8], away_avg[8]],
]

# Fill in empty stats for box score
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

# Sort array by batting average to determine batting order
home_batters = sorted(home_batters, key=lambda x: x[1], reverse=True)
away_batters = sorted(away_batters, key=lambda x: x[1], reverse=True)

###########################################################
# Scrape top 9 batters and batting averages for specified team/year

home_pitchers = [
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
    [[""], [0]],
]
away_pitchers = [
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
    [[""], [0]],
]

home_relief_pitchers = [[[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]]]
away_relief_pitchers = [[[""], [0]], [[""], [0]], [[""], [0]], [[""], [0]]]

home_closer = ["", 0]
away_closer = ["", 0]

home_pitchers_used = []
away_pitchers_used = []


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
            home_closer[0] = fname.strip("[],'") + " " + lname.strip("[],'")
            era = home_tree.xpath(
                '//table[@id="team_pitching"]/tbody/tr[' + str(x + 1) + "]/td[7]/text()"
            )
            home_closer[1] = float(str(era).strip("[]'"))
            home_pitchers[x][0] = "_EMPTY_"
        else:
            # Not closer
            home_pitchers[x][0] = fname.strip("[],'") + " " + lname.strip("[],'")
            era = home_tree.xpath(
                '//table[@id="team_pitching"]/tbody/tr[' + str(x + 1) + "]/td[7]/text()"
            )
            home_pitchers[x][1] = float(str(era).strip("[]'"))
    else:
        # Blank/header line
        home_pitchers[x][0] = "_EMPTY_"

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
            away_closer[0] = fname.strip("[],'") + " " + lname.strip("[],'")
            era = away_tree.xpath(
                '//table[@id="team_pitching"]/tbody/tr[' + str(x + 1) + "]/td[7]/text()"
            )
            away_closer[1] = float(str(era).strip("[]'"))
            away_pitchers[x][0] = "_EMPTY_"
        else:  # Not closer
            away_pitchers[x][0] = fname.strip("[],'") + " " + lname.strip("[],'")
            era = away_tree.xpath(
                '//table[@id="team_pitching"]/tbody/tr[' + str(x + 1) + "]/td[7]/text()"
            )
            away_pitchers[x][1] = float(str(era).strip("[]'"))
    else:
        # Blank/header line
        away_pitchers[x][0] = "_EMPTY_"

# For some reason, these loops need to be run twice each to remove empty array elements
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

# Pitchers 5 through 9 are relief pitchers
for x in range(5, 9):
    home_relief_pitchers[x - 5] = home_pitchers[x]
    away_relief_pitchers[x - 5] = away_pitchers[x]

# Print sorterd batters for Home
print("\nStarting lineup for the " + str(home_year) + " " + home_team + ":")
wait()
for x in home_batters:
    print(x[0] + " - " + format_batting_average(x[1]))
    wait_short()

# Print sorted batters for Away
print("\nStarting lineup for the " + str(away_year) + " " + away_team + ":")
wait()
for x in away_batters:
    print(x[0] + " - " + format_batting_average(x[1]))
    wait_short()

# Choose a random starting pitcher for each team
pitcher_rand = random.randint(0, 4)
home_starting_pitcher = home_pitchers[pitcher_rand]
current_home_pitcher = home_starting_pitcher

pitcher_rand = random.randint(0, 4)
away_starting_pitcher = away_pitchers[pitcher_rand]
current_away_pitcher = away_starting_pitcher

# Keep track of what starting pitchers were used, for end-of-game box score
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
print(
    "\033[1;93;40m"
    + home_starting_pitcher[0]
    + "\033[0m is now pitching for the "
    + home_team
    + "."
)
wait()
print(str(home_year) + " ERA: " + str(format_era(home_starting_pitcher[1])))
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

    pitch_result = calculate_pitch_outcome(atbat_pitch_count, False)

    if pitch_result == "Ball":
        if balls < 3:
            balls += 1
            pitching_animation()
            print("Ball. (" + str(balls) + " - " + str(strikes) + ")")

        elif balls == 3:  # Walk
            pitch_result = "Walk"
            pitching_animation()
            print("\033[1;30;102mWALK!\033[0m")
            if first == False and second == False and third == False:
                first = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[1] = current_home_batter
            elif first == True and second == False and third == False:
                second = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_home_batter
            elif first == False and second == True and third == False:
                first = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[1] = current_home_batter
            elif first == False and second == False and third == True:
                first = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[1] = current_home_batter
            elif first == True and second == True and third == False:
                third = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = runners_on_base[2]
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = runners_on_base[2]
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_home_batter
            elif first == False and second == True and third == True:
                first = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[1] = current_home_batter
            elif first == True and second == True and third == True:
                run(1)
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = runners_on_base[2]
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = runners_on_base[2]
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_home_batter
            elif first == True and second == False and third == True:
                second = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_home_batter
            if half_inning % 2 != 0:  # if top of inning
                away_batters[current_away_batter][7] += 1  # At-bat count for box score
                home_pitchers_used[-1][7] += 1
            elif half_inning % 2 == 0:  # if bottom of inning
                home_batters[current_home_batter][7] += 1  # At-bat count for box score
                away_pitchers_used[-1][7] += 1
            resetcount()

    elif pitch_result == "Strike":
        if strikes < 2:  # Strike
            strikes += 1
            pitching_animation()
            print("Strike. (" + str(balls) + " - " + str(strikes) + ")")

        elif strikes == 2 and half_inning % 2 != 0:  # Strikeout - away
            pitching_animation()
            print("\033[1;97;101mSTRIKEOUT!\033[0m")
            pitch_result = "Strikeout"
            away_batters[current_away_batter][8] += 1  # At-bat count for box score
            home_pitchers_used[-1][8] += 1
            out(1)

        elif strikes == 2 and half_inning % 2 == 0:  # Strikeout - home
            pitching_animation()
            print("\033[1;97;101mSTRIKEOUT!\033[0m")
            # print ("STRIKEOUT!")
            pitch_result = "Strikeout"
            home_batters[current_home_batter][8] += 1  # At-bat count for box score
            away_pitchers_used[-1][8] += 1
            out(1)

    elif pitch_result == "Foul":
        if strikes < 2:  # Foul
            strikes += 1
            pitching_animation()
            print("Foul. (" + str(balls) + " - " + str(strikes) + ")")

        elif strikes == 2:  # Foul (with 2 strikes)
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

            if first == False and second == False and third == False:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mFLY OUT!\033[0m")
                out(1)
            elif first == True and second == False and third == False:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mFLY OUT!\033[0m")
                out(1)
            elif first == False and second == True and third == False and outs < 2:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;30;103mFLY OUT! RUNNER ADVANCED.\033[0m")
                second = False
                third = True
                out(1)
                runners_on_base[3] = runners_on_base[2]
                runners_on_base[2] = -1
            elif first == False and second == True and third == False and outs == 2:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mFLY OUT!\033[0m")
                out(1)
            elif first == False and second == False and third == True and outs < 2:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;30;102mSACRIFICE FLY!\033[0m")
                third = False
                out(1)
                run(1)
                runners_on_base[3] = -1
            elif first == False and second == False and third == True and outs == 2:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mFLY OUT!\033[0m")
                out(1)
            elif first == True and second == True and third == False and outs < 2:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;30;103mFLY OUT! RUNNER ADVANCED.\033[0m")
                second = False
                third = True
                out(1)
                runners_on_base[3] = runners_on_base[2]
                runners_on_base[2] = -1
            elif first == True and second == True and third == False and outs == 2:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mFLY OUT!\033[0m")
                out(1)
            elif first == False and second == True and third == True and outs < 2:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;30;102mSACRIFICE FLY!\033[0m")
                third = False
                out(1)
                run(1)
                runners_on_base[3] = -1
            elif first == False and second == True and third == True and outs == 2:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mFLY OUT!\033[0m")
                out(1)
            elif first == True and second == False and third == True and outs < 2:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;30;102mSACRIFICE FLY!\033[0m")
                third = False
                out(1)
                run(1)
                runners_on_base[3] = -1
            elif first == True and second == False and third == True and outs == 2:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mFLY OUT!\033[0m")
                out(1)
            elif first == True and second == True and third == True and outs < 2:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;30;102mSACRIFICE FLY!\033[0m")
                third = False
                out(1)
                run(1)
                runners_on_base[3] = -1
            elif first == True and second == True and third == True and outs < 2:
                pitching_animation()
                ball_in_play_animation()
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

            if first == False and second == False and third == False:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mGROUND OUT!\033[0m")
                out(1)
            elif first == True and second == False and third == False and outs < 2:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mDOUBLE PLAY!\033[0m")
                out(2)
                first = False
                runners_on_base[1] = -1
            elif first == True and second == False and third == False and outs == 2:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mGROUND OUT!\033[0m")
                out(1)
            elif first == False and second == True and third == False:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mGROUND OUT!\033[0m")
                out(1)
            elif first == False and second == False and third == True:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mGROUND OUT!\033[0m")
                out(1)
            elif first == True and second == True and third == False and outs == 0:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mTRIPLE PLAY\033[0m")
                out(3)
            elif first == True and second == True and third == False and outs == 1:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mDOUBLE PLAY!\033[0m")
                out(2)
            elif first == True and second == True and third == False and outs == 2:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mGROUND OUT!\033[0m")
                out(1)
            elif first == False and second == True and third == True:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mGROUND OUT!\033[0m")
                out(1)
            elif first == True and second == True and third == True and outs == 0:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mTRIPLE PLAY!\033[0m")
                out(3)
            elif first == True and second == True and third == True and outs == 1:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mDOUBLE PLAY!\033[0m")
                out(2)
            elif first == True and second == True and third == True and outs == 2:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mGROUND OUT!\033[0m")
                out(1)
            elif first == True and second == False and third == True and outs < 2:
                pitching_animation()
                ball_in_play_animation()
                print("\033[1;97;101mDOUBLE PLAY!\033[0m")
                out(2)
                first = False
                runners_on_base[1] = -1
            elif first == True and second == False and third == True and outs == 2:
                pitching_animation()
                ball_in_play_animation()
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
            if first == False and second == False and third == False:
                first = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[1] = current_home_batter
            elif first == True and second == False and third == False:
                second = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_home_batter
            elif first == False and second == True and third == False:
                first = True
                second = False
                third = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = runners_on_base[2]
                    runners_on_base[2] = -1
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = runners_on_base[2]
                    runners_on_base[2] = -1
                    runners_on_base[1] = current_home_batter
            elif first == False and second == False and third == True:
                first = True
                third = False
                run(1)
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = -1
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = -1
                    runners_on_base[1] = current_home_batter
            elif first == True and second == True and third == False:
                third = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = runners_on_base[2]
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = runners_on_base[2]
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_home_batter
            elif first == False and second == True and third == True:
                first = True
                second = False
                run(1)
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = runners_on_base[2]
                    runners_on_base[2] = -1
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = runners_on_base[2]
                    runners_on_base[2] = -1
                    runners_on_base[1] = current_home_batter
            elif first == True and second == True and third == True:
                run(1)
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = runners_on_base[2]
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = runners_on_base[2]
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_home_batter
            elif first == True and second == False and third == True:
                second = True
                third = False
                run(1)
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = -1
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = -1
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_home_batter

            if half_inning % 2 != 0:  # if top of inning
                away_batters[current_away_batter][4] += 1  # Hit count for box score
                home_pitchers_used[-1][4] += 1
            elif half_inning % 2 == 0:  # if bottom of inning
                home_batters[current_home_batter][4] += 1  # Hit count for box score
                away_pitchers_used[-1][4] += 1

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
            if first == False and second == False and third == False:
                second = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[2] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[2] = current_home_batter
            elif first == True and second == False and third == False:
                first = False
                second = True
                third = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = runners_on_base[1]
                    runners_on_base[2] = current_away_batter
                    runners_on_base[1] = -1
                elif half_inning % 2 == 0:  # if bottom of inning
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
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = -1
                    runners_on_base[2] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = -1
                    runners_on_base[2] = current_home_batter
            elif first == True and second == True and third == False:
                first = False
                run(2)
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[2] = current_away_batter
                    runners_on_base[1] = -1
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[2] = current_home_batter
                    runners_on_base[1] = -1
            elif first == False and second == True and third == True:
                third = False
                run(2)
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[2] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[2] = current_home_batter
            elif first == True and second == True and third == True:
                first = False
                third = False
                run(3)
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = runners_on_base[1]
                    runners_on_base[2] = current_away_batter
                    runners_on_base[1] = -1
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = runners_on_base[1]
                    runners_on_base[2] = current_home_batter
                    runners_on_base[1] = -1
            elif first == True and second == False and third == True:
                second = True
                first = False
                third = False
                run(2)
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = runners_on_base[1]
                    runners_on_base[2] = current_away_batter
                    runners_on_base[1] = -1
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = runners_on_base[1]
                    runners_on_base[2] = current_home_batter
                    runners_on_base[1] = -1
            if half_inning % 2 != 0:  # if top of inning
                away_batters[current_away_batter][4] += 1  # Hit count for box score
                home_pitchers_used[-1][4] += 1
            elif half_inning % 2 == 0:  # if bottom of inning
                home_batters[current_home_batter][4] += 1  # Hit count for box score
                away_pitchers_used[-1][4] += 1
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
            if half_inning % 2 != 0:  # if top of inning
                away_batters[current_away_batter][4] += 1  # Hit count for box score
                away_batters[current_away_batter][6] += 1  # HR count for box score
                home_pitchers_used[-1][4] += 1
                home_pitchers_used[-1][6] += 1
            elif half_inning % 2 == 0:  # if bottom of inning
                home_batters[current_home_batter][4] += 1  # Hit count for box score
                home_batters[current_home_batter][6] += 1  # HR count for box score
                away_pitchers_used[-1][4] += 1
                away_pitchers_used[-1][6] += 1

            resetcount()
            pitch_result = "Home run"

            runners_on_base[1] = -1
            runners_on_base[2] = -1
            runners_on_base[3] = -1
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
            if first == False and second == False and third == False:
                first = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[1] = current_home_batter
            elif first == True and second == False and third == False:
                second = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_home_batter
            elif first == False and second == True and third == False:
                first = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[1] = current_home_batter
            elif first == False and second == False and third == True:
                first = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[1] = current_home_batter
            elif first == True and second == True and third == False:
                third = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = runners_on_base[2]
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = runners_on_base[2]
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_home_batter
            elif first == False and second == True and third == True:
                first = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[1] = current_home_batter
            elif first == True and second == True and third == True:
                run(1)
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = runners_on_base[2]
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = runners_on_base[2]
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_home_batter
            elif first == True and second == False and third == True:
                second = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[2] = runners_on_base[1]
                    runners_on_base[1] = current_home_batter
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
            if first == False and second == False and third == False:
                third = True
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = current_away_batter
            elif first == True and second == False and third == False:
                first = False
                third = True
                run(1)
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = current_away_batter
                    runners_on_base[1] = -1
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = current_away_batter
                    runners_on_base[1] = -1
            elif first == False and second == True and third == False:
                third = True
                second = False
                run(1)
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = current_away_batter
                    runners_on_base[2] = -1
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = current_away_batter
                    runners_on_base[2] = -1
            elif first == False and second == False and third == True:
                run(1)
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = current_away_batter
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = current_away_batter
            elif first == True and second == True and third == False:
                third = True
                first = False
                second = False
                run(2)
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = current_away_batter
                    runners_on_base[2] = -1
                    runners_on_base[1] = -1
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = current_away_batter
                    runners_on_base[2] = -1
                    runners_on_base[1] = -1
            elif first == False and second == True and third == True:
                second = False
                run(2)
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = current_away_batter
                    runners_on_base[2] = -1
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = current_away_batter
                    runners_on_base[2] = -1
            elif first == True and second == True and third == True:
                first = False
                second = False
                third = True
                run(3)
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = current_away_batter
                    runners_on_base[2] = -1
                    runners_on_base[1] = -1
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = current_away_batter
                    runners_on_base[2] = -1
                    runners_on_base[1] = -1
            elif first == True and second == False and third == True:
                first = False
                run(2)
                if half_inning % 2 != 0:  # if top of inning
                    runners_on_base[3] = current_away_batter
                    runners_on_base[1] = -1
                elif half_inning % 2 == 0:  # if bottom of inning
                    runners_on_base[3] = current_away_batter
                    runners_on_base[1] = -1
            if half_inning % 2 != 0:  # if top of inning
                away_batters[current_away_batter][4] += 1  # Hit count for box score
                home_pitchers_used[-1][4] += 1
            elif half_inning % 2 == 0:  # if bottom of inning
                home_batters[current_home_batter][4] += 1  # Hit count for box score
                away_pitchers_used[-1][4] += 1
            resetcount()
            pitch_result = "Triple"

    atbat_pitch_count += 1
    redo_pitch_loops = 0

    if half_inning % 2 == 0:
        away_pitcher_pitch_count += 1
    else:
        home_pitcher_pitch_count += 1

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
        if half_inning % 2 == 0 and current_home_batter < 8:
            current_home_batter += 1
        elif half_inning % 2 == 0 and current_home_batter == 8:
            current_home_batter = 0
        elif half_inning % 2 != 0 and current_away_batter < 8:
            current_away_batter += 1
        elif half_inning % 2 != 0 and current_away_batter == 8:
            current_away_batter = 0

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
    print("Game has ended. \033[1;93;40m" + home_team + " win!\033[0m")
elif home_score < away_score:
    print("Game has ended. \033[1;93;40m" + away_team + " win!\033[0m")

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
print(away_abbr + " ", end="")
for x in away_score_by_inning:
    wait_short()
    print(str(x) + " ", end="")
wait_short()
print("- \033[1;93;40m" + str(away_score) + "\033[0m")

wait_short()
print(home_abbr + " ", end="")
for x in home_score_by_inning:
    wait_short()
    print(str(x) + " ", end="")

if len(home_score_by_inning) < len(away_score_by_inning):
    print("  ", end="")
wait_short()
print("- \033[1;93;40m" + str(home_score) + "\033[0m\n")

wait_short()
print("Batting")
wait_short()
print("")
wait_short()

###########################################################
# Box score - Away batting
print(away_team.upper(), end="")
for y in range(25 - len(away_team)):
    print(" ", end="")
print("AB   R   H  RBI HR  BB  SO")

for x in away_batters:
    # Player name
    wait_short()
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
    away_total[0] = away_total[0] + away_batters[x][2]  # AB
    away_total[1] = away_total[1] + away_batters[x][3]  # R
    away_total[2] = away_total[2] + away_batters[x][4]  # H
    away_total[3] = away_total[3] + away_batters[x][5]  # RBI
    away_total[4] = away_total[4] + away_batters[x][6]  # HR
    away_total[5] = away_total[5] + away_batters[x][7]  # BB
    away_total[6] = away_total[6] + away_batters[x][8]  # SO

wait_short()
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
print(home_team.upper(), end="")
for y in range(25 - len(home_team)):
    print(" ", end="")
print("AB   R   H  RBI HR  BB  SO")

for x in home_batters:
    # Player name
    wait_short()
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
    home_total[0] = home_total[0] + home_batters[x][2]  # AB
    home_total[1] = home_total[1] + home_batters[x][3]  # R
    home_total[2] = home_total[2] + home_batters[x][4]  # H
    home_total[3] = home_total[3] + home_batters[x][5]  # RBI
    home_total[4] = home_total[4] + home_batters[x][6]  # HR
    home_total[5] = home_total[5] + home_batters[x][7]  # BB
    home_total[6] = home_total[6] + home_batters[x][8]  # SO

wait_short()
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
wait_short()
print("Pitching")
wait_short()
print("")
wait_short

###########################################################
# Box score - Away pitching
print(away_team.upper(), end="")
for y in range(25 - len(away_team)):
    print(" ", end="")
print("IP   R   H  ER  HR  BB  SO")

wait_short()
for x in away_pitchers_used:
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

    wait_short()

# Add up away pitching totals
away_total = [0, 0, 0, 0, 0, 0, 0]
for x in range(0, len(away_pitchers_used)):
    away_total[0] = away_total[0] + away_pitchers_used[x][2]  # IP
    away_total[1] = away_total[1] + away_pitchers_used[x][3]  # R
    away_total[2] = away_total[2] + away_pitchers_used[x][4]  # H
    away_total[3] = away_total[3] + away_pitchers_used[x][5]  # ER
    away_total[4] = away_total[4] + away_pitchers_used[x][6]  # HR
    away_total[5] = away_total[5] + away_pitchers_used[x][7]  # BB
    away_total[6] = away_total[6] + away_pitchers_used[x][8]  # SO

wait_short()
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
wait_short()


###########################################################
# Box score - Home pitching
print(home_team.upper(), end="")
for y in range(25 - len(home_team)):
    print(" ", end="")
print("IP   R   H  ER  HR  BB  SO")

wait_short()
for x in home_pitchers_used:
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

    wait_short()

# Add up home pitching totals
home_total = [0, 0, 0, 0, 0, 0, 0]
for x in range(0, len(home_pitchers_used)):
    home_total[0] = home_total[0] + home_pitchers_used[x][2]  # IP
    home_total[1] = home_total[1] + home_pitchers_used[x][3]  # R
    home_total[2] = home_total[2] + home_pitchers_used[x][4]  # H
    home_total[3] = home_total[3] + home_pitchers_used[x][5]  # ER
    home_total[4] = home_total[4] + home_pitchers_used[x][6]  # HR
    home_total[5] = home_total[5] + home_pitchers_used[x][7]  # BB
    home_total[6] = home_total[6] + home_pitchers_used[x][8]  # SO

wait_short()
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
wait_short()

print("")
wait_short()
wait_short()
print("")

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
    file1.write(away_abbr + " ")
    for x in away_score_by_inning:
        file1.write(str(x) + " ")
    file1.write("- " + str(away_score) + "\n")

    file1.write(home_abbr + " ")
    for x in home_score_by_inning:
        file1.write(str(x) + " ")
    if len(home_score_by_inning) < len(away_score_by_inning):
        file1.write("  ")
    file1.write("- " + str(home_score) + "\n\n")

    file1.write("Batting\n\n")

    ###########################################################
    # Box score - Away batting
    file1.write(away_team.upper())
    for y in range(25 - len(away_team)):
        file1.write(" ")
    file1.write("AB   R   H  RBI HR  BB  SO\n")

    for x in away_batters:
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
        away_total[0] = away_total[0] + away_batters[x][2]  # AB
        away_total[1] = away_total[1] + away_batters[x][3]  # R
        away_total[2] = away_total[2] + away_batters[x][4]  # H
        away_total[3] = away_total[3] + away_batters[x][5]  # RBI
        away_total[4] = away_total[4] + away_batters[x][6]  # HR
        away_total[5] = away_total[5] + away_batters[x][7]  # BB
        away_total[6] = away_total[6] + away_batters[x][8]  # SO

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
    file1.write(home_team.upper())
    for y in range(25 - len(home_team)):
        file1.write(" ")
    file1.write("AB   R   H  RBI HR  BB  SO\n")

    for x in home_batters:
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
        home_total[0] = home_total[0] + home_batters[x][2]  # AB
        home_total[1] = home_total[1] + home_batters[x][3]  # R
        home_total[2] = home_total[2] + home_batters[x][4]  # H
        home_total[3] = home_total[3] + home_batters[x][5]  # RBI
        home_total[4] = home_total[4] + home_batters[x][6]  # HR
        home_total[5] = home_total[5] + home_batters[x][7]  # BB
        home_total[6] = home_total[6] + home_batters[x][8]  # SO

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
    file1.write(away_team.upper())
    for y in range(25 - len(away_team)):
        file1.write(" ")
    file1.write("IP   R   H  ER  HR  BB  SO\n")

    for x in away_pitchers_used:
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
    for x in range(0, len(away_pitchers_used)):
        away_total[0] = away_total[0] + away_pitchers_used[x][2]  # IP
        away_total[1] = away_total[1] + away_pitchers_used[x][3]  # R
        away_total[2] = away_total[2] + away_pitchers_used[x][4]  # H
        away_total[3] = away_total[3] + away_pitchers_used[x][5]  # ER
        away_total[4] = away_total[4] + away_pitchers_used[x][6]  # HR
        away_total[5] = away_total[5] + away_pitchers_used[x][7]  # BB
        away_total[6] = away_total[6] + away_pitchers_used[x][8]  # SO

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
    file1.write(home_team.upper())
    for y in range(25 - len(home_team)):
        file1.write(" ")
    file1.write("IP   R   H  ER  HR  BB  SO\n")

    for x in home_pitchers_used:
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
    for x in range(0, len(home_pitchers_used)):
        home_total[0] = home_total[0] + home_pitchers_used[x][2]  # IP
        home_total[1] = home_total[1] + home_pitchers_used[x][3]  # R
        home_total[2] = home_total[2] + home_pitchers_used[x][4]  # H
        home_total[3] = home_total[3] + home_pitchers_used[x][5]  # ER
        home_total[4] = home_total[4] + home_pitchers_used[x][6]  # HR
        home_total[5] = home_total[5] + home_pitchers_used[x][7]  # BB
        home_total[6] = home_total[6] + home_pitchers_used[x][8]  # SO

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
