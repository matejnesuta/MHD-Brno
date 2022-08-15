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
    r = parse()
    print(r.url)
    soup = bs(r.text, 'html.parser')
    divs = soup.find("div", { "class" : "connection-list" }).findAll("div", { "class" : "box"}, recursive=False)
    for div in divs:
        header = div.find("h2")
        date = header.find("span").extract().string
        arrival = header.string
        dot = date.find(".")
        if date[4]==".":
            date = date[:dot+1] + "0" + date[dot+1:]
            date = date[:5] + date[6:]
        date = date.replace(".","-")
        p = div.find("p").text
        print("-"*80)
        print("|", arrival, "|", date, "|",p)
        print("-"*80)
        vehicles = div.findAll("div", { "class" : "outside-of-popup"})
        for vehicle in vehicles:
            name = vehicle.find("h3").text
            print(name)
            stations = vehicle.find("ul").text
            print(stations)
    # divs = soup.findAll("div", class_="title-container")
    # print(divs)
    # vehicle{
        
    # }
    # departure = soup.find("div", class_="reset stations first last").find("span")
    # print(departure)
    # for child in div:
    #     print(child)
scrape()