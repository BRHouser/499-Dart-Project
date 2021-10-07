#!flask/bin/python
from flask import Flask, render_template, request, redirect, Response
import json



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



@app.route('/banana', methods = ['POST'])
def something():
	return "SOMETHING"

if __name__ == '__main__':
	# run!
	app.run("0.0.0.0", "5010", debug=True)