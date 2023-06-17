import os
import sys


class runSingle:
    """
    Prevents script from running more than once at the same time
    """
    def __init__(self, fileName) -> None:
        self.f = open(fileName, "w")
        self.f.close()
        try:
            os.remove(fileName)
            self.f = open(fileName, "w")
        except WindowsError:
            sys.exit()
