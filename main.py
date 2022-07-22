import sys, getopt
import requests
import re
import datetime
from bs4 import BeautifulSoup as bs

def help():
    print("help")
    sys.exit

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    argv = sys.argv[1:]
    beginning = ''
    end = ''
    date = ''
    time = ''
    direct = "false"
    try:
        opts, args = getopt.getopt(argv,"hb:e:d:t:","direct")
    except getopt.GetoptError:
        eprint("Unknown parameters!")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            help()            
        elif opt in ("-b"):
            beginning = arg
        elif opt in ("-e"):
            end = arg
        elif opt in ("-d"):
            date = arg
        elif opt in ("-t"):
            time = arg
        elif opt in ("--direct"):
            direct = "true"
    
    base = "https://idos.idnes.cz/brno/spojeni/vysledky/"
    entry = f"?f={beginning}&t={end}&direct={direct}"
    if (time):
        if (re.match("^(([0-1][0-9])|2[0-3]):[0-5][0-9]$", time)):
            entry = entry + "&time=" + time 
        else:
            eprint("Wrong time format!")
            sys.exit(3)
    
    if (date):
        try:
            datetime.datetime.strptime(date, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Wrong date format, should be DD.MM.YYYY")
        entry = entry + "&date=" + date

    r = requests.get(base+entry)
    print(r.json)
main()