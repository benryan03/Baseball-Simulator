from lxml import html
import requests

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
		
def GetUserInputs():

	home_team_error = True
	while home_team_error == True:
		team = input("Enter the name of the home team: ")
		if parse_input(team) == "invalid":
			print("Invalid team.")
			continue
		else:

			homeTeam = parse_input(team).split(",")[0]
			homeAbbr = parse_input(team).split(",")[1]
			home_team_error = False

	home_year_error = True
	while home_year_error == True:
		homeYear = input("Enter year: ")
		home_page = requests.get( "https://www.baseball-reference.com/teams/"
			+ homeAbbr + "/" + homeYear + ".shtml")
		if str(home_page) != "<Response [200]>":
			print("Invalid year.")
			continue
		else:
			home_year_error = False

	away_team_error = True
	while away_team_error == True:
		awayTeam = input("Enter the name of the away team: ")
		if parse_input(awayTeam) == "invalid":
			print("Invalid team.")
			continue
		else:
			awayTeam = parse_input(awayTeam).split(",")[0]
			awayAbbr = parse_input(awayTeam).split(",")[1]
			away_team_error = False

	away_year_error = True
	while away_year_error == True:
		awayYear = input("Enter year: ")
		away_page = requests.get(
			"https://www.baseball-reference.com/teams/" + awayAbbr 
			+ "/" + awayYear + ".shtml"
		)
		if str(away_page) != "<Response [200]>":
			print("Invalid year.")
			continue
		else:
			away_year_error = False

	inputsArray = [homeTeam, awayTeam, homeAbbr, awayAbbr, homeYear, awayYear]
	return inputsArray

	