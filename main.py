'''This script does nothing but sends a get request to the IDOS page
and then scrapes the resulting page'''

import sys
import re
import datetime
import argparse
import requests
from bs4 import BeautifulSoup as bs

def eprint(*args, **kwargs):
    '''This prints on stderr with ease'''
    print(*args, file=sys.stderr, **kwargs)

def time_formatter(t):
    # dot = time.find(":")
    if t[1] ==":":
        return "0"+t[:1] + t[1:]
    else:
        return t
                 

def parse():
    '''This is where the arg parsing and url building happens'''
    beginning = ''
    end = ''
    date = ''
    time = ''
    direct = False
    parser = argparse.ArgumentParser(description='''This script scrapes the 
        IDOS web page for Brno and outputs the scheduled buses and trams on the stdout.''')
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
    elif beginning==end:
        eprint("Overlapping stations. Aborting the program.")
        sys.exit(3)
    else:
        base = "https://idos.idnes.cz/en/brno/spojeni/vysledky/"
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
    '''This is where the scraping happens'''
    r = parse()
    # print(r.url)
    soup = bs(r.text, 'html.parser')
    divs = soup.find("div", { "class" : "connection-list" }).findAll("div", { "class" : "box"}, recursive=False)
    for div in divs:
        print("")
        header = div.find("h2")
        date = header.find("span").extract().string
        arrival = time_formatter(header.string)
        dot = date.find(".")
        if date[4]==".":
            date = date[:dot+1] + "0" + date[dot+1:]
            date = date[:5] + date[6:]
        date = date.replace(".","-")
        print("_"*80+"\n")
        p = div.find("p").text
        print("-"*80)
        print("|", arrival, "|", date, "|",p)
        print("-"*80)
        vehicles = div.findAll("div", { "class" : "outside-of-popup"})
        for vehicle in vehicles:
            walk = vehicle.find("div", { "class" : "walk"})
            if walk != None:
                print("\n  "+walk.text.strip())
            name = vehicle.find("h3").text
            border = len(name)
            print("  "+"-"*(border+2))
            print("  |"+name+"|")
            print("  "+"-"*(border+2))
            stations = vehicle.findAll("li")
            for station in stations:
                time = time_formatter(station.find("p", {"class": "time"}).text)
                zone = station.find("span").extract().text
                name = station.find("p", {"class": "station"}).get_text()
                print(time.rjust(7," ")+" "+name.rjust(30, " ")+"   zone: "+zone)
            print("_"*80)
        print("")
    print("")
scrape()
