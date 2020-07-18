import csv
import shlex
import sys
import math
import powers

ms = 0          # time in ms
t = 0           # time in seconds
tick = 8        # tick rate to determine time stamps/time grouping

player_names = []
player_ids   = []
player_list = []
players = ''
name_filter  = ['Mu Guardian','Phantasm','Decoy Phantasm','Decoy','Coralax Blue Hybrid','Dr','Poison Trap','Decoy','Animated Stone','Superior Vigilant Assault','Blind','Galvanic Sentinel','Voltaic Geyser','Voltaic Sentinel','Water Spout']

pos_blue = [0,0] # red and blue are arbitrary, probably makes sense to be team 1 and 2
score    = [0,0]
match_map = ""

headers = ['time','actor','hp','deaths','team','action','target']

class Player:
	def __init__(self, name, pid):
		self.name = name
		self.id = pid
		self.team = ''
		self.deaths = 0
		self.hp = ''
		self.maxhp = 0.0
		self.lasthp = 0.0
		self.action = ''
		self.target = ''
	def reset(self):
		self.hp = ''
		self.action = ''
		self.target = ''

with open(sys.argv[1],'r') as fp:
	line = shlex.split(fp.readline().replace('\\',''))
	count = 0

	# initializing line loop
	while line and count < 20000:
		try:
			pid = int(line[1])
		except:
			pid = 0 # ignore special actors


		if line[2] == "Map":
			match_map = line[3]

		if line[2] == "NEW":
			if pid not in player_ids and line[3] not in name_filter:
				player_ids.append(pid)
				player_list.append(Player(line[3],pid))
		
		try:
			line = shlex.split(fp.readline()) #next line
		except:
			print(count)
		count = count + 1

	players = dict(zip(player_ids,player_list))
	
	# back to start of file
	fp.seek(0)
	count = 0
	line = shlex.split(fp.readline().replace('\\',''))
	with open(sys.argv[2],'w',newline='') as csvfile:
		csvw = csv.writer(csvfile, delimiter=',')
		csvw.writerow(headers)

	# main parsing loop
	while line:
		with open(sys.argv[2],'a',newline='') as csvfile:
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
					players[pid].team = 1
				else:
					dist = math.sqrt( ((pos_blue[0]-float(line[3]))**2)+((pos_blue[1]-float(line[5]))**2) )
					if dist < 20:
						players[pid].team = 1
					else:
						players[pid].team = 2
				# print("[" + str(players[pid].id) + "] " + "[TEAM " + str(players[pid].team) + "] "+ str(players[pid].name))


			try: # 
				if action == "HP" and pid in player_ids:
					hp  = float(line[3])
					if players[pid].lasthp != hp:
						players[pid].hp = hp
					if hp == 0:
						players[pid].deaths = players[pid].deaths + 1

				elif action == "FX" and line[3] == "OneShot" and pid in player_ids:
					action = next(substring for substring in powers.plist if substring in line[5])
					players[pid].action = powers.pdict[action]

				elif action == "TARGET" and players[pid].action != '':
					targ = int(line[4])
					if targ in player_ids:
						if targ != pid:
							players[pid].target = players[int(targ)].name
					else:
						players[pid].target = targ


			except:
				# print(count)
				pass

			ms = ms + int(line[0]) # running demo time
			t2 = round(ms*tick/1000)/tick # time in s rounded to the nearest server tick (manually set)
			
			if t2 > t:
				for key, p in players.items():
					csv_line = [t,p.name,p.hp,p.deaths,p.team,p.action,p.target]
					csvw.writerow(csv_line)
					p.reset()
			t = t2
			line = shlex.split(fp.readline().replace('\\','')) #next line
			count = count + 1
		



print("")
print("demo time " + str(t) + " seconds")
print("map: " + match_map)
print("")

score1 = 0
score2 = 0
for key, p in players.items():
	if p.team == 1:
		score2 = score2 + p.deaths
	else:
		score1 = score1 + p.deaths
	print("[TEAM " + str(p.team) + "]"+"[PID "+str(p.id)+"] " + p.name + " deaths: " + str(p.deaths))
	
print("")
print("SCORE: " + str(score1) + "-" + str(score2))
