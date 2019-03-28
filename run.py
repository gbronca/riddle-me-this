import os, json, random, operator
from flask import Flask, render_template, session, redirect, request, url_for, flash

app = Flask(__name__)

''' Loads the riddles.json file into a variable '''
def load_riddles():
    with open('data/riddles.json','r') as f:
        riddles_list = json.load(f)

    random.shuffle(riddles_list)
    riddles = riddles_list[:10]
 
    return riddles

''' Load the score files into a list '''
def load_scores():
    with open('data/scores.json', 'r') as f:
        scores = json.load(f)

    return scores

# Load the riddles
riddles = load_riddles()

# Load previous scores
scores = load_scores()

# Starts the game and delete existing session
@app.route('/')
def index():
    if session:
        return render_template('index.html', session=True)
    else:
        return render_template('index.html', session=False)

# Logout the current user and delete existing session
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

''' Create new session and start a new game when a username is passed by index function '''
@app.route('/new_game', methods = ['GET', 'POST'])
def new_game():

    if 'username' not in session:
        session['username'] = request.form['username']
        session['score'] = 0
        session['attempts'] = 0
        session['index'] = 0 # Pointer to the current question number
        session['updated'] = False
    else:
        session['score'] = 0
        session['attempts'] = 0
        session['index'] = 0
        session['updated'] = False
    
    # Shuffles the riddles, ensuring that 2 players playing at the same time
    # would have a different order for the riddles
    random.shuffle(riddles)
    
    return redirect(url_for('riddle'))

@app.route('/scoreboard')
def scoreboard():
    
    score = []
    index = 0

    if 'index' in session:
        if session['index'] < len(riddles):
            if session['score'] > 0:
                score.append({'username' : session['username'], 'score' : session['score']})
            score += scores
        else:
            score = scores
        index = session['index']
    else:
        score += scores

    score.sort(key=operator.itemgetter('score'),reverse=True)
    return render_template('scoreboard.html', scores=score, index=index)

@app.route('/skip', methods = ['GET', 'POST'])
def skip():
    session['index'] += 1
    session['attempts'] = 0
    
    return redirect(url_for('riddle'))


@app.route('/riddle', methods = ['GET', 'POST'])
def riddle():
    if 'username' not in session:
        return redirect(url_for('index'))

    index = session['index']
    score = session['score']
    attempts = session['attempts']
    user = session['username']
    
    if request.method == 'POST' and index < len(riddles):
        if request.form['answer'].lower() == riddles[index]['answer'].lower():
            score += 1
            index += 1
            attempts = 0
            if index < len(riddles):
                flash('Great answer, %s. Your current score is %s.' % (user, score), 'success')
        elif attempts < 2:
            attempts += 1
            if attempts == 2:
                flash('"%s" is the wrong answer, %s, this is your last chance.' % (request.form['answer'], user), 'second-warning')
            else:
                flash('"%s" is not the correct answer, %s. You have %s more attempts.' % (request.form['answer'], user, 3 - int(attempts)), 'first-warning')
        else:
            attempts = 0
            index += 1
            if index < len(riddles):
                flash('Wrong answer! Better luck next time', 'error')

    session['index'] = index
    session['score'] = score
    session['attempts'] = attempts

    if index >= len(riddles):
        if not session['updated']:
            scores.append({'username' : session['username'], 'score' : session['score']})
            session['updated'] = True
        flash('Congratulations %s, you have finished the game. You scored %s points.' %(user, score), 'victory')
        return render_template('riddle.html', question='', index='', victory=True)
    else:
        return render_template('riddle.html', question=riddles[index]['question'], index=index+1, victory=False)

if __name__ == '__main__':
    app.secret_key = os.getenv('SECRET')
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=False)