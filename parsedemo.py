import csv
import shlex
import sys
import math
import powers

ms = 0          # demo time in ms
t = 0           # demo time in seconds
tick = 16       # tick rate to determine time stamps/time grouping, not the actual server ticks

player_ids   = []
player_list  = []
players      = ''

match_map = ""

# in seconds
targetwindow = 4   # time window for min attacks to count a spike 
targetcooldown = 8 # time after spike started to ignore new attacks as a spike
targetminattacks = 3   # minimum atks on target to count as attack
targetminattackers = 2 # minimum ppl on target to count as attack
# getting good numbers comparing to vods with these values

headers = ['time','actor','hp','deaths','team','action','target']

class Player:
	def __init__(self, name, pid):
		self.name = name
		self.id = pid
		self.team = ''
		self.death = ''
		self.hp = ''
		self.hp = 0
		self.lasthp = 0
		self.deathtotal = 0
		self.maxhp = 0.0

		self.crey = 0
		
		self.action = ''
		self.target = ''
		self.reverse = False
		self.emp = False	

		self.targetstart = -1
		self.targetcooldown = 0
		self.attackcounter = 0
		self.attackercounter = 0
		self.targetattackers = []
		self.targeted = 0
		self.targetlock = False

	def reset(self):
		self.hp = ''
		self.action = ''
		self.target = ''
		self.death = ''
		self.reverse = False

	def targetcount(self, t, aid):
		if (self.targetstart == -1 or 					# first target
			(t - self.targetstart) > targetcooldown or	# cooldown timer has elapsed
			(self.attackcounter<targetminattacks and (t - self.targetstart) > targetwindow and self.attackercounter < targetminattackers and not self.targetlock) # or previous attack was rogue damage from 1 person
			): 
			self.targetstart = t #start timer
			self.attackcounter = 0
			self.targetattackers = []
			self.targetlock = False

		# print(self.attackcounter)
		if (t - self.targetstart) < targetwindow and not self.targetlock: #if within targeting window
			self.attackcounter = self.attackcounter + 1 #increase the #attacks on
			if aid not in self.targetattackers:
				self.targetattackers.append(aid) #add the actor to the attacker list
				self.attackercounter = self.attackercounter + 1 #increment the #attackers on target
			if self.attackcounter >= targetminattacks and self.attackercounter >= targetminattackers:
				self.targeted = self.targeted + 1
				self.targetlock = True






with open(sys.argv[1],'r') as fp:

	# blank out csv if existing
	with open(sys.argv[1]+'.csv','w',newline='') as csvfile:
		csvw = csv.writer(csvfile, delimiter=',')
		csvw.writerow(headers)

	line = shlex.split(fp.readline().replace('\\','').replace('\'',''))
	count = 0

	# initializing line loop - players, teams, 
	while line and count < 10000: # 10k should be enough to find all players
		try:
			pid = int(line[1]) # player ID
		except:
			pid = 0 # ignore special actors like CAM
		if line[2] == "Map":
			match_map = line[3]
			match_map = match_map.split('/')[-1]
		if line[2] == "NEW":
			if pid not in player_ids and line[3] not in powers.name_filter:
				player_ids.append(pid)
				player_list.append(Player(line[3],pid))
		if line[2] in powers.npc and pid in player_ids: # don't count self if recording from obs
		# if line[2] in powers.npc "NPC" and pid in player_ids: # don't count self if recording from obs
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
			if any(substring for substring in powers.buffs if substring in line[5]):
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
	count = 0
	line = shlex.split(fp.readline().replace('\\','').replace('\'',''))

	# main parsing loop
	with open(sys.argv[1]+'.csv','a',newline='') as csvfile:
		csvw = csv.writer(csvfile, delimiter=',')
		while line:
			ms = ms + int(line[0]) # running demo time
			t2 = round(ms*tick/1000)/tick # time in s rounded to the nearest server tick to organize data - user input tick
			if t2 > t:
				for key, p in players.items():
					csv_line = [t,p.name,p.hp,p.death,p.team,p.action,p.target]
					if p.hp != '' or p.death != '' or p.action  != '':
						csvw.writerow(csv_line)
					p.reset()
			t = t2
			action = line[2]

			try:
				pid = int(line[1])
			except:
				pid = 0 # ignore special 
	

			try: # 
				if action == "POS" and pid in player_ids and players[pid].team == '':
					pass # todo use starting pos to get end of buff cycle

				elif action == "HP" and pid in player_ids:
					hp  = float(line[3])
					players[pid].hp = hp
					
					# you can have insta respawn deaths where the person doesn't go down to 0, happens a couple times a night, caught by MOV hopefully
					# also deaths like 2 jaunts up probably aren't counted
					if hp == 0 and players[pid].lasthp != 0: 
						players[pid].death = 1
						players[pid].deathtotal = players[pid].deathtotal + 1
					players[pid].lasthp = hp

				elif action == "FX" and pid in player_ids:
					action = next(substring for substring in powers.pdict.keys() if substring in line[5])
					if any(substring for substring in powers.preverse if substring in line[5]):
						players[pid].reverse = True
					# if any(substring for substring in powers.pemp if substring in line[5]):
						# players[pid].emp = True
					players[pid].action = powers.pdict[action]

				elif action == "TARGET" and players[pid].action != '':
					tid = int(line[4])
					if tid in player_ids: # if target is a player
						if tid != pid: # if target is not actor
							if players[pid].reverse: # if the receiver is listed as the actor
								players[tid].target = players[pid].name #
								players[tid].action = players[pid].action
								players[pid].action = ''
								players[pid].target = ''
								players[pid].reverse = False
							else:
								players[pid].target = players[tid].name
							
							if players[pid].team != players[tid].team:
								players[tid].targetcount(t,pid)
								
				elif action == "MOV":
					mov = line[3]

					# this should hopefully catch most instarespawn deaths w/o hp = 0
					if mov == 'PLAYER_HITDEATH' and players[pid].lasthp != 0:
						players[pid].death = 1
						players[pid].deathtotal = players[pid].deathtotal + 1
					
					# think this may be more accurate than the FX crey
					# doesn't catch villain crey yet
					if mov == 'DRAW_PISTOL' or mov == 'A_DRAW_PISTOL':
						players[pid].crey = players[pid].crey + 1
						players[pid].action = 'crey pistol'




			except:
				# print(count)
				pass

			line = shlex.split(fp.readline().replace('\\','').replace('\'',''))
			count = count + 1
		



print("")
t_min = round(t/60,2)
print("demo time " + str(t_min) + " seconds")
print("map: " + match_map)
print("")

score1 = 0
score2 = 0
targets1 = 0
targets2 = 0
for key, p in players.items():
	if p.team == 'BLU':
		score2 = score2 + p.deathtotal
		targets2 = targets2 + p.targeted
	else:
		score1 = score1 + p.deathtotal
		targets1 = targets1 + p.targeted
	# print("[TEAM " + str(p.team) + "]"+"[PID "+str(p.id)+"] " + p.name + " deaths: " + str(p.deathtotal))
	print("[" + str(p.team) + "] "+ "{:<20}".format(p.name) + " deaths: " + "{:<8}".format(str(p.deathtotal))+ "targeted: " + str(p.targeted))
	
print("")
print("SCORE: " + str(score1) + "-" + str(score2))
print("TARGETS CALLED: " + str(targets1) + "-" + str(targets2))
