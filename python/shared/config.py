import sys
import os.path

class ConfigReader(object):

    def __init__(self):
        self._load()

    def get(self, key):
        if key in self._dict:
            return self._dict[key]
        else:
            print "ERROR: config property does not exist: " + key
            sys.exit()

    def _load(self):
        self._dict = {}

        with open('config.properties') as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) > 0 and line[0] != '!' and line[0] != '#':
                    tuple = line.partition('=')
                    key = tuple[0].strip()
                    val = tuple[2].strip()
                    self._dict[key] = val
