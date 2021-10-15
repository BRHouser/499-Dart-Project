import sys
sys.path.append('Database')
import os
from flask import Flask, render_template, request, redirect, Response
import database
import json

project_directory = os.getcwd()
project_directory = project_directory[0:project_directory.find("Project") + 7]    
database_address = os.getcwd() + "/Database/Dart_Scorer_Database.db"
database_connection = database.create_connection(database_address)


app = Flask(__name__)
@app.route('/')
def createMatchSetup():
	# serve index template
	return render_template('startmatch.html')

@app.route('/scorekeeper')
def createScorekeeper():
	return render_template('scorekeeper.html')

@app.route('/scoreboard')
def createScoreboard():
	return render_template('scoreboard.html')

@app.route('/baseCaseSendInformation', methods = ['POST'])
def worker():
	# read json + reply, Information is in form of type dictionary
	data = json.loads(request.get_data())
	return data["information"]


# This function connects the HMI Button 'Add Player' To the database and allows a new table to be made
# Pertaining to the player just added
@app.route('/addPlayer', methods = ['POST'])
def addPlayer():
	data = json.loads(request.get_data())
	columns = ["id", "First_Name", "Last_Name", "Total_Number_of_Throws", "Total_Number_of_BullsEyes"]
	if(database.add_table(database_connection, data["firstname"] + "_" + data["lastname"] + "_" + "Statistics", columns)):
		row = [data["firstname"], data["lastname"], str(data["totalthrows"]), str(data["totalbullseyes"])]
		name = data["firstname"] + "_" + data["lastname"] + "_" + "Statistics"
		database.add_information(database_connection, name, [row])
		row = [data["firstname"], data["lastname"]]
		database.add_information(database_connection, "List_of_Players", [row])
		return "True"
	else:
		return "False"

@app.route("/getPlayers", methods = ['POST'])
def getPlayers():
	information = database.get_information(database_connection, "List_of_Players")
	send = {}
	for x in range(1, len(information)):
		send["Player" + str(x)] = information[x][1] + " " + information[x][2]
	send = json.dumps(send)
	return send


@app.route("/deletePlayer", methods = ['POST'])
def deletePlayer():
	data = json.loads(request.get_data())
	database.delete_table(database_connection, data["firstname"] + "_" + data["lastname"] + "_Statistics")
	location = database.get_information(database_connection, "List_of_Players")
	check = False
	x = -1
	while check == False:
		x = x + 1
		if str(location[x][1]).strip() == str(data["firstname"]).strip():
			if str(location[x][2]).strip() == str(data["lastname"]).strip():
				check = True

	database.delete_row(database_connection, "List_of_Players", location[x])
	return ""

@app.route("/getPlayerInformation", methods=["POST"])
def getPlayerInformation():
	data = json.loads(request.get_data())
	information = database.get_information(database_connection, data["firstname"] + "_" + data["lastname"] + "_Statistics")
	send = {}

	x = 0
	for y in range(len(information[x])):
		send[information[x][y]] = information[x + 1][y]
	send = json.dumps(send)
	return send

if __name__ == '__main__':
	# run!
	app.run("0.0.0.0", "5010", debug=True)