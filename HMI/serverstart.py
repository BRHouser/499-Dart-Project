#!flask/bin/python
from flask import Flask, render_template, request, redirect, Response

app = Flask(__name__)
@app.route('/')
def createScorekeeper():
	# serve index template
	return render_template('scorekeeper.html')

@app.route('/scoreboard')
def createScoreboard():
	return render_template('scoreboard.html')

@app.route('/oooo', methods = ['POST'])
def worker():
	# read json + reply
	# data = request.get_json()
	result = "THIS CHANGES THE TITLE"
	return result

@app.route('/banana', methods = ['POST'])
def something():
	return "SOMETHING"

if __name__ == '__main__':
	# run!
	app.run("0.0.0.0", "5010", debug=True)