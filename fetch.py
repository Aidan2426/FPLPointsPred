import requests     #third party http that calls the api
import time     #python time module
import json

API = "https://fantasy.premierleague.com/api/"  #url
s = requests.Session()  #creates seesion for a reuseable connection
s.headers["User-Agent"] = "fpl-endpoint-check/1.0 (personal script)"    #bassically says whos calling

def get(path):  #function that takes endpoint path like fixtures
    r = s.get(API + path, timeout = 30) #joins base rul and path sends get request
    return r.status_code, (r.json() if r.headers.get("content-type", "").startswith("application/json") else None)  #returns the status code, 200 good, 404 not found, 403 = forbidden, also parses header starts with application/json

_, boot = get("bootstrap-static/")  #this gets everyting, _ thrwos away the status code and boot holds the json as a python dictonary
gw = next(e["id"] for e in boot["events"] if e["is_current"]) #Loops through the gameweeks and get the id of the first one marked as is current
#player = max(boot["elements"], key=lambda p: p["total_points"])["id"]  #looks thorugh all the players and finds the one with the most points, then gets their ID, the lambda is a tiny inline funciton telling max what to cmopre on

player = max(boot["elements"], key=lambda p: p["total_points"])


print(player["web_name"])

all_summaries = {}

for p in boot["elements"]:
    status, body = get(p)
    all_summaries=[boot["elements", "id"]]
    time.sleep(0.5)
    with open("raw_data.json", "w") as f: 
        json.dump(all_summaries, f)
    


print(player)

with open("raw_data.json", "w") as f: 
    json.dump(player, f)
    #json.dump(boot);   this is all the raw data


paths=[ #these are f strings, list of endpoint paths, plug variables in, element-summary/{player}/ would become element-summary/115/
    "bootstrap-static/",
    "fixtures/",
    f"fixtures/?event={gw}",
    f"element-summary/{player["id"]}/",
    "team/set-piece-notes/",
]

for p in paths: #goes through each path
    status, body = get(p)   #calls the helper function and upacks the 2 return values
    shape = list(body)[:4] if isinstance(body,dict) else f"list of {len(body)}" if isinstance(body, list) else"-"   #if the boyd is a dictonary show the first 4 keys, it it s allist then show list of N, otherwise show -
    print(f"{status} {p:<45} {shape}")  #prints one line per endpoint, left=-aligns a 45 character column so the output lines up
    time.sleep(0.5) #waits between each call to the server isn't flooded