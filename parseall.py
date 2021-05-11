import os
import sys
import csv
import parsedemo
import allnames

path = sys.argv[1]
series = [s for s in os.listdir(path) if not s.endswith(".csv")]
scount = 1

matchheader = ['date','team1','team2','match#','map','score blu','score red','targets blu','targets red','player','character','team','score (team)','score (enemy)','deaths','targeted']
playerheader = []

header = matchheader + playerheader

with open(path+'/playerstats.csv','w',newline='') as csvfile:
	csvw = csv.writer(csvfile, delimiter=',')
	csvw.writerow(header)

	for s in series:
		matches = os.listdir(path + "/" + s)
		matches = [m for m in os.listdir(path + "/" + s) if m.endswith(".cohdemo")]
		mcount = 1
		for match in matches:
			m = path + "/" + s + "/" + match

			matchid = match.split(".")[0] # match number in series
			seriesdate = s.split("_")[0] # yymmdd
			team1 = s.split("_",1)[1] # typically team1 is the demo recorder's side
			team2 = ''
			if "_" in team1:
				team2 = team1.split('_')[1]
				team1 = team1.split('_')[0]
			if team1 == 'kb': # rename shorthand
				team1 = 'kickball'

			print("[" + str(scount) + " of " + str(len(series)) + "] [" + s + " " + str(mcount) + " of " + str(len(matches)) + "]") # print progress to terminal
			
			players, match_map, deaths, targets, targeted = parsedemo.main(m, True)
			score = {'BLU':deaths['RED'],'RED':deaths['BLU']}

			for p in players.values():

				# player data formatting
				wld = [0,0,0] # win loss draw
				if score[p.team] > deaths[p.team]:
					wld[0] = 1
				elif score[p.team] < deaths[p.team]:
					wld[1] = 1
				elif score[p.team] == deaths[p.team]:
					wld[2] = 1
				psupport = 0
				if p.support:
					psupport = 1

				playername = ""
				if p.name in allnames.toons: # attempt to get player name from toon name
					playername = allnames.toons[p.name] 

				matchdata  	= [seriesdate,team1,team2,matchid,match_map,score['BLU'],deaths['BLU'],targets['BLU'],targets['RED']] # 9
				playerdata	= [playername,p.name,p.team,wld[0],wld[1],wld[2],p.deathtotal,p.targeted,p.set1,p.set2,p.archetype,psupport] # 12
				offencedata = [p.ontarget,p.ontarget/max(targets[p.team],1),p.attackstotal,p.attacks,p.first,p.avgspiketiming,p.avgspiketimingvar,p.avgspikedist,] #
				defencedata	= [-p.totaldmgtaken,-p.totaldmgtakenonspike,p.firstblood,20-p.greens]
				supportdata = ['']*7
				if p.support:
					supportdata = [p.healontarget,p.healontarget/max(targeted[p.team]-p.targeted,1),p.healstotal,p.ontargetheals,p.healalpha,p.avghealspeed,p.avghealspeedvar]

				csvdata = matchdata + playerdata + offencedata + defencedata + supportdata
				csvw.writerow(csvdata)

			mcount += 1
		scount += 1
