import os, json, random
from flask import Flask, render_template, session, redirect, request, url_for, flash

app = Flask(__name__)

''' Loads the riddles.json file into a variable '''
def load_riddles():
    with open('data/riddles.json','r') as f:
        riddles = json.load(f)
    return riddles

''' Loads the riddles and shuffle the questions '''
riddles = load_riddles()

@app.route('/')
def index():
    return render_template('index.html')


''' Create new session and start a new game when a username is passed by index function '''
@app.route('/new_game', methods = ['GET', 'POST'])
def new_game():
    session['username'] = request.form['username']
    session['score'] = 0
    session['attempts'] = 0
    session['index'] = 0 # Pointer to the current question number
    random.shuffle(riddles)
    return redirect(url_for('riddle'))


@app.route('/riddle', methods = ['GET', 'POST'])
def riddle():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST' and session['index'] < len(riddles):
       if request.form['answer'].lower() == riddles[session['index']]['answer'].lower():
           session['score'] += 1
           session['index'] += 1
           flash('Correct answer, %s, %s' % (session['score'], session['username']), 'warning')
           
           print(session['score'])
           print(request.form['answer'])
           print(session['username'])
           print(session['score'])



   # for riddle in riddles:
   #     print (riddle['question'])
    #    print (riddle['answer'])

    return render_template('riddle.html', question=riddles[session['index']]['question'])

if __name__ == '__main__':
    app.secret_key = os.getenv('SECRET', 'mysecretkey123')
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', '5000')), debug=True)