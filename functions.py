from datetime import datetime

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
    
    return date