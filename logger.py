import datetime

class Logger():
    def __init__(self):
        self.loggingDirectory = r"./Logs/"
        self.current_date = datetime.datetime.now().strftime('%m%d%Y')
        
        if __name__ == "RanAtMain":
            with open(self.loggingDirectory + self.current_date + "log.txt", "a") as f:
                f.write(f"\n{self.current_date} - {datetime.datetime.now().strftime('%H:%M:%S')} - Program Started\n")
                
            with open(self.loggingDirectory + self.current_date + "log.txt", "a") as f:
                f.write(f"{datetime.datetime.now().strftime('%H:%M:%S')} - logging started\n")
            
    def addToLog(self, message):
        with open(self.loggingDirectory + self.current_date + "log.txt", "a") as f:
            f.write(f"{datetime.datetime.now().strftime('%H:%M:%S')} - {message}\n")
        