import sys
import os.path

from distro import builder1
from distro import builder2


def main():
    path = '<path-to-output>'

    #uncomment one builder:
    #builder1.DistroBuilder(path).run()
    #builder2.DistroBuilder(path).run()



if __name__ == '__main__': main()
