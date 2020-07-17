import csv
import shlex
import sys
import math

ms = 0          # time in ms
t = 0           # time in seconds
tick = 8        # tick rate to determine time stamps

player_names = []
player_ids   = []
name_filter  = ['Mu Guardian','Phantasm','Decoy Phantasm','Decoy','Coralax Blue Hybrid','Dr','Poison Trap','Decoy','Animated Stone','Superior Vigilant Assault','Blind','Galvanic Sentinel','Voltaic Geyser','Voltaic Sentinel','Water Spout']

pos_blue = [0,0] # red and blue are arbitrary, probably makes sense to be team 1 and 2
pos_red  = [0,0]
score    = [0,0]

with open(sys.argv[1],'r') as fp:
	line = shlex.split(fp.readline())
	count = 0
	while line and count < 50000:
		ms = ms + int(line[0]) # running demo time
		t = round(ms*tick/1000)/tick # time in s rounded to the nearest server tick (manually set)

		if len(line) > 0 and line[2] == "NEW":
			if line[3] not in player_names and line[3] not in name_filter:
				player_ids.append(line[1])
				player_names.append(line[3])

		# assign team id to player based on intial position - 
		if line[2] == "POS" and line[1] in player_ids: # and team[player].id not assigned
			if pos_blue == [0,0]:
				pos_blue = [line[3],line[5]]
			else:
				dist = math.sqrt( ((float(pos_blue[0])-float(line[3]))**2)+((float(pos_blue[1])-float(line[5]))**2) )
				if dist < 20:
					pass # team[playerid] = blue
				else:
					pass # team[playerid] = red

		# if line[2] == "HP":
		#	player[id].hp  = float(line[3])
		#	if player.hp == 0
		#		team.deaths = team.deaths + 1
		#		player.deaths = player.deaths + 1
		
		line = shlex.split(fp.readline()) #next line
		count = count + 1

players = dict(zip(player_ids,player_names))
print(players)
