class Logging():
    def __init__(self):
        pass

    def info(self, header, message):
        print("{} Info: {}".format(header, message))
    
    def error(self, header, message):
        print("{} Error with: {}".format(header, message))
        