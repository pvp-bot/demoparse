import csv
import shlex
import sys
import math
import numpy as np

from data.powers import *
from data.config import *
from data.Player import Player
from data.Target import Target

ms = 0          # demo time in ms
t = 0           # demo time in seconds

player_ids   = []
player_list  = []
players      = ''

spikes      = []

match_map = ""
starttime = 0 # in seconds

headers = ['time','actor','hp','deaths','team','action','target','targeted','demoline','line uid']
emotecheck = 0
lastactor = 0
writeline = False # flag to write line to csv
timeinc = False  # flag if inc has progressed in demo

lasttarget = {'BLU':'','RED':''}
lastgather = {'BLU':0,'RED':0}
gatherplayercount = {'BLU':0,'RED':0}
gathertimes = {'BLU':[],'RED':[]}

with open(sys.argv[1],'r') as fp:

	# blank out csv if existing
	with open(sys.argv[1]+'.csv','w',newline='') as csvfile:
		csvw = csv.writer(csvfile, delimiter=',')
		csvw.writerow(headers)

	line = shlex.split(fp.readline().replace('\\','').replace('\'',''))
	count = 0

	# initializing line loop - players, teams,
	while line and count < 30000: # 30k should be enough to find all players
		try:
			pid = int(line[1]) # player ID
			action = line[2]
		except:
			pid = 0 # ignore special actors like CAM
			action = ''
		if action == "Map":
			match_map = line[3]
			match_map = match_map.split('/')[-1]
			match_map = match_map.split('_')[1]
		if action == "NEW":
			if pid not in player_ids and line[3] not in name_filter:
				player_ids.append(pid)
				player_list.append(Player(line[3],pid))
		if action in npc and pid in player_ids: #
			del player_ids[-1]
			del player_list[-1]
		try:
			line = shlex.split(fp.readline().replace('\\','').replace('\'',''))
		except:
			print(count) # find broken lines
		count = count + 1

	players = dict(zip(player_ids,player_list))




	# back to start of file
	fp.seek(0)
	count = 0
	line = shlex.split(fp.readline().replace('\\','').replace('\'',''))

	# loop for assigning teams
	# assumes at least 1 buff-type power is thrown in the match per person
	num_players   = len(player_ids)
	count_players = 0
	buff_count	  = 0
	while line and count_players < num_players:
		try:
			pid = int(line[1])
			action = line[2] # catches weird lines without anything on it
		except:
			pid = 0 # ignore special
			action = ''
		if action == 'FX' and pid in player_ids:
			if any(substring for substring in buffs if substring in line[5]):
				buff_count = count
		elif action == 'TARGET' and count < (buff_count+5) and pid in player_ids:
			tid = int(line[4]) # target player id
			if tid in player_ids:
				if pid in player_ids and players[pid].team == '': # if  the buffer doesn't have a team
					count_players = count_players + 1
					players[pid].team = count_players
				if players[tid].team == '':
					players[tid].team = players[pid].team
					count_players = count_players + 1
				else:
					players[pid].team = min(players[pid].team,players[tid].team)
					players[tid].team = min(players[pid].team,players[tid].team)
		count = count + 1
		line = shlex.split(fp.readline().replace('\\','').replace('\'',''))

	for key, p in players.items():
		if p.team == 1:
			p.team = 'BLU'
		else:
			p.team = 'RED'


	# back to start of file
	fp.seek(0)
	line = shlex.split(fp.readline().replace('\\','').replace('\'',''))

	# loop for determining start of match/end of buffs
	# determine when 3 players on the same team are at least 20 yd from each other
	# method won't work if people are jaunting at the start I guess
	posstart = {}
	posids = []
	posteam = ''
	maxdist = 15 # 15 yards? < gather radius
	while line and starttime == 0:
		ms = ms + int(line[0]) # running demo time
		try:
			pid = int(line[1])
			action = line[2]
		except:
			pid = 0 # ignore special
			action = ''
		# first jump action of the game also works pretty well, usually before the POS check
		if action == 'MOV' and pid in player_ids:
			if 'JUMP' in line[3]:
				starttime = ms
				if starttime < 1000:
						starttime = 0

		elif action == 'POS' and pid in player_ids:
			if len(posstart) == 0:
				posstart[pid] = np.array([float(line[3]),float(line[5]),float(line[4])]) # swapping game x,z,y to typical x,y,z
				posids.append(pid)
				posteam = players[pid].team
			elif players[pid].team == posteam and pid not in posids and len(posids) < 3: # use 3 players on a team to determine
				posstart[pid] = np.array([float(line[3]),float(line[5]),float(line[4])])
				posids.append(pid)
			elif pid in posids and len(posids) == 3:
				posstart[pid] = np.array([float(line[3]),float(line[5]),float(line[4])])
				if (
					np.sqrt(np.sum((posstart[posids[0]]-posstart[posids[1]])**2)) > maxdist and
					np.sqrt(np.sum((posstart[posids[0]]-posstart[posids[2]])**2)) > maxdist and
					np.sqrt(np.sum((posstart[posids[1]]-posstart[posids[2]])**2)) > maxdist
				):
					starttime = ms
					if starttime < 1000:
						starttime = 0

		line = shlex.split(fp.readline().replace('\\','').replace('\'',''))



	# back to start of file
	fp.seek(0)
	ms = -starttime
	count = 0
	line = shlex.split(fp.readline().replace('\\','').replace('\'',''))
	lineuid = 0

	# ################################################ #
	# ################################################ #
	# MAIN PARSING LOOP ############################## # 
	# ################################################ #
	# ################################################ #

	with open(sys.argv[1]+'.csv','a',newline='') as csvfile:
		csvw = csv.writer(csvfile, delimiter=',')
		for key, p in players.items(): # print blu team first
			if p.team == 'BLU':
				csv_line = [-starttime/1000,p.name,'','',p.team,'','','',match_map]
				csvw.writerow(csv_line)
		for key, p in players.items(): # print blu team first
			if p.team == 'RED':
				csv_line = [-starttime/1000,p.name,'','',p.team]
				csvw.writerow(csv_line)

		while line and t <= matchtime: # ignore data after match end with small buffer time
			# print(count)
			ms = ms + int(line[0]) # running demo time
			t2 = (ms/1000) # to seconds
			if t2 > t or writeline:
				if t2 > t:
					timeinc = True
					gatherplayercount = {'BLU':0,'RED':0}
				else:
					timeinc = False

				for key, p in players.items():
					csv_line = [t,p.name,p.hp,p.death,p.team,p.action,p.target,p.targetinstance,count,lineuid]
					if p.hp != '' or p.death != '' or p.action  != '' or p.target != '' or p.targetinstance == 1:
						csvw.writerow(csv_line)
						lineuid += 1
						p.reset()
			t = t2


			try:
				pid = int(line[1])
				action = line[2]
			except:
				pid = 0 # ignore special

			if pid in players:

				if writeline: # write to csv if new action but team hasn't elapsed
					players[lastactor].reset()
					writeline = False
				lastactor = pid

				if action == "HP":
					hp  = float(line[3])
					players[pid].hp = hp

					# you can have insta respawn deaths where the person doesn't go down to 0, happens a couple times a night, caught by MOV hopefully
					# also deaths like 2 jaunts up probably aren't counted
					if hp == 0 and players[pid].lasthp != 0  and (ms - players[pid].lastdeath) > 14000:
						players[pid].death = 1
						players[pid].lastdeath = ms
						players[pid].deathtotal = players[pid].deathtotal + 1
					players[pid].lasthp = hp

				elif action == "FX":
					action = next((substring for substring in atk.keys() if substring in line[5]), None)
					if action is not None:
						if any(substring for substring in preverse if substring in line[5]):
							players[pid].reverse = True
						players[pid].action = atk[action]

					# gather check
					if (any(substring for substring in gatherbuffs if substring in line[5]) and
						t - lastgather[players[pid].team] > 30 and t > 10):
						gatherplayercount[players[pid].team] += 1 # inc number of teammates hit
						if gatherplayercount[players[pid].team] == 4: # if you hit at least 4 teammates
							gathertimes[players[pid].team].append(t)
							lastgather[players[pid].team] = t



				elif action == "TARGET" and players[pid].action != '':
					if line[3] == 'ENT':
						tid = int(line[4])
						if tid != pid and tid in player_ids: # if target is a player
							players[pid].target = players[tid].name

							if players[pid].team != players[tid].team and players[pid].action not in utility and not players[pid].reverse:
								if pid == 28 and players[pid].action == '':
									print(count)
								players[tid].targetcount(t, pid, players,players[pid].action)
							elif players[pid].reverse:
								players[tid].target = players[pid].name
								players[tid].action = players[pid].action
								players[pid].action = ''
								players[pid].target = ''
								players[pid].reverse = False
								if players[pid].team != players[tid].team:
									players[pid].targetcount(t, tid, players,players[tid].action)
							else:
								if players[pid].action in heals:
									players[pid].healcount(t, players[tid])

					elif line[3] == 'POS':
						if players[pid].action == 'jaunt': # catch cases where you jaunt off 1 attack
							players[pid].lastjaunt = t
							players[pid].jauntoffone(t)
						players[pid].target = '!pos'
						writeline = True

				elif action == "PREVTARGET":
					writeline = True
					

				elif action == "MOV":
					mov = line[3]

					# this should hopefully catch most insta-respawn deaths w/o hp = 0
					if mov == 'PLAYER_HITDEATH' and players[pid].lasthp != 0 and (ms - players[pid].lastdeath) > 14000:
						players[pid].death = 1
						players[pid].lastdeath = ms
						players[pid].deathtotal = players[pid].deathtotal + 1
						players[pid].hp = 0
						players[pid].lasthp = 0

					# think this may be more accurate than the FX crey
					# doesn't catch villain crey yet
					if 'DRAW_PISTOL' in mov or 'DRAW_WEAPONBACK' in mov: # WEAPONBACK might be shared with some other sets
						players[pid].crey = players[pid].crey + 1
						players[pid].action = 'crey pistol'
					# if 'WALL' in mov and players[pid].action == '':
					# 	players[pid].action = 'ssj'

					elif 'EMOTE' in mov: # WEAPONBACK might be shared with some other sets
						players[pid].emote = players[pid].emote + 1
						players[pid].action = 'emote'
						emotecheck += 1

			line = shlex.split(fp.readline().replace('\\','').replace('\'','').replace('\"',''))
			count = count + 1




