import requests
import json

URL = 'https://stats.nba.com/stats/commonallplayers/?leagueId=00&season=2019-20&isOnlyCurrentSeason=1' # May have to edit the season value for future seasons.

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

r = requests.get(url = URL, headers = request_headers)
data = r.json()
jstr = [{"playerID" : 000000, "firstName" : "John", "lastName" : "Smith"}] # Placeholder data, can be deleted.

for player in data["resultSets"][0]["rowSet"]:
    fullName = player[1].split(', ') # Names are returned as (Smith, John) so this line splits the name into first and last at the comma.
    try:
        entry = {"playerID" : player[0], "firstName" : fullName[1], "lastName" : fullName[0]}
        jstr.append({"playerID" : player[0], "firstName" : fullName[1], "lastName" : fullName[0]}) # Append our names onto our future json object.
    except:
        print('Error')
jstr = json.dumps(jstr, indent=2) # Make the json more readable by indenting it. 

with open ('players.json', 'w') as outfile: # Overwrites existing players.json, if there is one. 
    outfile.write(jstr)