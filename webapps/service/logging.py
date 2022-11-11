class Logging(object):
    def __init__(self):
        pass

    @staticmethod
    def info(header, message):
        print(f'{header} Info: {message}')

    @staticmethod
    def error(header, message):
        print(f'{header} Error with: {message}')