for pid in player_ids: # clean up, if target at end of match
	if players[pid].istarget:
		players[pid].resettargetcount(players)

with open(sys.argv[1]+'.csv','a',newline='') as csvfile:
	csvw = csv.writer(csvfile, delimiter=',')
	for key, p in players.items(): # append stats
		# start and end points for time graphing
		csv_line = [0,p.name,'',0]
		csvw.writerow(csv_line)
		csv_line = [matchtime,p.name,'',0]
		csvw.writerow(csv_line)

		csv_line = [t,p.name,'','',p.team,'on target',p.ontarget]
		csvw.writerow(csv_line)
		csv_line = [t,p.name,'','',p.team,'first',p.first]
		csvw.writerow(csv_line)
		csv_line = [t,p.name,'','',p.team,'attack timing avg',str(sum(p.spiketiming) / max(len(p.spiketiming), 1))[:4]]
		csvw.writerow(csv_line)
		divontarget = max(p.ontarget,1)
		csv_line = [t,p.name,'','',p.team,'atk per spike avg',p.attacks / divontarget]
		csvw.writerow(csv_line)

	for gathertime in gathertimes['BLU']:
		csv_line = [gathertime,'','','','BLU','gather']
		csvw.writerow(csv_line)		
	for gathertime in gathertimes['RED']:
		csv_line = [gathertime,'','','','RED','gather']
		csvw.writerow(csv_line)		

