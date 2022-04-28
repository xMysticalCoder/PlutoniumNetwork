import os
from replit import db
import time
import keep_alive
import random
import requests


apikey = os.environ["APIKEY"]
city = "new york city"
city = city.replace(" ", "+")
url = "http://api.openweathermap.org/data/2.5/weather?appid=baede7da17f762fbffef4981ca45dad1&q="+city

data = requests.get(url).json()
print(round(1.8*(data["main"]["temp"]-273)+32))


os.system(
    'pip install scratch2py & pip install --force-reinstall websocket-client')
from scratch2py import Scratch2Py

username = os.environ['username']
password = os.environ['password']
while True:
    try:
        s2py = Scratch2Py(username, password)
    except:
        print("Login failed, trying again.")
        continue
    break
print("Connected to user")
cloudproject = s2py.scratchConnect('658854833')
print("Connected to project and cloud variables")


def readVar(name):
    return cloudproject.readCloudVar(name)


def setVar(name, val):
    return cloudproject.setCloudVar(name, val)


def resetDatabase():
    for i in db.keys():
      try:
        print(f"Deleting {i}")
        del db[i]
      except:
        print(f"Couldn't delete {i}")
    print("Server reset complete")
    db["Ads"] = []
    print("Ads are reset")


project = s2py.project('658854833')
loop = 0

keep_alive.keep_alive()

while True:
    try:
        print(project.getComments()[0]["author"]["username"])
        loop += 1
        print(f"Server has been up for {loop} loops")
        #time.sleep(0)
        if str(readVar("weather_get")) != "0":
          location = readVar("weather_get")
          city = str(s2py.decode(location))
          city = city.replace(" ", "+")
          url = "http://api.openweathermap.org/data/2.5/weather?appid=baede7da17f762fbffef4981ca45dad1&q="+city
          try:
            data = requests.get(url).json()
            setVar("weather_recieve",round(1.8*(data["main"]["temp"]-273)+32))
            
          except:
            setVar("weather_recieve", "123456789")
          setVar("weather_get", 0)
        # WEBSITE SEARCHING
        if str(readVar("search")) != "0":
            print("Search found")
            print(readVar("search"))
            search = s2py.decode(str(readVar("search")))
            print(f"Decoded search {search}")
            if search.lower() in db.keys():
                print("Website found")
                search = search.lower()
                print(db[search])
                setVar("result", s2py.encode(str(db[search][1])))
                try:
                    ad = db["Ads"][random.randint(0, len(list(db["Ads"])) - 1)]
                except:
                    ad = "No ads are created yet."
                print(f"Sending ad {ad}")

                setVar("ad", s2py.encode(ad))
                setVar("search", 0)
            else:
                print("Website not found")
                setVar("result", 1)
                setVar("search", 0)
        
            
          

            
        else:
            # WEBSITE CREATION
            latestComment = project.getComments()[0]["content"]
            if latestComment.startswith(
                    "createWebsite(") and latestComment.endswith(
                        ")") and "," in latestComment:
                latestComment = latestComment.split("(")
                latestComment = latestComment[1]
                latestComment = latestComment.split(")")
                latestComment = latestComment[0]
                latestComment = latestComment.split(",")
                print("Split latest comment")
                if latestComment[0] in db.keys() or len(
                        latestComment[1]) > 128 or len(latestComment[0]) > 128:
                    print(
                        f"Attempted to create website {latestComment[0]} with data {latestComment[1]}"
                    )
                    continue
                else:
                    db[latestComment[0].lower()] = [
                        project.getComments()[0]["author"]["username"],
                        latestComment[1]
                    ]
                    print(
                        f'Created website {latestComment[0]} with data {latestComment[1]} made by {project.getComments()[0]["author"]["username"]}'
                    )

            # WEBSITE EDITING
            latestComment = project.getComments()[0]["content"]
            author = project.getComments()[0]["author"]["username"]
            if latestComment.startswith(
                    "editWebsite("
            ) and "," in latestComment and latestComment.endswith(")"):
                latestComment = latestComment.split("(")
                latestComment = latestComment[1]
                latestComment = latestComment.split(")")
                latestComment = latestComment[0]
                latestComment = latestComment.split(",")
                if author == db[latestComment[0]][0]:
                    db[latestComment[0]][1] = latestComment[1]

            # ADVERTISEMENT CREATION
            latestComment = project.getComments()[0]["content"]
            if latestComment.startswith(
                    "createAd(") and latestComment.endswith(")"):
                print("Got advertisement")
                latestComment = latestComment.split("(")
                latestComment = latestComment[1]
                latestComment = latestComment.split(")")
                latestComment = latestComment[0]
                print(latestComment)
                if latestComment in list(db["Ads"]):
                    print("Ad already exists")
                else:
                    db["Ads"] = list(db["Ads"]) + [latestComment]
                    print("Ad created")
            

    except:
        print("Loop failed. Trying startup sequence.")
        while True:
            try:
                s2py = Scratch2Py(username, password)
                cloudproject = s2py.scratchConnect('658854833')
                project = s2py.project('658854833')
                print("Startup sequence complete.")
                break
            except:
                print("Login failed, trying again.") #add multi acc switching from HAL
                continue
