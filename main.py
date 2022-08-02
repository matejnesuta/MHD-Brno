import sys
import requests
import re
import datetime
from bs4 import BeautifulSoup as bs
import argparse

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def parse():
    beginning = ''
    end = ''
    date = ''
    time = ''
    direct = False
    
    parser = argparse.ArgumentParser(description='This script scrapes the IDOS web page for Brno and outputs the scheduled buses and trams on the stdout.')
    parser.add_argument("beginning")
    parser.add_argument("end")
    parser.add_argument("--direct", action="store_true")
    parser.add_argument("-d")
    parser.add_argument("-t")
    args = parser.parse_args()

    beginning = args.beginning
    end = args.end
    direct = args.direct
    date = args.d
    time = args.t
    
    if (not beginning or not end):
        eprint("No starting point or destination found. Aborting the program.")
        sys.exit(2)
    elif(beginning==end):
        eprint("Overlapping stations. Aborting the program.")
        sys.exit(3)
    else:
        base = "https://idos.idnes.cz/brno/spojeni/vysledky/"
        entry = f"?f={beginning}&t={end}&direct={direct}"
    if (time):
        if (re.match("^(([0-1][0-9])|2[0-3]):[0-5][0-9]$", time)):
            entry = entry + "&time=" + time 
        else:
            eprint("Wrong time format.")
            sys.exit(4)
    
    if (date):
        try:
            datetime.datetime.strptime(date, '%d.%m.%Y')
        except ValueError:
            eprint("Wrong date format, should be DD.MM.YYYY.")
            sys.exit(5)
        entry = entry + "&date=" + date

    r = requests.get(base+entry)
    return r

def scrape():
    r = parse()
    print(r.url)

scrape()