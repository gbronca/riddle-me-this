import os, json, random
from flask import Flask, render_template, session, redirect, request, url_for, flash

app = Flask(__name__)

''' Loads the riddles.json file into a variable '''
def load_riddles():
    with open('data/riddles.json','r') as f:
        riddles = json.load(f)
    return riddles

# Load the riddles
riddles = load_riddles()

# Starts the game and delete existing session
@app.route('/')
def index():
    if session:
        [session.pop(key) for key in list(session.keys())]
    return render_template('index.html')

# Logout the current user and delete existing session
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

''' Create new session and start a new game when a username is passed by index function '''
@app.route('/new_game', methods = ['GET', 'POST'])
def new_game():
    session['username'] = request.form['username']
    session['score'] = 0
    session['attempts'] = 0
    session['index'] = 0 # Pointer to the current question number
    
    # Shuffles the riddles, ensuring that 2 players playing at the same time
    # would have a different order for the riddles
    random.shuffle(riddles)

    return redirect(url_for('riddle'))

@app.route('/scoreboard')
def scoreboard():
    with open('data/scores.json', 'r') as f:
        scores = json.load(f)
    
    return render_template('scoreboard.html', scoreboard=scores)


@app.route('/riddle', methods = ['GET', 'POST'])
def riddle():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST' and session['index'] < len(riddles):
        if request.form['answer'].lower() == riddles[session['index']]['answer'].lower():
            session['score'] += 1
            session['index'] += 1
            flash('Correct answer, %s, %s' % (session['score'], session['username']), 'success')
        elif session['attempts'] < 2:
            session['attempts'] += 1
            print(session['attempts'])
            if session['attempts'] == 2:
                flash('"%s" is the wrong answer, %s, this is your last chance' % (request.form['answer'], session['username']), 'warning')
            else:
                flash('"%s" is not the correct answer %s. You have %s more attempts' % (request.form['answer'], session['username'], 3 - int(session['attempts'])), 'warning')
        else:
            session['attempts'] = 0
            session['index'] += 1
            flash('Wrong answer! Better luck with the next riddle', 'error')
            

    if session['index'] >= 3:
        flash('Congratulations, you finished the game %s. Your score is %s' %(session['username'], session['score']), 'victory')


    return render_template('riddle.html', question=riddles[session['index']]['question'])

if __name__ == '__main__':
    app.secret_key = os.getenv('SECRET', 'mysecretkey123')
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', '5000')), debug=True)