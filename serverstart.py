import sys
sys.path.append('Database')
import os
from flask import Flask, render_template, request, redirect, Response
import database
import json
import Components.UpdateScoreboard as UpdateScoreboard
import Components.ReceiveData as ReceiveData
import Components.GameSetup as GameSetup
import Components.LeagueStats as LeagueStats

# Directory of the Database
project_directory = os.getcwd()
project_directory = project_directory[0:project_directory.find("Project") + 7]    
database_address = os.getcwd() + "/Database/Dart_Scorer_Database.db"
database_connection = database.create_connection(database_address)

app = Flask(__name__)

# Renders Home Page
@app.route('/')
def createMatchSetup():
	# serve index template
	return render_template('startmatch.html')


# Renders Scorekeeper Page
@app.route('/scorekeeper')
def createScorekeeper():
	return render_template('scorekeeper.html')


# Renders Scoreboard Page
@app.route('/scoreboard')
def createScoreboard():
	return render_template('scoreboard.html')


# INPUT: Dictionary with keys: 'firstname', 'lastname', totalthrows', 'totalbullseyes'
# OUTPUT: True if Player was added to the database, False if Player was not added to the database
# The purpose of this function is to add a player to the database by recieving data from the 
# HMI and call add_table and add_information with the information from the dictionary
@app.route('/addPlayer', methods = ['POST'])
def addPlayer():
	# Loads the data from the HMI
	data = json.loads(request.get_data())
	LS = LeagueStats.LeagueStats()
	LS.delete_player(str(data['firstname'] + " " + str(data['lastname'])))
	LS.update_stat(str(data['firstname'] + " " + str(data['lastname'])), "Last Win", data['LastWin'])
	LS.update_stat(str(data['firstname'] + " " + str(data['lastname'])), "Average League Score", int(data['Average_League_Score']))
	LS.update_stat(str(data['firstname'] + " " + str(data['lastname'])), "Lifetime 180s", int(data['Lifetime_180s']))
	LS.update_stat(str(data['firstname'] + " " + str(data['lastname'])), "Wins", int(data['Number_of_wins']))
	LS.update_ranks()

	# Set terms of what the header should be for a player
	columns = ["id", "First_Name", "Last_Name", "Last_Win", "Average_League_Score", "Lifetime_180s", "Number_of_Wins"]
	# If a table was created for the given person, then add the person to the List_of_Players Table and return True
	# Else return False which means the player is already in the database
	if(database.add_table(database_connection, data["firstname"] + "_" + data["lastname"] + "_" + "Statistics", columns)):
		row = [data["firstname"], data["lastname"], str(data["LastWin"]), str(data['Average_League_Score']), str(data['Lifetime_180s']), str(data['Number_of_wins'])]
		name = data["firstname"] + "_" + data["lastname"] + "_" + "Statistics"
		database.add_information(database_connection, name, [row])
		row = [data["firstname"], data["lastname"]]
		database.add_information(database_connection, "List_of_Players", [row])
		return "True"
	else:
		return "False"


# OUTPUT: A dictionary with all the player names in it 
# The purpose of this function is to send a dictionary of player names to the HMI by calling get_information 
# on the List_of_Players table 
@app.route("/getPlayers", methods = ['POST'])
def getPlayers():
	# Gets list of players from database
	information = database.get_information(database_connection, "List_of_Players")

	# Converts Information into dictionary format
	send = {}
	for x in range(1, len(information)):
		send["Player" + str(x)] = information[x][1] + " " + information[x][2]

	# Converts information into JSON and sends to HMI
	send = json.dumps(send)
	return send


# INPUT: Dictionary with keys: 'firstname', 'lastname'
# The purpose of this function is to delete a player from the database by recieving data from the 
# HMI and call delete_table and delete_row with the information from the dictionary
@app.route("/deletePlayer", methods = ['POST'])
def deletePlayer():
	# Get information
	data = json.loads(request.get_data())

	# Deletes the Players Statistics
	database.delete_table(database_connection, data["firstname"] + "_" + data["lastname"] + "_Statistics")
	
	# Find the Player in List_of_Players
	location = database.get_information(database_connection, "List_of_Players")
	check = False
	x = -1
	while check == False:
		x = x + 1
		if str(location[x][1]).strip() == str(data["firstname"]).strip():
			if str(location[x][2]).strip() == str(data["lastname"]).strip():
				check = True

	# Deletes the Player in List_of_Players
	database.delete_row(database_connection, "List_of_Players", location[x])
	return ""


