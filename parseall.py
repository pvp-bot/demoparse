import os
import sys
import csv
import parsedemo
from data.playernames import playerdict

path = sys.argv[1]
series = [s for s in os.listdir(path) if not s.endswith(".csv")]
series.sort()

scount = 1

matchheader = [ 'date',			'team1',		'team2',	'seriesid',		'matchid',	'match#',	'map',		'score_blu',	'score_red','targets_blu',	'targets_red',	
				'player',		'character',	'pteam',	'win',			'loss',		'draw',		'deaths',	'targets',		'set1',		'set2',			'at',			'support',	
				'ontarget',		'otp',			'atks',		'atks target',	'first',	'avg timing',			'timing var',	'avg dist',	
				'dmg',			'spike dmg',	'first blood time',			'greens used',	
				'heal on target',	'heal otp',	'heals',	'heals spike',	'heal alpha',	'heal speed',	'heal speed var',]

playerheader = []

header = matchheader + playerheader

with open(path+'/playerdata.csv','w',newline='') as csvfile:
	csvw = csv.writer(csvfile, delimiter=',')
	csvw.writerow(header)

	for s in series:
		matches = os.listdir(path + "/" + s)
		matches = [m for m in os.listdir(path + "/" + s) if m.endswith(".cohdemo")]
		matches.sort()
		mcount = 1
		for match in matches:
			m = path + "/" + s + "/" + match

			matchno = match.split(".")[0] # match number in series
			seriesdate = s.split("_")[0] # yymmdd
			team1 = s.split("_",1)[1] # typically team1 is the demo recorder's side
			team2 = ''
			if "_" in team1:
				team2 = team1.split('_')[1]
				team1 = team1.split('_')[0]
			
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
				# player, toonlist
				for k,v in playerdict.items(): # attempt to get player name from toon name
					if p.name.lower() in (toon.lower() for toon in v):
						playername = k
						break

				matchid = s+matchno

				matchdata  	= [seriesdate,team1,team2,s,matchid,matchno,match_map,score['BLU'],deaths['BLU'],targets['BLU'],targets['RED']] # 11
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
