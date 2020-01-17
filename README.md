# reddit-NBA-stats
A reddit bot that will retrieve various statistics given an NBA player.

## Required
* [praw](https://praw.readthedocs.io/en/latest/)
* [requests](https://requests.readthedocs.io/en/master/)
* [nameparser](https://github.com/derek73/python-nameparser)

## Usage 
Clone repository and ensure that you have installed all of the required modules as listed above. In main.py, set the subreddit_choice variable to the subreddit that you wish to monitor. Next fill out the praw configuration by following what is listed in sampleConfig.py. Run main.py locally and navigate to the subreddit that you have chosen to monitor. Now you can send the bot a query of this format.

'!stats N firstname lastname suffix'

* N = Range of games (optional)
* firstname = Players first name
* lastname = Players last name
* suffix = Any suffix if applicable (optional)

