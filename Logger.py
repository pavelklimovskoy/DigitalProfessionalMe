from datetime import datetime

def log(data):
    logFile = open("logs/logs.txt", 'a')
    current_time = datetime.now().time()
    logFile.write(str(current_time) + " " + str(data) + "\n")
