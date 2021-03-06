from datetime import datetime
import datetime as dt
import json

def isFormat(date, format):
    try:
        if date != datetime.strptime(date, format).strftime(format):
            raise ValueError
        return True
    except ValueError:
        return False

def dateFormating(date):
    if isFormat(date,"%d/%m/%y"):
        date = datetime.strptime(date,"%d/%m/%y")
    elif isFormat(date,"%d-%m-%y"):
        date = datetime.strptime(date,"%d-%m-%y")
    elif isFormat(date,"%d/%m"):
        date = datetime.strptime(date,"%d/%m")
        date = date.replace(year=datetime.now().year)
    elif isFormat(date,"%d-%m"):
        date = datetime.strptime(date,"%d-%m")
        date = date.replace(year=datetime.now().year)
    else :
        return None

    if ((date.month < datetime.now().month) or (date.month == datetime.now().month and date.day < datetime.now().day)) and date.year <= datetime.now().year:
        date = date.replace(year=datetime.now().year + 1)
    
    return date

def getDevoirs():
    with open("devoirs.json", "r") as myfile:
        return json.load(myfile)

def setDevoirs(devoirs):
    devoirs["fields"].sort(key=lambda item: item.get("date"))
    with open("devoirs.json", "w") as myfile:
        myfile.write(json.dumps(devoirs))

def devoirsParMatiere(matiere = ""):
    devoirs = getDevoirs()
    devoirsPrets = {"title": devoirs["title"], "color": 16711680, "fields": []}
    i = 0
    for element in devoirs["fields"]:
        if element["name"].lower() == matiere.lower() or matiere == "":
            date = datetime.fromisoformat(element["date"])
            date_str = date.strftime("%d/%m/%Y")
            toAppend = {"name": devoirs["fields"][i]["name"], "value": devoirs["fields"][i]["value"] + " pour le " + date_str}
            devoirsPrets["fields"].append(toAppend)
            i += 1
    return devoirsPrets

def devoirsParDate(laDate = datetime(dt.MINYEAR,1,1)):
    devoirs = getDevoirs()
    devoirsPrets = {"title": devoirs["title"], "color": 16711680, "fields": []}
    
    for element in devoirs["fields"]:
        date = datetime.fromisoformat(element["date"])
        if (date.day == laDate.day and date.year != dt.MINYEAR) or laDate.year == dt.MINYEAR:
            date_str = date.strftime("%d/%m/%Y")
            toAppend = {"name": date_str + " : " + element["name"], "value": element["value"]}
            devoirsPrets["fields"].append(toAppend)
    return devoirsPrets