# INPUT: Dictionary with keys: 'firstname', 'lastname'
# OUTPUT: Dictionary with keys as column headers and values as the information per column
# The purpose of this function is to return the Player's Statistics Table by recieving
# data from the HMI and call get_information with the information from the dictionary
@app.route("/getPlayerStatistics", methods=["POST"])
def getPlayerStatistics():
	# Get Information from HMI
	data = json.loads(request.get_data())

	# Gets Information from database
	information = database.get_information(database_connection, data["firstname"] + "_" + data["lastname"] + "_Statistics")
	send = {}

	# Puts information into dictionary form
	x = 0
	for y in range(len(information[x])):
		send[information[x][y]] = information[x + 1][y]
	print(send)
	# Convert data to JSON and send it to HMI
	send = json.dumps(send)
	return send

# Receive Data
# INPUT: data from scorekeeper to be processed by ReceiveData component
@app.route("/receiveData", methods=["POST"])
def receiveData():
	data = json.loads(request.get_data())
	receiveData = ReceiveData.ReceiveData(data)
	return ""

# Update Scoreboard
# OUTPUT: current game state json object for scoreboard
@app.route("/updateScoreboard", methods=["POST"])
def updateScoreboard():
	#print(request.get_data())
	data = json.loads(request.get_data())
	first_read = data["first_read"]
	#todo: send first_read with js
	updater = UpdateScoreboard.UpdateScoreboard(first_read)
	if first_read: first_read = False
	return updater.get_current_game_state()

# Adds Match to Current Match table
@app.route('/addMatch', methods = ['POST'])
def addMatch():
	# Loads the data from the HMI
	data = json.loads(request.get_data())
	#print(data)
	game_setup = GameSetup.GameSetup(data)
	#Adds the match created to current_match
	row = [data["Player1Name"], data["Player2Name"], data["Score"], data["MatchType"], str(data["SetNumber"]) , str(data["NumberOfLegs"]), data["MatchOfficial"], data["NameofMatch"], data["Location"], data["DateOfMatch"]]
	database.add_information(database_connection, "List_Matches", [row])
	
	# Set terms of what the header should be for the legs table
	columns = ["id", "_Set_", "_Leg_", "Throw_1", "Throw_2",  "Throw_3", "Score"]

	name1 = data['NameofMatch'].replace(' ', "_") + "_" + data["Player1Name"].replace(' ', '_') + "_" + "Record"
	name2 = data['NameofMatch'].replace(' ', "_") + "_" + data["Player2Name"].replace(' ', '_') + "_" + "Record"
	if database.add_table(database_connection, name1, columns) and database.add_table(database_connection, name2, columns):
		row = [1, 1, 'START', 'START', 'START', data['Score']]
		database.add_information(database_connection, name1, [row])
		row = [1, 1, 'START', 'START', 'START', data['Score']]
		database.add_information(database_connection, name2, [row])
		return "True"
	else:
		return "False"	


# OUTPUT: A dictionary with all the Matches in it 
# The purpose of this function is to send a dictionary of Matchs to the HMI by calling get_information 
# on the List_Matches table 
@app.route("/getMatches", methods = ['POST'])
def getMatches():
	# Gets list of matches from database
	information = database.get_information(database_connection, "List_Matches")

	# Converts Information into dictionary format
	send = {}
	for x in range(1, len(information)):
		send["Match" + str(x)] = information[x][8]
	# Converts information into JSON and sends to HMI
	send = json.dumps(send)
	return send


# OUTPUT: A dictionary with all the Matches in it 
# The purpose of this function is to send a dictionary of Matchs to the HMI by calling get_information 
# on the List_Matches table 
@app.route("/getPlayersMatch", methods = ['POST'])
def getPlayersMatches():
	# Gets list of matches from database
	information = database.get_information(database_connection, "List_Matches")
	data = json.loads(request.get_data())
	# Converts Information into dictionary format
	send = {}
	for x in range(1, len(information)):
		if(data["game"]["MatchName"] == information[x][8]):
			send["Player" + str(x)] = information[x][1]
			send["Player" + str(x)] = information[x][2]
	# Converts information into JSON and sends to HMI
	send = json.dumps(send)
	return send


# Main Start Server
if __name__ == '__main__':
	# run!
	app.run("0.0.0.0", "5010", debug=True)