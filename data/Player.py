from data.powers import absorbs
from data.powers import primaryattacks
from data.config import *
from data.Target import Target


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
		self.recentattacks = []
		self.recentprimaryattacks = []
		self.lastjaunt = False
		self.istarget = False
		self.ontarget = 0
		self.resets = 0
		self.lastresdebuff = False


		# spiking someone else
		self.ontime = 0
		self.late = 0
		self.spiketiming = []
		self.attacks = 0
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

	def endtarget(self, players,spikes):
		players[self.targetattackers[0]].first += 1
		for atk in self.recentattacks:
			players[atk[1]].attacks += 1
		for aid in self.targetattackers:
			timing = matchtime # large number to catch error in output
			for atk in self.recentattacks:
				if atk[1] == aid:
					timing = min(timing,atk[0])
			self._update_ontarget(timing, aid, players)

		# spike data
		spikes.append(Target(self.name,self.team,self.targetstart))
		spikes[-1].attacks = self.recentattacks[:]
		spikes[-1].attackers = self.recentattacks[:]
		spikes[-1].heals = self.targetheals[:]
		spikes[-1].evades = self.targetevades[:]
		spikes[-1].greensavailable = self.greensavailable
		spikes[-1].greensused = self.greensavailable - self.greens
		spikes[-1].spiketime = self.targetstart - self.recentattacks[-1][0]
		spikes[-1].debufftime = self.lastresdebuff
		if self.lasthp == 0:
			spikes[-1].death = 1

		self.targetstart = False # restart timer
		self.recentattacks = []
		self.recentprimaryattacks = []
		self.targetattackers = []
		self.healedby = []
		self.targetheals = []
		self.targetevades = []
		self.lastresdebuff = False
		self.istarget = False

	def inittarget(self,players):
		self.istarget = True
		self.targeted += 1
		self.targetinstance = 1 # for spreadsheet

		self.greensavailable = self.greens

		if len(self.recentprimaryattacks) > 0:
			self.targetstart = self.recentprimaryattacks[0][0]
		else:
			self.targetstart = self.recentattacks[0][0]

		for atk in self.recentattacks:
			if atk[1] not in self.targetattackers:
				self.targetattackers.append(atk[1])

		for time, hid in self.absorbed:
			if (self.targetstart - time) < predictspiketime: # absorb was fired before the spike
				players[hid].predicts += 1
			self.absorbed = []

	def jauntoffone(self,t,players): # count as target if jaunt off single primary attack
		if not self.istarget and len(self.recentprimaryattacks) == 1 and (t-self.recentprimaryattacks[0][0]) <= targetwindow: # with 1 sec of atk
			self.inittarget(players)

	def targetcount(self,t,aid,players,action,spikes):
		if self.istarget: # if already target
			if t-self.targetstart >= targetmaxtime or t-self.recentattacks[-1][0] > targetcooldown: # if we're over the max target window or it's been long enough since the last attack
				self.endtarget(players,spikes)
			else:
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
				
				self.inittarget(players)



	def healcount(self, t, targetplayer,action):
		# todo
		# ignore if player dead
		# account for phases
		# account for jaunts?
		if targetplayer.istarget:
			targetplayer.targetheals.append([t,self.id,action])
			if self.id not in targetplayer.healedby:
				late = False
				if t- targetplayer.targetstart < targethealwindow or len(targetplayer.recentattacks)<4:
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