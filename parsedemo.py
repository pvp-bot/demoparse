import csv
import shlex
import sys
import math
import numpy as np

from data.powers import *
from data.config import *
from data.Player import Player
from data.Target import Target
import data.override as override

def main():
	ms = 0          # demo time in ms
	t = 0           # demo time in seconds

	player_ids   = []
	player_list  = []
	players      = ''

	spikes      = []
	rogues      = []

	demoname = sys.argv[1].split('/')[-1].split('.')[0]
	match_map = ""
	starttime = 0 # in seconds

	header = ['demo','map','linetype']
	header_log = ['player','team','time (s)','hp','death','action','target','target_team','targeted','value','uid','stat1','stat2','stat3','stat4','stat5','stat6','stat7','stat8','stat9','stat10','stat11','stat12','stat13','stat14','stat15']
	header.extend(header_log)

	emotes = []

	lastgather = {'BLU':0,'RED':0}
	gatherplayercount = {'BLU':0,'RED':0}
	gathertimes = {'BLU':[],'RED':[]}

	with open(sys.argv[1],'r') as fp:

		# blank out csv if existing
		with open(sys.argv[1]+'.csv','w',newline='') as csvfile:
			csvw = csv.writer(csvfile, delimiter=',')
			csvw.writerow(header)

		line = shlex.split(fp.readline().replace('\\','').replace('\'',''))
		count = 0
		playerline = 0

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
				if match_map in map_aliases:
					match_map = map_aliases[match_map]
				else:
					match_map = match_map.split('_')[1].lower()
			if action == "Player":
				playerline = count
			if action == "NPC" and line[3] != 'FRK_45':
				player_ids = [i for i in player_ids if i != pid]
				player_list = [i for i in player_list if i.id != pid]
			if action == "NEW":
				if pid not in player_ids and line[3] not in name_filter:
					if count == playerline + 1:
						player_ids = [pid] + player_ids # if player is recording, they're first
						player_list = [Player(line[3],pid)] + player_list
					else:
						player_ids.append(pid)
						player_list.append(Player(line[3],pid))
					

			# read manual demo overrides
			if action == override.key:
				if line[3] == 'SCORE':
					override.score = [int(line[5]),int(line[4])]  # 0 0 OVERRIDE SCORE 0 1 (ex), numbers reversed since deaths not score
				elif line[3] == "PLAYERSWAP":
					override.playerswap.append(line[4]) # 0 0 OVERRIDE PLAYERSWAP ghostmaster
				elif line[3] == "TEAMSWAP": 
					override.teamswap = True # 0 0 OVERRIDE TEAMSWAP
				elif line[3] == "POWERSETS": 
					override.powersets[line[4]] = [line[5],line[6]] 
			if action in npc and pid in player_ids and line[3] != 'FRK_45': #
				del player_ids[-1]
				del player_list[-1]
			try:
				line = shlex.split(fp.readline().replace('\\','').replace('\'',''))
			except:
				print(f'{count} line error') # find broken lines
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
		
		team_groups = []
		for pid in player_ids:
			team_groups.append([pid])
		maxgroupsize = 0

		while line and maxgroupsize<math.floor(num_players/2): #assuming even number teams
			try:
				pid = int(line[1])
				action = line[2] # catches weird lines without anything on it
			except:
				pid = 0 # ignore special
				action = ''
			if action == 'FX' and pid in player_ids:
				if any(substring for substring in buffs if substring in line[5]):
					buff_count = count
			elif action == 'TARGET' and count < (buff_count+8) and pid in player_ids:
				tid = int(line[4]) # target player id
				if tid != pid and tid in player_ids:
					group1 = False
					group2 = False
					groupcount = 0
					for group in team_groups:
						if pid in group and tid not in group:
							group1 = groupcount
						elif tid in group and pid not in group:
							group2 = groupcount
						groupcount += 1
					g1 = min(group1,group2)
					g2 = max(group1,group2)
					if g1 != g2: # if a buff is thrown merge lists to first list
						team_groups[g1]+=team_groups[g2]
						del team_groups[g2]
						maxgroupsize = max(maxgroupsize,len(team_groups[g1]))
						
					
			elif action == 'PREVTARGET':
				buff_count = False

			count = count + 1
			line = shlex.split(fp.readline().replace('\\','').replace('\'',''))

		team1 = 'BLU'
		team2 = 'RED'
		teamremaining=''
		# if team swap override
		if override.teamswap:
			team1 = 'RED'
			team2 = 'BLU'

		for group in team_groups:
			if player_ids[0] in group:
				for pid in group:
					players[pid].team = team1 # think this reliably puts the recorder on BLU (if in buff phase)
				if len(group) < math.floor(num_players/2):
					teamremaining = team1
				else:
					teamremaining = team2
			elif len(group) == math.floor(num_players/2):
				for pid in group:
					players[pid].team = team2

		for key, p in players.items():
			if p.team == '':
				p.team = teamremaining

			# if playerswap override
			if p.name in override.playerswap:
				if p.team == team2:
					p.team = team1
				else:
					p.team = team2
			


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
		t_bundle = 0.0

		# ################################################ #
		# ################################################ #
		# MAIN PARSING LOOP ############################## # 
		# ################################################ #
		# ################################################ #

		with open(sys.argv[1]+'.csv','a',newline='') as csvfile:
			csvw = csv.writer(csvfile, delimiter=',')

			while line and t <= matchtime: # ignore data after match end with small buffer time
				ms = ms + int(line[0]) # running demo time
				t2 = (ms/1000) # to seconds
				
				for p in players.values():
					csv_log = [demoname,match_map,'log',p.name,p.team,t,p.hp,p.death,p.action,p.target,p.targetteam,p.targetinstance,count,lineuid]
					
					# dealing with stupid entangles (same fx as strangler hit)
					if p.action == 'strangler' and p.target != '': # hold half second to confirm no entangle
						p.csvhold = [t+0.25,csv_log[:]]
						# p.reset()
					if p.action == 'entangle': # cancel last strangler when entangle pops up
						p.csvhold = False

					# check end target each timestep
					if p.istarget and (p.death == 1 or (t2-p.targetstart >= targetmaxtime and t-p.recentattacks[-1][0] > targetcooldown)): # if we're over the target window
						p.endtarget(players,spikes)


					# if (p.death == 1 or p.action  != '' or p.target != '' or p.targetinstance == 1) and not p.csvhold:
					if p.writelog and not p.csvhold:
						csvw.writerow(csv_log)

						# keep track of extra
						if p.action != '' and (p.action not in heals or p.action == 'spirit ward') and p.action not in evade and p.action not in filterextras and t > extras_start:
							if p.action in p.supportextras.keys() and t>0:
								p.supportextras[p.action] += 1
							else:
								p.supportextras[p.action] = 1
						if p.action in heals and p.action != 'spirit ward' and t>0:
							p.healpowers[p.action] += 1
						if p.action in phases:
							p.lastphase = t
							if not p.istarget:
								rogues.append([t,p.id,p.action,p.id])
						if p.action == 'green' and not p.istarget:
							rogues.append([t,p.id,p.action,p.id])
						
						if (p.death == 1 and p.lastdeath != p.lastspikedeath):
							rogues.append([t,p.id,'death',p.id])

						if p.action in utilitycount:
							p.utilcount += 1 

						lineuid += 1 # for debugging
						p.reset()

				# more stupid entangle stuff
				for p in players.values():
					if p.csvhold and t > p.csvhold[0]:
						csvw.writerow(p.csvhold[1])
						p.csvhold = False
						p.reset()


				if t2 > t:
					gatherplayercount = {'BLU':0,'RED':0} # reset gather count on time inc

				# aggregate data by time type
				if t > 0:
					t_bundle += t2-t
				if t_bundle > t_bundle_step and t2<matchtime:
					# aggregate greens availability
					for p in players.values():
						csvw.writerow([demoname,match_map,'greens_log',p.name,p.team,math.floor(t2/t_bundle_step)*t_bundle_step,'','','','','','','',lineuid,p.greens])
					t_bundle = 0
				t = t2

				try:
					pid = int(line[1])
					action = line[2]
				except:
					pid = 0 # ignore special

				if pid in players:

					if action == "HP":
						hp  = float(line[3])
						players[pid].hp = hp

						# you can have insta respawn deaths where the person doesn't go down to 0, happens a couple times a night, caught by MOV hopefully
						# also deaths like 2 jaunts up probably aren't counted
						if hp == 0 and players[pid].lasthp != 0  and (ms - players[pid].lastdeath) > 14000: # 14 sec death cooldown
							players[pid].death = 1
							players[pid].lastdeath = ms
							players[pid].deathtotal = players[pid].deathtotal + 1
							players[pid].writelog = True

						players[pid].totaldmgtaken += min(0,hp-players[pid].lasthp)
						players[pid].totalhprecovered += max(0,hp-players[pid].lasthp)
						if players[pid].istarget:
							players[pid].totaldmgtakenonspike += min(0,hp-players[pid].lasthp)
							players[pid].dmgtaken += min(0,hp-players[pid].lasthp)
							players[pid].healreceived += max(0,hp-players[pid].lasthp)
							players[pid].targethp.append([t,hp])
						players[pid].lasthp = hp

					if action == "HPMAX":
						hp  = float(line[3])
						players[pid].maxhp = max(players[pid].maxhp,hp)



					elif action == "FX":
						action = next((substring for substring in fx.keys() if substring in line[5]), None)
						if action is not None:
							if any(substring for substring in preverse if substring in line[5]):
								players[pid].reverse = True
							players[pid].action = fx[action]
						else:
							players[pid].action = ''
							players[pid].target = ''


						# gather check
						if (any(substring for substring in gatherbuffs if substring in line[5]) and
							t - lastgather[players[pid].team] > 30 and t > 10):
							gatherplayercount[players[pid].team] += 1 # inc number of teammates hit
							if gatherplayercount[players[pid].team] == 4: # if you hit at least 4 teammates
								gathertimes[players[pid].team].append(t)
								lastgather[players[pid].team] = t

						# damresdebuff
						if resdebuff in line[5]:
							players[pid].painted = t
							if players[pid].istarget and not players[pid].lastresdebuff:
								players[pid].lastresdebuff = t
						if players[pid].action == 'green':
							if players[pid].istarget:
								players[pid].targetheals.append([t,pid,players[pid].action])
							players[pid].greens -= 1


						if players[pid].action in evade:
							players[pid].targetevades.append([t,pid,players[pid].action])


						# powerset determination
						if not players[pid].reverse:
							if not players[pid].set1:
								othercheck = next((substring for substring in otherfx.keys() if substring in line[5]), None)
								if othercheck:
									othercheck = otherfx[othercheck] 
								if players[pid].action in powersets:
									players[pid].set1 = powersets[players[pid].action]						
								elif othercheck in powersets:
									players[pid].set1 = powersets[othercheck]
							if not players[pid].set2:
								othercheck = next((substring for substring in otherfx.keys() if substring in line[5]), None)
								if othercheck:
									othercheck = otherfx[othercheck] 
								if players[pid].action in powersets and powersets[players[pid].action] != players[pid].set1:
									players[pid].set2 = powersets[players[pid].action]						
								elif othercheck in powersets and  powersets[othercheck] != players[pid].set1:
									players[pid].set2 = powersets[othercheck]






					elif action == "TARGET" and players[pid].action != '':
						if line[3] == 'ENT':
							tid = int(line[4])


							if players[pid].reverse and tid in players:
								players[tid].writelog = True
							else:
								players[pid].writelog = True

							if tid != pid and tid in player_ids: # if target is a player
								players[pid].target = players[tid].name
								players[pid].targetteam = players[tid].team

								if players[pid].team != players[tid].team and players[pid].action not in utility and not players[pid].reverse:
									players[tid].targetcount(t, pid, players,players[pid].action,spikes,rogues)
								elif players[pid].reverse:
									players[tid].target = players[pid].name
									players[tid].action = players[pid].action
									players[tid].targetteam = players[pid].team
									players[pid].action = ''
									players[pid].target = ''
									players[pid].reverse = False
									if players[pid].team != players[tid].team and players[tid].action not in utility:
										players[pid].targetcount(t, tid, players,players[tid].action,spikes,rogues)
									elif players[tid].action in heals and t>0:
										players[tid].healcount(t, players[pid],players[tid].action)
								else:
									if players[pid].action in heals and t>0:
										players[pid].healcount(t, players[tid],players[pid].action)


						elif line[3] == 'POS':
							if players[pid].action == 'jaunt': # catch cases where you jaunt off 1 attack
								players[pid].lastjaunt = t
								players[pid].jauntoffone(t,players)
							players[pid].target = '!pos'
							players[pid].writelog = True

						else:
							players[pid].target = ''
							players[pid].writelog = True
						
					# elif action == "PREVTARGET":
					# 	pass
						
					elif action == "POS":
						players[pid].pos = [line[3],line[4],line[5]] # x, z, y? 

					elif action == "MOV":
						mov = line[3]

						# this should hopefully catch most insta-respawn deaths w/o hp = 0
						if 'DEATH' in mov and players[pid].lasthp != 0 and (ms - players[pid].lastdeath) > 14000:
							players[pid].death = 1
							players[pid].lastdeath = ms
							players[pid].deathtotal = players[pid].deathtotal + 1
							
							# count hp loss when HP bar doesn't move
							players[pid].dmgtaken += min(0,0-players[pid].lasthp)
							players[pid].totaldmgtaken += min(0,0-players[pid].lasthp)
							if players[pid].istarget:
								players[pid].totaldmgtakenonspike += min(0,0-players[pid].lasthp)

							players[pid].hp = 0
							players[pid].lasthp = 0

						# think this may be more accurate than the FX crey
						# doesn't catch villain crey yet
						if 'DRAW_PISTOL' in mov or 'DRAW_WEAPONBACK' in mov: # WEAPONBACK might be shared with some other sets
							players[pid].crey = players[pid].crey + 1
							players[pid].action = 'crey pistol'
							players[pid].writelog = True
						# if 'WALL' in mov and players[pid].action == '':
						# 	players[pid].action = 'ssj'

						# add KBs to spike log
						if mov == 'PLAYERKNOCKBACK':
							players[pid].kbtime = t

						if 'EMOTE' in mov: # WEAPONBACK might be shared with some other sets
							emotes.append([players[pid].name,mov,t])

				line = shlex.split(fp.readline().replace('\\','').replace('\'','').replace('\"',''))
				count = count + 1

	for p in players.values(): # clean up, if target at end of match
		if p.istarget:
			p.endtarget(players,spikes)

		for heal in p.targetheals:
			players[heal[1]].topups += 1
		for atk in p.recentattacks:
			rogues.append([atk[0],atk[1],atk[2],p.id])

	# PRINT STATS TO CSV

	with open(sys.argv[1]+'.csv','a',newline='') as csvfile:
		csvw = csv.writer(csvfile, delimiter=',')
		for p in players.values(): # append stats
			csvw.writerow([demoname,match_map,'log',p.name,p.team,0,'',0,'','','',0,])
			csvw.writerow([demoname,match_map,'log',p.name,p.team,matchtime,'',0,'','','',0])
			csvw.writerow([demoname,match_map,'greens_log',p.name,p.team,0,'','','','','','','','',20])
			csvw.writerow([demoname,match_map,'greens_log',p.name,p.team,matchtime,'','','','','','','',lineuid,p.greens])
			csvw.writerow([demoname,match_map,'greens_log','','',0,'','','','','','','','',0])
			for stat, value in p.stats.items():
				csvw.writerow([demoname,match_map,'stats'     ,p.name,p.team,'','','',stat,'','','',value])
			for ac, count in p.atkchains.items():
				csvw.writerow([demoname,match_map,'atk_chains',p.name,p.team,'','','',ac,  '','','',count])
			# [demoname,match_map,'log',p.name,p.team,t,p.hp,p.death,p.action,p.target,p.targetteam,p.targetinstance,value,lineuid]


		for gathertime in gathertimes['BLU']:
			csvw.writerow([demoname,match_map,'gathers','','BLU',gathertime])		
		for gathertime in gathertimes['RED']:
			csvw.writerow([demoname,match_map,'gathers','','RED',gathertime])

		# 'rogues' to csv (attacks + greens not as target)
		for r in rogues:
			p1 = players[r[1]].name
			p2 = players[r[3]].name
			t1 = players[r[1]].team
			t2 = players[r[3]].team
			if p1 == p2:
				p2 = '-'
				t2 = '-'
			csvw.writerow([demoname,match_map,'rogue_log',p1,t1,r[0],'','',r[2],p2,t2,'','',''])

		suid = 1 # spike uid
		spikes.sort(key=lambda x: x.start) # sort spikes by start time

		for s in spikes:

			csvw.writerow([demoname,match_map,'spike_summary',s.target,s.team,round(s.start,1),round(s.stats['spike duration'],1),s.death,'','','',len(s.attacks),len(s.attackers),suid,s.stats['total hp lost']])

			# spike log data
			for act in s.attacks:
				act_time = round(act[0] - s.start,2)
				csvw.writerow([demoname,match_map,'spike_log',s.target,s.team,act_time,'',s.death,act[2],players[act[1]].name,players[act[1]].team,'','',suid])
			for act in s.heals:
				healer = players[act[1]].name
				if act[2] == 'green':
					healer = '+'
				act_time = round(act[0] - s.start,2)
				csvw.writerow([demoname,match_map,'spike_log',s.target,s.team,act_time,'',s.death,act[2],healer,players[act[1]].team,'','',suid])
			for act in s.evades:
				act_time = round(act[0] - s.start,2)
				csvw.writerow([demoname,match_map,'spike_log',s.target,s.team,act_time,'',s.death,act[2],'-',players[act[1]].team,'','',suid])
			if s.debufftime:
				debufftime = round(s.debufftime - s.start,2)
				if debufftime <= 0:
					csvw.writerow([demoname,match_map,'spike_log',s.target,s.team,debufftime,'',s.death,'-res painted','--','','','',suid])
				else:
					csvw.writerow([demoname,match_map,'spike_log',s.target,s.team,debufftime,'',s.death,'-res hit','--','','','',suid])
			if s.kbtime:
				kbtime = round(s.kbtime - s.start,2)
				csvw.writerow([demoname,match_map,'spike_log',s.target,s.team,kbtime,'',s.death,'knocked','!','','','',suid])
			if s.spikedeath:
				csvw.writerow([demoname,match_map,'spike_log',s.target,s.team,round(s.spikedeath,1),'',s.death,'death','x','','','',suid])
			
			# graphing spike hp
			if len(s.hp)>1:
				for hp in s.hp:
					hptime = round(hp[0]-s.start,2)
					csvw.writerow([demoname,match_map,'spike_hp',s.target,s.team,hptime,hp[1],s.death,'','','','','',suid])

			# spike stats
			for stat,value in s.stats.items():
				csvw.writerow([demoname,match_map,'spike_stats',s.target,s.team,'','',s.death,stat,'','','',value,suid])
			
			suid += 1 # spike uid



	# console output

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

	offence_headers = ['team', '{:<20}'.format('name'), 'deaths', 'targeted', 'survival', 'ontarget', 'otp', 'timing', 'variance','first', 'apspike']
	offence_content = []
	healer_headers = ['team', '{:<20}'.format('name'), 'on time', 'late','topups', 'alpha', 'timing','ontrgt%', 'ontime%','predicts','hpspike']
	healer_content = []


	deaths = {'BLU':0,'RED':0}
	targeted = {'BLU':0,'RED':0}
	for p in players.values():
		deaths[p.team] += p.deathtotal 
		targeted[p.team] += p.targeted
		if p.ontargetheals+p.topups > p.attacks/1.5 and p.ontargetheals > 4 and p.healontime > 0:
			p.support = True

		# setup player powersets in order
		if p.support:
			if p.set2 in primarysupport:
				set3 = p.set2
				p.set2 = p.set1
				p.set1 = set3
		else:
			if p.set2 in primaryoffence and p.set1 != 'poison':
				set3 = p.set2
				p.set2 = p.set1
				p.set1 = set3
		if not p.set1:
			p.set1 = '-'
		if not p.set2:
			p.set2 = '-'
		if p.name in override.powersets:
			p.set1 = override.powersets[p.name][0]
			p.set2 = override.powersets[p.name][1]


		p.at = p.set1+'/'+p.set2


	targets = {'BLU':targeted['RED'],'RED':targeted['BLU']}
	total_ontarget = {'BLU':0,'RED':0}
	total_attacks  = {'BLU':0,'RED':0}
	total_timing   = {'BLU':[],'RED':[]}

	with open(sys.argv[1]+'.csv','a',newline='') as csvfile:
		csvw = csv.writer(csvfile, delimiter=',')

		for p in sorted(players.values(), key=lambda i: i.team):
			targetteam = 'BLU'
			if p.team == 'BLU':
				targetteam = 'RED'

			spiketiming = sum(map(abs,p.spiketiming)) / max(len(p.spiketiming), 1)
			spiketimingvar = sum((x-spiketiming)**2 for x in p.spiketiming) / max(len(p.spiketiming),1)
			healtiming = sum(p.healtiming) / max(len(p.healtiming), 1)
			healtimingvar = sum((x-healtiming)**2 for x in p.healtiming) / max(len(p.healtiming),1)

			offence_content.append([
				"[" + p.team + "]",
				'{:<20}'.format(p.name),
				p.deathtotal,
				p.targeted,
				"{:.0%}".format(1-p.deathtotal/max(p.targeted,1)),
				p.ontarget,
				"{:.0%}".format(p.ontarget/max(targets[p.team],1)),
				str(spiketiming)[:4],
				str(spiketimingvar)[:4],
				p.first,
				str(p.attacks / max(p.ontarget, 1))[:4]
			])

			if p.ontargetheals > 0:
				hpspike =p.ontargetheals/(p.healontime+p.heallate)
				healer_content.append([
					"[" + p.team + "]",
					'{:<20}'.format(p.name),
					p.healontime,
					p.heallate,
					p.topups,
					p.healalpha,
					str(healtiming)[:4],
					"{:.0%}".format(p.healontarget/(targeted[p.team]-p.targeted),1),
					"{:.0%}".format(p.healontime/(targeted[p.team]-p.targeted),1),
					p.predicts,
					str(hpspike)[:4]

				])
			if p.support:
				csvw.writerow([demoname,match_map,'support_stats',p.name,p.team,'','','',p.set1,'',targetteam,'',  '',''      ,p.deathtotal,p.targeted,p.healontime,p.heallate,p.healfollowup,p.topups,p.healalpha,hpspike,healtiming,p.predicts,p.guesses,p.phaseheals,p.healmisseddead,targeted[p.team]])
				# if p.support:
				for extra, count in p.supportextras.items():
					csvw.writerow([demoname,match_map,'support_extras',p.name,p.team,'','','',p.set1,extra,targetteam,'',  '',''      ,count])
				healpowers = [demoname,match_map,'support_powers',p.name,p.team,'','','',p.set1,'',targetteam,'',  '','']
				for power, count in p.healpowers.items():
					healpowers.append(count)
				csvw.writerow(healpowers)
				csvw.writerow([demoname,match_map,'support_breakdown',p.name,p.team,'','','',p.set1,'on time',targetteam,'',  '',''      ,p.healontime])
				csvw.writerow([demoname,match_map,'support_breakdown',p.name,p.team,'','','',p.set1,'late',targetteam,'',  '',''      ,p.heallate])
				csvw.writerow([demoname,match_map,'support_breakdown',p.name,p.team,'','','',p.set1,'missed (dead)',targetteam,'',  '',''      ,p.healmisseddead])
				csvw.writerow([demoname,match_map,'support_breakdown',p.name,p.team,'','','',p.set1,'missed',targetteam,'',  '',''      ,targeted[p.team]-(p.healontime+p.heallate+p.healmisseddead)])

			
			# header_log = ['demo','map',   'linetype',    'playr','team',t, hp d  a  tgt tt tgtd,'value','uid','stat1','stat2','stat3','stat4','stat5',stat6,stat7,stat8,...]
			csvw.writerow([demoname,match_map,'summary_stats',p.name,p.team,'','','',p.at,'',targetteam,'',  '',''      ,p.deathtotal,p.targeted,1-p.deathtotal/max(p.targeted,1) if p.targeted > 0 else '',p.ontarget/targets[p.team] if p.ontarget > 0 else '',p.healontarget/(targeted[p.team]-p.targeted) if p.healontarget > 0 else '',p.attackstotal,p.healstotal,p.utilcount]) 
			csvw.writerow([demoname,match_map,'offence_stats',p.name,p.team,'','','','','', targetteam,'',  '',''      ,p.deathtotal,p.targeted,p.ontarget,p.ontarget/max(targets[p.team],1),spiketiming,p.attacks / max(p.ontarget, 1),p.first,targets[p.team]-p.ontarget, p.misseddead, p.attacks, p.attackstotal-p.attacks,round(sum(p.followuptiming)/max(len(p.followuptiming),1),2),p.lateatks])
			csvw.writerow([demoname,match_map,'defence_stats',p.name,p.team,'','','','','', targetteam,'',  '',''      ,p.deathtotal,p.targeted,-p.totaldmgtakenonspike,p.totalhealsreceivedontarget,p.totalhealsreceived,p.totalearlyphases,p.totalearlyjaunts,-p.totaldmgtaken,20-p.greens,p.dmgtakensurv])
			
			total_attacks[p.team]  += p.attacks
			total_ontarget[p.team] += p.ontarget
			total_timing[p.team].extend(p.spiketiming)

		# fix missing deaths in the score line
		deaths['RED'] += override.score[1]
		deaths['BLU'] += override.score[0]

		csvw.writerow([demoname,match_map,'summary','','','','','','score','', '','',  '',''      			,deaths['RED'],deaths['BLU']])
		csvw.writerow([demoname,match_map,'summary','','','','','','targets called','', '','',  '',''      	,targets['BLU'],targets['RED']])
		csvw.writerow([demoname,match_map,'summary','','','','','','avg on target','', '','',  '',''      	,round(total_ontarget['BLU']/max(targets['BLU'],1),1),round(total_ontarget['RED']/max(targets['RED'],1),1)])
		csvw.writerow([demoname,match_map,'summary','','','','','','atk per target','', '','',  '',''      	,round(total_attacks['BLU']/max(targets['BLU'],1),1),round(total_attacks['RED']/max(targets['RED'],1),1)])
		csvw.writerow([demoname,match_map,'summary','','','','','','avg atk timing','', '','',  '',''      	,round(sum(total_timing['BLU'])/max(len(total_timing['BLU']),1),2),round(sum(total_timing['RED'])/max(len(total_timing['RED']),1),2)])

	print_table(offence_headers, offence_content)
	print_table(healer_headers, healer_content)

	print("SCORE: " + str(deaths['RED']) + "-" + str(deaths['BLU']))
	print("TARGETS CALLED: " + str(targets['BLU']) + "-" + str(targets['RED']))
	if len(emotes) > 0:
		print('CHECK EMOTES: ')
		print(emotes)

	return True

if __name__ == "__main__":
    main()