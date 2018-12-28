import os, json, random
from flask import Flask, render_template, session, redirect, request, url_for, flash

app = Flask(__name__)

''' Loads the riddles.json file into a variable '''
def load_riddles():
    with open('data/riddles.json','r') as f:
        riddles = json.load(f)
    return riddles


@app.route('/')
def index():
    return render_template('index.html')


''' Create new session and start a new game when a username is passed by index function '''
@app.route('/new_game', methods = ['GET', 'POST'])
def new_game():
    session['username'] = request.form['username']
    session['score'] = 0
    session['attempts'] = 0
    return redirect(url_for('riddle'))


@app.route('/riddle', methods = ['GET', 'POST'])
def riddle():
    ''' Loads the riddles from file and shuffles the results '''
    riddles = load_riddles()
    random.shuffle(riddles)

    for riddle in riddles:
        print (riddle['question'])
        print (riddle['answer'])

    return render_template('riddle.html')

if __name__ == '__main__':
    app.secret_key = os.getenv('SECRET', 'mysecretkey123')
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', '5000')), debug=True)