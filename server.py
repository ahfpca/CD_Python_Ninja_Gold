from flask import Flask, render_template, request, redirect, session
import random, datetime

app = Flask(__name__)
app.secret_key = "duifhwe87gebiw"


# Play ground items
playObj = [
    {"name": "Farm", 
    "lowRng": 10, 
    "highRng": 20, 
    "justEarn": True },

    {"name": "Cave", 
    "lowRng": 5, 
    "highRng": 10, 
    "justEarn": True },

    {"name": "House", 
    "lowRng": 2, 
    "highRng": 5, 
    "justEarn": True },

    {"name": "Casino", 
    "lowRng": 0, 
    "highRng": 50, 
    "justEarn": False }
    ]


@app.route("/")
def index():
    if "totalGold" not in session:
        session["totalGold"] = 0

    if "ninjaActs" not in session:
        session["ninjaActs"] = []
    
    return render_template("index.html", playObject = playObj)


@app.route("/process_money", methods=["POST"])
def processMoney():
    for obj in playObj:
        if obj["name"] == request.form["actPlace"]:
            goldNum = random.randrange(obj["lowRng"], obj["highRng"] + 1)

            mode = 1 # Earn
            if obj["justEarn"] == False:
                mode = random.randrange(0, 2)

            name = obj["name"]
            actStr = ""

            if mode == 1: # EARNED
                actStr = f"Earned { goldNum } from the { name }! ({ datetime.datetime.now() })"
                session["totalGold"] += goldNum
            else: # LOST
                actStr = f"Entered a { name } and lost { goldNum } golds... Ouch! ({ datetime.datetime.now() })"
                session["totalGold"] -= goldNum

            # Creating Ninja act's object
            newAct = {  
                "mode": mode,
                "action": actStr
            }

            # Add it to session
            session["ninjaActs"].append(newAct)

            break

    return redirect("/")


@app.route("/reset")
def reset():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug = True)
