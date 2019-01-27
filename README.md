# Riddle-Me-This Game Project

This is the 3rd project for the Full Stack Web Development bootcamp from Code Institute. The project comprises of a simple game of ***Riddles*** to be answered by the user.

* **Game's Source Code**

  * [Github](https://github.com/gbronca/ridle-me-this)

* **Game's Website**

  * [Riddle-Me-This](https://riddle-me-this-gb.herokuapp.com)

## UX

The idea is to have a simple and clean UX, but also interesting by the changing background images. No CSS Framerworks were used to build the project, only CSS Flexbox and Grid.

## Features

* The first page of app introduces the game and request the user's name.

* Once logged in, the game will present the user with a series of 10 riddles, one by one, and will award 1 point for ever correct answer. The user has 3 changes to answer correctly, before the game moves on to the next Riddle.

* Colour coded warining messages are presented, based on the user's response.

* The user can access the Scoreboard and the homepage without being logged out. By pressing "Return", the user is re-directed back to the game.

* The scores are ranked from highest to lowest.

* The Skip button allow the player to skip the current riddle.

* The background images changes everytime the page is refreshed.

## Tecnologies and Software Used

* [VS Code](https://code.visualstudio.com/)
* HTML5
* CSS Flexbox
* CSS Grid
* Python 3
* Flask

## Tests

No testing code has been written on this project.

All navigation buttons and links where tested in all stages of the game, ensuring they direct the user to the correct page and return the expected result.

The game was also played/tested by 3rd party players that reported any unusual behaviour.

The CSS was validated by [W3C CSS Validator](https://jigsaw.w3.org/css-validator/) and the HTML bt [W3C Markup Validator](https://validator.w3.org/).

The python file was checked by pylint.

## Images Source

The images are sourced from [Unsplash Sorce](https://source.unsplash.com/ "Unsplash Source")

## Deployment

* Created a new application in [Heroku](https://heroku.com) called [riddle-me-this-gb](https://riddle-me-this-gb.herokuapp.com)

* Create a requirements.txt file and Procfile
    > sudo pip3 freeze --local > requirements.txt
    > echo web: python run.py > Procfile

* To connect Heroku with GitHub and deploy the app
    > git remote add heroku <https://git.heroku.com/riddle-me-this-gb.git>
    > git push -u heroku master
    > heroku ps:scale web=1