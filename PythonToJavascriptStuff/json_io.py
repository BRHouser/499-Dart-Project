#!flask/bin/python
import sys
from flask import Flask, render_template, request, redirect, Response

app = Flask(__name__)
@app.route('/')
def output():
	# serve index template
	return render_template('index.html')

@app.route('/receiver', methods = ['POST'])
def worker():
	# read json + reply
	data = request.get_json()
	result = "hello JSON"
	return result

	
if __name__ == '__main__':
	# run!
	app.run("0.0.0.0", "5010")