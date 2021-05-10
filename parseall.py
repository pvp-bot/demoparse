import os
import sys
import csv
import parsedemo
import allnames

path = sys.argv[1]
series = [s for s in os.listdir(path) if not s.endswith(".csv")]
scount = 1
header = ['date','series','match','map','player','character','team','score (team)','score (enemy)','deaths','targeted']

with open(path+'/playerstats.csv','w',newline='') as csvfile:
	csvw = csv.writer(csvfile, delimiter=',')
	csvw.writerow(header)

	for s in series:
		matches = os.listdir(path + "/" + s)
		matches = [m for m in os.listdir(path + "/" + s) if m.endswith(".cohdemo")]
		mcount = 1
		for match in matches:
			m = path + "/" + s + "/" + match

			matchid = match.split(".")[0]
			seriesdate = s.split("_")[0]
			seriesteams = s.split("_",1)[1]

			print("[" + str(scount) + " of " + str(len(series)) + "] [" + s + " " + str(mcount) + " of " + str(len(matches)) + "]")
			
			deaths, players match_map = parsedemo.main(m, True)
			score = {'BLU':deaths['RED'],'RED':deaths['BLU']}
			for p in players.values():
				playername = ""
				if p.name in allnames.toons:
					playername = allnames.toons[p.name]
				playerdata = [seriesdate,seriesteams,matchid,match_map,playername,p.name,p.team,score[p.team],deaths[p.team],p.deathtotal,p.targeted]
				csvw.writerow(playerdata)

			mcount += 1
		scount += 1
