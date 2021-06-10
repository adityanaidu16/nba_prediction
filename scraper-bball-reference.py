import requests
from bs4 import BeautifulSoup
import csv
import re

boxscores = []
visitteams = []
fullStats = []
months = ['october', 'november', 'december', 'january', 'february', 'march']
years = ['2017', '2018', '2019', '2020', '2021']

for y in years:                                                                                                      # Collect y-year Schedule page
    for m in months:
        page = requests.get(('https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html').format(y,m))       # Collect m-month Schedule page

        soup = BeautifulSoup(page.text, 'html.parser')

        for link in soup.find_all('th', attrs={'data-stat':'date_game'}):
            csk = link.get('csk')
            if type(csk)==str:
                boxscores.append(csk)
            else:
                pass

        for link in soup.find_all('td', attrs={'data-stat':'visitor_team_name'}):
            visitteams.append((link.get('csk'))[0:3])

res = dict(zip(boxscores, visitteams))
fields=['fg', 'fga', 'fg3', 'fg3a', 'ft', 'fta', 'orb', 'drb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts','finalpoints', 'wins', 'gp','oppfg', 'oppfga', 'oppfg3', 'oppfg3a', 'oppft', 'oppfta', 'opporb', 'oppdrb', 'oppast', 'oppstl', 'oppblk', 'opptov', 'opppf', 'opppts', 'oppfinalpoints', 'oppwins', 'oppgp']

with open("nbascrape.csv", "w", newline='') as csvFile:
    csvwriter = csv.writer(csvFile)
    csvwriter.writerow(fields)
    numprocess=0
    times = 1

    for csk in res:
        numprocess+=1
        if numprocess==100:
            print((numprocess*times), end = '')
            print("games done")
            numprocess = 0
            times+=1

        page = requests.get(('https://www.basketball-reference.com/boxscores/{}.html').format(csk))                 # Collect the page

        soup = BeautifulSoup(page.text, 'html.parser')                                                              # Create a BeautifulSoup object 

        homestats = []
        awaystats = []

        home = (csk[-3:])
        away = res[csk]

        for a in soup.find_all(id=('div_box-{}-q1-basic').format(home)):                                            # get dataset for home team

            fg=a.find_all('td', attrs={'data-stat':'fg'})
            fga=a.find_all('td', attrs={'data-stat':'fga'})
            fg3=a.find_all('td', attrs={'data-stat':'fg3'})
            fg3a=a.find_all('td', attrs={'data-stat':'fg3a'})
            ft=a.find_all('td', attrs={'data-stat':'ft'})
            fta=a.find_all('td', attrs={'data-stat':'fta'})
            orb=a.find_all('td', attrs={'data-stat':'orb'})
            drb=a.find_all('td', attrs={'data-stat':'drb'})
            ast=a.find_all('td', attrs={'data-stat':'ast'})
            stl=a.find_all('td', attrs={'data-stat':'stl'})
            blk=a.find_all('td', attrs={'data-stat':'blk'})
            tov=a.find_all('td', attrs={'data-stat':'tov'})
            pf=a.find_all('td', attrs={'data-stat':'pf'})
            pts=a.find_all('td', attrs={'data-stat':'pts'})
            for a in soup.find_all(id=('box-{}-game-basic').format(home)):
                finalpoints=a.find_all('td', attrs={'data-stat':'pts'})

            for a in soup.find_all(id=('box-{}-game-basic_sh').format(home)):
                record=a.find('h2')
            record = str(record)
            record = re.findall('\(([^)]+)', record)
            record = record[0]
            record_parts = record.split('-')
            wins = int(record_parts[0])
            losses = int(record_parts[-1])
            gp = wins+losses


            while len(homestats) < 13:
                homestats.append(fg.pop().text)
                homestats.append(fga.pop().text)
                homestats.append(fg3.pop().text)
                homestats.append(fg3a.pop().text)
                homestats.append(ft.pop().text)
                homestats.append(fta.pop().text)
                homestats.append(orb.pop().text)
                homestats.append(drb.pop().text)
                homestats.append(ast.pop().text)
                homestats.append(stl.pop().text)
                homestats.append(blk.pop().text)
                homestats.append(tov.pop().text)
                homestats.append(pf.pop().text)
                homestats.append(pts.pop().text)
                homestats.append(finalpoints.pop().text)
                homestats.append(wins)
                homestats.append(gp)
            else:
                break


        for a in soup.find_all(id=('div_box-{}-q1-basic').format(away)):                                            # get dataset for away team
            fg=a.find_all('td', attrs={'data-stat':'fg'})
            fga=a.find_all('td', attrs={'data-stat':'fga'})
            fg3=a.find_all('td', attrs={'data-stat':'fg3'})
            fg3a=a.find_all('td', attrs={'data-stat':'fg3a'})
            ft=a.find_all('td', attrs={'data-stat':'ft'})
            fta=a.find_all('td', attrs={'data-stat':'fta'})
            orb=a.find_all('td', attrs={'data-stat':'orb'})
            drb=a.find_all('td', attrs={'data-stat':'drb'})
            ast=a.find_all('td', attrs={'data-stat':'ast'})
            stl=a.find_all('td', attrs={'data-stat':'stl'})
            blk=a.find_all('td', attrs={'data-stat':'blk'})
            tov=a.find_all('td', attrs={'data-stat':'tov'})
            pf=a.find_all('td', attrs={'data-stat':'pf'})
            pts=a.find_all('td', attrs={'data-stat':'pts'})
            for a in soup.find_all(id=('box-{}-game-basic').format(away)):
                finalpoints=a.find_all('td', attrs={'data-stat':'pts'})

            for a in soup.find_all(id=('box-{}-game-basic_sh').format(away)):
                record=a.find('h2')
            record = str(record)
            record = re.findall('\(([^)]+)', record)
            record = record[0]
            record_parts = record.split('-')
            wins = int(record_parts[0])
            losses = int(record_parts[-1])
            gp = wins+losses


            while len(awaystats) < 16:
                awaystats.append(fg.pop().text)
                awaystats.append(fga.pop().text)
                awaystats.append(fg3.pop().text)
                awaystats.append(fg3a.pop().text)
                awaystats.append(ft.pop().text)
                awaystats.append(fta.pop().text)
                awaystats.append(orb.pop().text)
                awaystats.append(drb.pop().text)
                awaystats.append(ast.pop().text)
                awaystats.append(stl.pop().text)
                awaystats.append(blk.pop().text)
                awaystats.append(tov.pop().text)
                awaystats.append(pf.pop().text)
                awaystats.append(pts.pop().text)
                awaystats.append(finalpoints.pop().text)
                awaystats.append(wins)
                awaystats.append(gp)
            else:
                fullStats = homestats + awaystats
                csvwriter.writerow(fullStats)
                break
            



