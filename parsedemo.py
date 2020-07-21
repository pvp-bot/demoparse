import csv
import shlex
import sys
import math
import powers

ms = 0          # time in ms
t = 0           # time in seconds
tick = 16        # tick rate to determine time stamps/time grouping

player_names = []
player_ids   = []
player_list = []
players = ''


pos_blue = [0,0] # red and blue are arbitrary, probably makes sense to be team 1 and 2
match_map = ""

crey = 'DRAW_PISTOL'

targetwindow = 4 # seconds
targetcooldown = 10 # seconds
targetminattacks = 3 # minimum ppl on target to count as attack
targetminattackers = 2 # minimum attacks on target to count as attack

headers = ['time','actor','hp','deaths','team','action','target']

def newSplit(value):
    lex = shlex.shlex(value)
    lex.quotes = "'"
    lex.whitespace_split = True
    lex.commenters = ''
    return list(lex)

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
			(self.attackcounter<targetminattacks and (t - self.targetstart) > targetwindow-2 and self.attackercounter < targetminattackers) # or previous attack was rogue damage from 1 person
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
	line = shlex.split(fp.readline().replace('\\','').replace('\'',''))
	count = 0

	# initializing line loop - players, teams, 
	while line and count < 20000:
		try:
			pid = int(line[1])
		except:
			pid = 0 # ignore special actors


		if line[2] == "Map":
			match_map = line[3]

		if line[2] == "NEW":
			if pid not in player_ids and line[3] not in powers.name_filter:
				player_ids.append(pid)
				player_list.append(Player(line[3],pid))
		
		try:
			line = shlex.split(fp.readline().replace('\\','').replace('\'',''))
		except:
			print(count)
		count = count + 1

	players = dict(zip(player_ids,player_list))
	
	# back to start of file
	fp.seek(0)
	count = 0
	line = shlex.split(fp.readline().replace('\\','').replace('\'',''))
	with open(sys.argv[1]+'.csv','w',newline='') as csvfile:
		csvw = csv.writer(csvfile, delimiter=',')
		csvw.writerow(headers)

	# main parsing loop
	while line:
		with open(sys.argv[1]+'.csv','a',newline='') as csvfile:
			csvw = csv.writer(csvfile, delimiter=',')
			# print(count)
			action = line[2]
			try:
				pid = int(line[1])
			except:
				pid = 0 # ignore special 

			# assign team id to player based on intial position
			# assumes demo record starts in the buff phase
			if action == "POS" and pid in player_ids and players[pid].team == '':
				if pos_blue == [0,0]:
					pos_blue = [float(line[3]),float(line[5])]
					players[pid].team = 'BLU'
				else:
					dist = math.sqrt( ((pos_blue[0]-float(line[3]))**2)+((pos_blue[1]-float(line[5]))**2) )
					if dist < 20:
						players[pid].team = 'BLU'
					else:
						players[pid].team = 'RED'
				# print("[" + str(players[pid].id) + "] " + "[TEAM " + str(players[pid].team) + "] "+ str(players[pid].name))


			try: # 
				if action == "HP" and pid in player_ids:
					hp  = float(line[3])
					players[pid].hp = hp
					if hp == 0 and players[pid].lasthp != 0:
						players[pid].death = 1
						players[pid].deathtotal = players[pid].deathtotal + 1
					players[pid].lasthp = hp

				elif action == "FX" and pid in player_ids:
					action = next(substring for substring in powers.plist if substring in line[5])
					if any(substring for substring in powers.preverse if substring in line[5]):
						players[pid].reverse = True
					if any(substring for substring in powers.pemp if substring in line[5]):
						players[pid].emp = True
					players[pid].action = powers.pdict[action]

				elif action == "TARGET" and players[pid].action != '':
					tid = int(line[4])
					if tid in player_ids:
						if tid != pid:
							if players[pid].reverse: # if the receiver is listed as the actor
								players[tid].target = players[pid].name
								players[tid].action = players[pid].action
								players[pid].action = ''
								players[pid].reverse = False
							else:
								players[pid].target = players[tid].name
							
							if players[pid].team != players[tid].team:
								players[tid].targetcount(t,pid)
								
				elif action == "MOV":
					if line[3] == crey:
						players[pid].crey = players[pid].crey + 1




			except:
				# print(count)
				pass

			ms = ms + int(line[0]) # running demo time
			t2 = round(ms*tick/1000)/tick # time in s rounded to the nearest server tick (manually set)
			
			if t2 > t:
				for key, p in players.items():
					csv_line = [t,p.name,p.hp,p.death,p.team,p.action,p.target]
					if p.hp != '' or p.death != '' or p.action  != '':
						csvw.writerow(csv_line)
					p.reset()
			t = t2
			line = shlex.split(fp.readline().replace('\\','').replace('\'',''))
			count = count + 1
		



print("")
print("demo time " + str(t) + " seconds")
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