print("\ndemo time " + str(round((t+starttime/1000)/60,2)) + " minutes")
print("map: " + match_map)

score1 = 0
clean1 = 0
score2 = 0
clean2 = 0
targets1 = 0
targets2 = 0


def print_table(headers, content):
	first_red = True
	header_str = ' | '.join([i.center(8) for i in headers])
	print(header_str)
	print('|'.join([('-' * len(i)) for i in header_str.split('|')]))

	for row in content:
		if first_red and '[RED]' in row[0]:
			print('|'.join([('-' * len(i)) for i in header_str.split('|')]))
			first_red = False
		print(' | '.join([str(i).center(8) for i in row]))

	print('')

offence_headers = ['team', '{:<20}'.format('name'), 'deaths', 'targeted', '', 'ontarget', '', 'timing', 'first', 'apspike']
offence_content = []
healer_headers = ['team', '{:<20}'.format('name'), 'ontarget', 'timing', 'topups', "AP's", 'predicts']
healer_content = []


for p in sorted(players.values(), key=lambda i: i.team):
	if p.team == 'BLU':
		score2 = score2 + p.deathtotal
		clean2 = clean2 + p.cleanspiked
		targets2 = targets2 + p.targeted
	else:
		score1 = score1 + p.deathtotal
		clean1 = clean1 + p.cleanspiked
		targets1 = targets1 + p.targeted

	offence_content.append([
		"[" + p.team + "]",
		'{:<20}'.format(p.name),
		p.deathtotal,
		p.targeted,
		p.cleanspiked,
		p.ontarget,
		p.late,
		str(sum(p.spiketiming) / max(len(p.spiketiming), 1))[:4],
		p.first,
		str(p.attacks / max(p.ontarget, 1))[:4]
	])

	if p.ontargetheals or p.topups:
		healer_content.append([
			"[" + p.team + "]",
			'{:<20}'.format(p.name),
			p.ontargetheals,
			str(sum(p.healtiming) / max(len(p.healtiming), 1))[:4],
			p.topups,
			p.aps,
			p.predicts
		])

print_table(offence_headers, offence_content)
print_table(healer_headers, healer_content)

print("")
print("SCORE: " + str(score1) + "-" + str(score2))
print("TARGETS CALLED: " + str(targets1) + "-" + str(targets2))
# print('CLEAN SPIKES: ' + str(clean1) + '-' + str(clean2))
if emotecheck > 0:
	print('CHECK EMOTES: ' + str(emotecheck) + ' were used')
