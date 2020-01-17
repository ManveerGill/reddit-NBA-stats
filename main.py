import praw
import requests
import json
import config
from nameparser import HumanName

subreddit_choice = ''

with open('players.json', 'r') as fp: # Load JSON file into program
    obj = json.load(fp)

def findPlayer(obj, firstName, lastName): # Function that will perform a search on the JSON file of players. Looks for a sucessful match in first and last name, ignoring case and some special characters. Returns the playerID.
    for dict in obj:
        if dict['firstName'].lower().translate(str.maketrans('','',"!?.,'123456789-")) == firstName.lower() and dict['lastName'].lower().translate(str.maketrans('','',"!?.,'123456789-")) == lastName.lower(): # Remove any odd characters. Sometimes users forget a hyphen etc.
            return dict['playerID']

request_headers = {
    'Host':'stats.nba.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Referer': 'stats.nba.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}

reddit = praw.Reddit(
    client_id = config.client_id,
    client_secret = config.client_secret,
    username = config.username ,
    password = config.password ,
    user_agent = config.user_agent)

subreddit = reddit.subreddit(subreddit_choice) # We only want the bot running on this specific subreddit
keyphrase = '!stats ' # Bot responds to this keyphrase only.

for comment in subreddit.stream.comments(skip_existing=True): # Watch the comment stream on our subreddit of choice
    if keyphrase in comment.body:
        tableBase = "PTS|REB|AST|STL|BLK|TOV|3PM|FG%|FT%\n:--|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--\n" # We want to format our response neatly, this is just the formatting convention Reddit uses to create tables. 
        N = 0 # N represents the number of games to include in our averages. N = 0 will default to pulling averages for the entire season so far. 

        player = comment.body.replace(keyphrase, '') # Get rid of the keyphrase leaving us with the players name and optionally an N value
        player = HumanName(player.translate(str.maketrans('','',"!?.,'-")))

        if (player.first.isdigit() == True): # If the user entered a number
            N = player.first
            player.first = player.middle

        if player.suffix == '': # Player did not enter a suffic (Jr, III etc)
            playerID = findPlayer(obj, player.first, player.last)
        else:
            playerID = findPlayer(obj, player.first, player.last + " " + player.suffix)

        if playerID != None:
            URL = 'https://stats.nba.com/stats/playerdashboardbylastngames/?measureType=Base&perMode=PerGame&plusMinus=N&paceAdjust=N&rank=N&leagueId=00&season=2019-20&seasonType=Regular+Season&poRound=0&playerId=' + str(playerID) + '&outcome=&location=&month=0&seasonSegment=&dateFrom=&dateTo=&opponentTeamId=0&vsConference=&vsDivision=&gameSegment=&period=0&shotClockRange=&lastNGames=' + str(N)
        
            r = requests.get(url = URL, headers = request_headers)
            data = r.json()
            try:
                stats = data["resultSets"][0]["rowSet"][0] # The data we want is nested here
                tableBase = tableBase + str(stats[26]) + "|" + str(stats[18]) + "|" + str(stats[19]) + "|" + str(stats[21]) + "|" + str(stats[22]) + "|" + str(stats[20]) + "|" + str(stats[10]) + "|" + str(stats[9]) + "|" + str(stats[15]) # Refer to /doc/headerMapping.txt for additional mappings.
                comment.reply(tableBase)
            except:
                comment.reply("Error: This player is active on a roster but has not played this season.")
        else:
            comment.reply("Error: No such player was found. Please ensure you include the suffix if applicable and any hyphens or other special characters (Karl-Anthony Towns, Willie Cauley-Stein, Marvin Bagley III etc). Please note that the bot will only provide statistics for people who have played this year.")
