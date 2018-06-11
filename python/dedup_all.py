from dedup import nonemail_pstitems_tofile as nepi_tofile
from dedup import nonemail_pstitems as nepi
from dedup import email_pstitems as epi
from dedup import fileitems as fi


def main():
    nepi_tofile.run()
    nepi.run()
    epi.run()
    fi.run()


if __name__ == '__main__': main()
