import sys, getopt
import requests
import re
import datetime
from bs4 import BeautifulSoup as bs

def help():
    print("This script scrapes the IDOS web page for Brno and outputs the scheduled buses and trams on the stdout.")
    print("\nusage:")
    print("python main.py -b starting_destination -e end_destination [ options ] [ direct ]\n")
    print("python main.py -h")
    print("Required flags:")
    print("\t-b [bus_stop]\t - sets the location we want to take a bus/from.")
    print("\t-e [bus_stop]\t - sets our desired end location.")
    print("\nOptional arguments:\n")
    print("\t-d DD.MM.YYYY\t - sets the date of the journey (takes system date if flag is not set)")
    print("\t-h | --help\t - prints help (this has priority over the rest of the flags)")
    print("\t-t HH:MM\t - sets the time of bus/tram arrival to the starting location (takes system time if flag is not set)")
    print("\t--direct\t - sets if the route should be direct or not (default is false)")
    print("\n")
    sys.exit(0)

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def parse():
    argv = sys.argv[1:]
    beginning = ''
    end = ''
    date = ''
    time = ''
    direct = "false"
    
    try:
        opts, args = getopt.getopt(argv,"hb:e:d:t:",["direct","help"])
    except getopt.GetoptError:
        eprint("Unknown parameters!")
        sys.exit(1)
    for opt, arg in opts:
        if opt == "-h" or opt == "--help":
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
            # raise ValueError("Wrong date format, should be DD.MM.YYYY.")
        entry = entry + "&date=" + date

    r = requests.get(base+entry)
    return r

def scrape():
    r = parse()
    print(r.url)

scrape()