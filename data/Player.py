from data.powers import absorbs
from data.powers import primaryattacks
from data.config import *
from data.Target import Target
import math


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
		self.lastdeath = -14000
		self.maxhp = 0.0

		self.crey = 0
		self.emote = 0

		self.action = ''
		self.target = ''
		self.targetteam = ''
		self.reverse = False

		self.set1 = False
		self.set2 = False
		self.at = ''

		# being spiked
		self.targetstart = -1
		self.attackcounter = 0
		self.primaryattackcounter = 0
		self.targetattackers = []
		self.targeted = 0
		self.targetlock = False
		self.targetinstance = 0
		self.cleanspiked = 0
		self.absorbed = [] # List[[time, pid]] where time is when the absorb was placed, pid was the player who placed it

		# new spike count system
		self.recentattacks = [] # [t,aid,action]
		self.recentprimaryattacks = []
		self.lastjaunt = False
		self.istarget = False
		self.ontarget = 0
		self.resets = 0
		self.lastresdebuff = False

		self.dmgtaken = 0
		self.healreceived = 0
		self.totaldmgtaken = 0
		self.totalhprecovered = 0
		self.totalhealsreceived = 0
		self.totalhealsreceivedontarget = 0

		self.totalearlyjaunts = 0
		self.totalearlyphases = 0

		self.targethp = []
		self.misseddead = 0 # targets missed while dead


		# spiking someone else
		self.ontime = 0
		self.late = 0
		self.spiketiming = []
		self.attacks = 0
		self.attackstotal = 0
		self.first = 0
		self.healedby = []

		# healing peeps
		self.ontargetheals = 0
		self.healtiming = []
		self.topups = 0
		self.aps = 0 # absorb pain
		self.predicts = 0 # predicted the spike target and gave an absorb

		self.healalpha = 0
		self.healontime = 0
		self.heallate = 0
		self.healontarget = 0


		self.targetheals = []
		self.targetevades = []

		self.greens = 20 # assumes all slots greens
		self.greensavailable = 20 # assumes all slots greens

		self.support = False

		self.stats = {}
		self.atkchains = {}

	def reset(self):
		self.hp = ''
		self.action = ''
		self.target = ''
		self.targetteam = ''
		self.death = ''
		self.reverse = False
		self.targetinstance = 0

	def _update_ontarget(self, t, aid, players):
		timing = (t - self.targetstart)
		players[aid].spiketiming.append(timing)
		players[aid].ontarget += 1

	def isrecent(self,time,attacktime):
		t = time-attacktime
		if self.istarget:
			window = targetmaxtime
		else:
			window = targetwindow
		if t < window:
			return True
		else:
			return False

	def endtarget(self,players,spikes):
		players[self.targetattackers[0]].first += 1
		for atk in self.recentattacks:
			players[atk[1]].attacks += 1
		for aid in self.targetattackers:
			timing = matchtime # large number to catch error in output
			atkchain = ''
			for atk in self.recentattacks:
				if atk[1] == aid:
					timing = min(timing,atk[0]) # update attacker timing for avg
					atkchain += atk[2]+' - ' # change atk chain to string
			atkchain = atkchain[:-3]
			if atkchain in players[aid].atkchains.keys():
				players[aid].atkchains[atkchain] += 1
			else:
				players[aid].atkchains[atkchain] = 1

			self._update_ontarget(timing, aid, players)

		# new spike
		spikes.append(Target(self.name,self.team,self.targetstart))

		# spike data
		spikes[-1].attacks = self.recentattacks[:]
		spikes[-1].attackers = self.targetattackers[:]
		spikes[-1].heals = self.targetheals[:]
		spikes[-1].evades = self.targetevades[:]
		spikes[-1].hp = self.targethp[:]
		spikes[-1].spiketime = self.targetstart - self.recentattacks[-1][0]
		spikes[-1].debufftime = self.lastresdebuff
		if self.death == 1:
			spikes[-1].spikedeath = self.lastdeath/1000 - self.targetstart
		if self.lasthp == 0:
			spikes[-1].death = 1

		# spike summary
		spikes[-1].stats['atks before evade'] = ''
		if len(self.targetevades) > 0:
			atkb4evade = 0
			for atk in self.recentattacks:
				if self.targetevades[0][0] > atk[0]:
					atkb4evade += 1
			if (atkb4evade <= earlyevadecount or self.targetevades[0][0] < earlyevadetime):
				if (self.targetevades[0][2] == 'phase' or self.targetevades[0][2] == 'hibernate'):
					self.totalearlyphases  += 1
				elif (self.targetevades[0][2] == 'jaunt' ): #or self.targetevades[0][2] == 'translocation'
					self.totalearlyjaunts  += 1
				
			
			spikes[-1].stats['atks before evade'] = atkb4evade
		spikes[-1].stats['attackers'] = len(self.targetattackers)
		spikes[-1].stats['attacks'] = len(self.recentattacks)
		healsreceived = 0
		# to not count greens
		for h in self.targetheals:
			if h[1] != 'green':
				healsreceived += 1
		spikes[-1].stats['heals received'] = healsreceived
		spikes[-1].stats['greens available'] = self.greensavailable # at the start of the spike
		spikes[-1].stats['greens used'] = self.greensavailable - self.greens
		spikes[-1].stats['spike duration'] = self.recentattacks[-1][0] - self.targetstart
		spikes[-1].stats['total dmg lost'] = self.dmgtaken
		spikes[-1].stats['total hp recovered'] = self.healreceived
		spikes[-1].stats['hp after spike'] = self.lasthp

		for p in players.values(): # count num spikes missed if dead
			if p.team != self.team:
				lastdeath = p.lastdeath/1000
				respawn = math.ceil((lastdeath-1)/15)*15+15 # 1 sec safety, includes 15 sec uneffecting
				if lastdeath < self.targetstart and self.recentattacks[-1][0] < respawn:
					p.misseddead += 1


		self.targetstart = False # restart timer
		self.recentattacks = []
		self.recentprimaryattacks = []
		self.targetattackers = []
		self.healedby = []
		self.targetheals = []
		self.targethp = []
		self.dmgtaken = 0
		self.healreceived = 0
		# self.targetevades = [] # reset handled in the preevade lines
		self.lastresdebuff = False
		self.istarget = False

	def inittarget(self,t,players):
		self.istarget = True
		self.targeted += 1
		self.targetinstance = 1 # for spreadsheet

		self.greensavailable = self.greens

		if len(self.recentprimaryattacks) > 0:
			self.targetstart = self.recentprimaryattacks[0][0]
		else:
			self.targetstart = self.recentattacks[0][0]

		# add all current attackers to list
		for atk in self.recentattacks:
			if atk[1] not in self.targetattackers:
				self.targetattackers.append(atk[1])

		# for spirit ward predicts
		for time, hid in self.absorbed:
			if (self.targetstart - time) < predictspiketime: # absorb was fired before the spike
				players[hid].predicts += 1
			self.absorbed = []

		self.targethp.append([t,self.lasthp])
		# determine preevades
		if len(self.targetevades) > 0:
			lastevade = self.targetevades[-1]
			self.targetevades = []
			if (t-lastevade[0] < targetwindow):
				self.targetevades.append(lastevade)

	def jauntoffone(self,t,players): # count as target if jaunt off single primary attack
		if not self.istarget and len(self.recentprimaryattacks) == 1 and (t-self.recentprimaryattacks[0][0]) <= targetwindow/2: # with 1 sec of atk
			self.inittarget(t,players)

	def targetcount(self,t,aid,players,action,spikes):
		players[aid].attackstotal += 1

		if self.istarget: # if already target
			self.recentattacks.append([t,aid,action]) # add the atk
			if action in primaryattacks:
				self.recentprimaryattacks.append([t,aid,action])
			for atk in self.recentattacks:
				if atk[1] not in self.targetattackers: # add the atkr if needed
						self.targetattackers.append(atk[1])
			

		if not self.istarget:
			self.recentattacks.append([t,aid,action]) # add the atk
			if action in primaryattacks:
				self.recentprimaryattacks.append([t,aid,action])
			

			self.recentattacks = [x for x in self.recentattacks if self.isrecent(t,x[0])] # remove recent attacks outside window
			self.recentprimaryattacks = [x for x in self.recentprimaryattacks if self.isrecent(t,x[0])]

			self.targetattackers = []
			for atk in self.recentattacks:
				if atk[1] not in self.targetattackers: # add the atkr if needed
					self.targetattackers.append(atk[1])
			if  (
				len(self.targetattackers) >= targetminattackers and not self.istarget and # at least 2 people on target and not already target
				(((2*len(self.recentprimaryattacks) + len(self.recentattacks))/2.9>= targetminattacks) # if min 2 primary attacks (weighted)
				# or (len(self.recentattacks) >= targetminattacks*2) # or if people throw at least 4x trash damage on someone i.e. 4 BBs on emp at same time
				or (len(self.recentprimaryattacks) == targetminattacks/2 and t-self.lastjaunt < targetwindow/2) # if jaunt slightly before primary atk activated				# or (len(self.recentprimaryattacks) >= targetminattacks-1 and len(self.recentattacks) >= targetminattacks+2) # if 1
				)):
				
				self.inittarget(t,players)



	def healcount(self, t, targetplayer,action):
		# todo
		# ignore if player dead
		# account for phases
		# account for jaunts?
		targetplayer.totalhealsreceived += 1
		if targetplayer.istarget:
			targetplayer.totalhealsreceivedontarget += 1
			targetplayer.targetheals.append([t,self.id,action])
			if self.id not in targetplayer.healedby:
				late = False
				if t- targetplayer.targetstart < targethealwindow or len(targetplayer.recentattacks)<3:
					self.healontime += 1
					if targetplayer.healedby == []:
						self.healalpha += 1
				elif t- targetplayer.targetstart > targethealwindow*2:
					self.heallate += 1 # counting extra late as topups
					late = True
				else:
					self.heallate += 1

				targetplayer.healedby.append(self.id)
				if not late: 
					self.healtiming.append(t-targetplayer.targetstart)
				self.healontarget += 1

			self.ontargetheals += 1

		else:
			self.topups += 1

		if self.action in absorbs:
			targetplayer.absorbed.append([t, self.id])