    
import sys
import os

class Logger:
    def __init__(self):
        self.message = ''

    # def print(self, message):
    #     self.message = str(message)
    #     sys.stdout.write('\r' +  str(message))
    #     sys.stdout.flush()


    def print(self, message):
        os.system('cls')
        self.message = str(message)
        lines = message.split('\n')
        for i, line in enumerate(lines):
            if i == 0:
                sys.stdout.write('\r' + line)
            else:
                sys.stdout.write('\n' + line)
        sys.stdout.flush()