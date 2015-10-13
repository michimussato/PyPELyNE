import getpass, os, datetime

class timeTracker:
    def __init__(self, assetName, taskName, projectPath):
        #super(timeTracker).__init__(None)

        self.trackerRoot = os.path.join(projectPath, 'timetracker')

        self.user = getpass.getuser()
        self.assetName = assetName
        self.taskName = taskName

        if not os.path.exists(self.trackerRoot):
            os.makedirs(self.trackerRoot, mode=0777)

        self.trackerData = os.path.join(self.trackerRoot, 'timetracker.csv')

        if not os.path.exists(self.trackerData):
            open(self.trackerData, 'a').close()

    def start(self):

        self.timeStartObject = datetime.datetime.now()
        self.timeStart = self.timeStartObject.strftime('%Y-%m-%d_%H%M-%S')
        self.timeStartDate = self.timeStartObject.strftime('%Y.%m.%d')
        self.timeStartTime = self.timeStartObject.strftime('%H:%M:%S')

        csv = open(self.trackerData, 'a')
        csv.write(self.user + '\t' + self.assetName + '__' + self.taskName + '\t' + 'START' + '\t' + self.timeStartDate + '\t' + self.timeStartTime + '\n')
        csv.close()

    def stop(self):

        self.timeStopObject = datetime.datetime.now()
        self.timeStop = self.timeStopObject.strftime('%Y-%m-%d_%H%M-%S')
        self.timeStopDate = self.timeStopObject.strftime('%Y.%m.%d')
        self.timeStopTime = self.timeStopObject.strftime('%H:%M:%S')

        self.timeDelta = self.timeStopObject - self.timeStartObject
        self.duration = str(self.timeDelta).split(".")[0]

        csv = open(self.trackerData, 'a')

        csv.write(self.user + '\t' + self.assetName + '__' + self.taskName + '\t' + 'STOP' + '\t' + self.timeStopDate + '\t' + self.timeStopTime + '\n')
        csv.write(self.user + '\t' + self.assetName + '__' + self.taskName + '\t' + 'DURATION' + '\t' + '\t' + '\t' + self.duration + '\n')

        csv.close()


def main():
    tracker = timeTracker()
    tracker.start()
    tracker.stop()




if __name__ == "__main__":
    main()