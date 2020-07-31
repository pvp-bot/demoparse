import csv
import shlex
import sys
import math
import numpy as np

from data.powers import atk, preverse, heals, npc, name_filter, buffs
from data.config import *
from data.Player import Player

ms = 0          # demo time in ms
t = 0           # demo time in seconds
tick = 16       # tick rate to determine time stamps/time grouping, not the actual server ticks

player_ids   = []
player_list  = []
players      = ''

match_map = ""
starttime = 0 # in seconds

headers = ['time','actor','hp','deaths','team','action','target','targeted']



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
		except:
			pid = 0 # ignore special actors like CAM
		if line[2] == "Map":
			match_map = line[3]
			match_map = match_map.split('/')[-1]
		if line[2] == "NEW":
			if pid not in player_ids and line[3] not in name_filter:
				player_ids.append(pid)
				player_list.append(Player(line[3],pid))
		if line[2] in npc and pid in player_ids: #
			del player_ids[-1]
			del player_list[-1]
		try:
			line = shlex.split(fp.readline().replace('\\','').replace('\'',''))
		except:
			print(count) # find broken lines
		if len(player_list) == 16: # assuming 8v8 at most
			print(f'found 16 players after {count} lines')
			break
		count = count + 1

	players = dict(zip(player_ids,player_list))




	# back to start of file
	fp.seek(0)
	count = 0
	line = shlex.split(fp.readline().replace('\\','').replace('\'',''))

	# loop for assigning teams
	# assumes at least 1 buff-type power is thrown in the match per person
	# also assumes no confused buffs thrown, hmmm
	num_players   = len(player_ids)
	count_players = 0
	buff_count	  = 0
	while line and count_players < num_players:
		try:
			pid = int(line[1])
		except:
			pid = 0 # ignore special
		action = line[2]

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
		except:
			pid = 0 # ignore special
		action = line[2]

		if action == 'POS' and pid in player_ids:
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

	# main parsing loop
	with open(sys.argv[1]+'.csv','a',newline='') as csvfile:
		csvw = csv.writer(csvfile, delimiter=',')
		while line and t < 600: # ignore data after match end
			ms = ms + int(line[0]) # running demo time
			t2 = round(ms*tick/1000)/tick # time in s rounded to the nearest server tick to organize data - user input tick
			if t2 > t:
				for key, p in players.items():
					csv_line = [t,p.name,p.hp,p.death,p.team,p.action,p.target,p.targetinstance]
					if p.hp != '' or p.death != '' or p.action  != '' or p.targetinstance == 1:
						csvw.writerow(csv_line)
					p.reset()
			t = t2
			action = line[2]

			try:
				pid = int(line[1])
			except:
				pid = 0 # ignore special


			if pid in players:
				if action == "POS" and players[pid].team == '':
					pass # todo use starting pos to get end of buff cycle

				elif action == "HP":
					hp  = float(line[3])
					players[pid].hp = hp

					# you can have insta respawn deaths where the person doesn't go down to 0, happens a couple times a night, caught by MOV hopefully
					# also deaths like 2 jaunts up probably aren't counted
					if hp == 0 and players[pid].lasthp != 0:
						players[pid].death = 1
						players[pid].deathtotal = players[pid].deathtotal + 1
					players[pid].lasthp = hp

				elif action == "FX":
					action = next((substring for substring in atk.keys() if substring in line[5]), None)
					if action is not None:
						if any(substring for substring in preverse if substring in line[5]):
							players[pid].reverse = True
						players[pid].action = atk[action]

				elif action == "TARGET" and line[3] == 'ENT' and players[pid].action != '':
					tid = int(line[4])
					if tid != pid and tid in player_ids: # if target is a player

						if players[pid].team != players[tid].team:
							players[tid].targetcount(t, pid, players)
						else:
							if players[pid].action in heals:
								players[pid].healcount(t, players[tid])

				elif action == 'PREVTARGET' and players[pid].reverse:
					# strangler, ssj etc are dumb
					aid = int(line[4])
					if aid in player_ids and aid != pid:
						players[aid].target = players[pid].name
						players[aid].action = players[pid].action

						if players[pid].team != players[aid].team:
							players[pid].targetcount(t, aid, players)

				elif action == "MOV":
					mov = line[3]

					# this should hopefully catch most insta-respawn deaths w/o hp = 0
					if mov == 'PLAYER_HITDEATH' and players[pid].lasthp != 0:
						players[pid].death = 1
						players[pid].deathtotal = players[pid].deathtotal + 1
						players[pid].hp = 0
						players[pid].lasthp = 0

					# think this may be more accurate than the FX crey
					# doesn't catch villain crey yet
					if mov == 'DRAW_PISTOL' or mov == 'A_DRAW_PISTOL':
						players[pid].crey = players[pid].crey + 1
						players[pid].action = 'crey pistol'


			line = shlex.split(fp.readline().replace('\\','').replace('\'',''))
			count = count + 1




print("\ndemo time " + str(round(t/60,2)) + " minutes")
print("map: " + match_map)

print('\nlegend:')
print(f'targeted: attacked by {targetminattacks} attacks spread across at least {targetminattackers} attackers in less than {targetwindow} seconds')
print(f'clean: same as targeted except over {cleanspike} seconds')
print(f'ontime: number of spikes joined within {cleanspike} seconds')
print(f'late: number of spikes joined after {cleanspike} seconds')
print(f'timing: average time joining in on a spike')
print(f'first: number of times player is the first to attack a target')
print(f'apspike: short for attacks per spike, the average number of attacks the player throws on target')
print('')

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

offence_headers = ['team', '{:<20}'.format('name'), 'deaths', 'targeted', 'clean', 'ontime', 'late', 'timing', 'first', 'apspike']
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
		p.ontime,
		p.late,
		str(sum(p.spiketiming) / max(len(p.spiketiming), 1))[:4],
		p.first,
		str(p.attacks / max(p.ontime + p.late, 1))[:4]
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
print('CLEAN SPIKES: ' + str(clean1) + '-' + str(clean2))
