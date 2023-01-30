import os
import sys


class runSingle:
    def __init__(self, fileName) -> None:
        self.f = open(fileName, "w")
        self.f.close()
        try:
            os.remove(fileName)
            self.f = open(fileName, "w")
        except WindowsError:
            sys.exit()
