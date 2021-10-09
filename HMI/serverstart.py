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
		return "True"
	else:
		return "False"

if __name__ == '__main__':
	# run!
	app.run("0.0.0.0", "5010", debug=True)