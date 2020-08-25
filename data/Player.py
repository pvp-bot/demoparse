from data.powers import absorbs
from data.powers import primaryattacks
from data.config import *

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
		self.reverse = False
		self.emp = False

		self.at = ''

		# being spiked
		self.targetstart = -1
		self.targetcooldown = 0
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

		self.poison = False
		self.emp = False

	def reset(self):
		self.hp = ''
		self.action = ''
		self.target = ''
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
			window = targetcooldown
		else:
			window = targetwindow

		if t < window:
			return True
		else:
			return False

	def resettargetcount(self, players):
		players[self.targetattackers[0]].first += 1
		for atk in self.recentattacks:
			players[atk[1]].attacks += 1
		for aid in self.targetattackers:
			timing = matchtime # large number to catch error in output
			for atk in self.recentattacks:
				if atk[1] == aid:
					timing = min(timing,atk[0])
			self._update_ontarget(timing, aid, players)

		self.targetstart = False # restart timer
		self.recentattacks = []
		self.recentprimaryattacks = []
		self.targetattackers = []
		self.istarget = False

	def inittarget(self):
		self.istarget = True
		self.targeted += 1
		self.targetinstance = 1 # for spreadsheet
		if len(self.recentprimaryattacks) > 0:
			self.targetstart = self.recentprimaryattacks[0][0]
		else:
			self.targetstart = self.recentattacks[0][0]
		for atk in self.recentattacks:
			if atk[1] not in self.targetattackers:
				self.targetattackers.append(atk[1])

	def jauntoffone(self,t): # count as target if jaunt off single primary attack
		if not self.istarget and len(self.recentprimaryattacks) == 1 and (t-self.recentprimaryattacks[0][0]) <= targetwindow: # with 1 sec of atk
			self.inittarget()

	def targetcount(self,t,aid,players,action):

		if self.istarget: # if already target
			if t-self.targetstart >= targetcooldown: # if we're over the target window
				self.resettargetcount(players)
			else:
				self.recentattacks.append([t,aid,action]) # add the atk
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
				
				self.inittarget()



	def old_targetcount(self, t, aid, players, action = ''):


		if (self.targetstart == -1 or 					# first target
			(t - self.targetstart) > targetcooldown or	# cooldown timer has elapsed
			(self.attackcounter<targetminattacks+1 and (t - self.targetstart) > targetwindow and len(self.targetattackers) < targetminattackers and not self.targetlock) # or previous attack was rogue damage from 1 person
			) and action != 'jaunt':
			self.targetstart = t # restart timer
			self.attackcounter = 0
			self.primaryattackcounter = 0 # to determine spikes only count "primary attacks" and not random extra damage
			self.targetattackers = []
			self.targetlock = False
			self.cleanspikelock = False
			self.healedby = []

		timing = self.targettime(t)
		
		if action == 'jaunt' and timing < targetwindow and self.primaryattackcounter >= 1 and not self.targetlock:
			self.targeted = self.targeted + 1
			self.targetinstance = 1
			self.targetlock = True
			for attacker, time in self.targetattackers:
				self._update_ontarget(time, attacker, players)
				players[attacker].attacks += 1

		elif action != 'jaunt':
			if timing < targetwindow: #if within targeting window
				self.attackcounter += 1 #increase the #attacks on

				if action in primaryattacks:
					self.primaryattackcounter += 1 # increase 'primary' attack count

				if self.targetlock:
					players[aid].attacks += 1 # increase atk count of attacker

				if aid not in [i[0] for i in self.targetattackers]:
					self.targetattackers.append([aid, t]) #add the actor to the attacker list
					self._update_ontarget(t, aid, players)

				for time, hid in self.absorbed:
					if (self.targetstart - time) < predictspiketime: # absorb was fired before the spike
						players[hid].predicts += 1
				self.absorbed = []

				if (self.primaryattackcounter >= targetminattacks or self.attackcounter >= 4) and len(self.targetattackers) >= targetminattackers and not self.targetlock:
					self.targeted = self.targeted + 1
					self.targetinstance = 1
					self.targetlock = True
					for attacker, time in self.targetattackers:
						self._update_ontarget(time, attacker, players)
						players[attacker].attacks += 1

				if timing <= cleanspiketime and self.attackcounter == cleanspikecount:
					self.cleanspiked += 1

			elif timing < targetcooldown and self.targetlock:
				# count trash damage vs non-evaders as attacks on target
				players[aid].attacks += 1

	def healcount(self, t, targetplayer):
		if targetplayer.istargeted(t):
			if self.id not in targetplayer.healedby:
				targetplayer.healedby.append(self.id)
				self.healtiming.append(targetplayer.targettime(t))

			self.ontargetheals += 1
		else:
			self.topups += 1

		if self.action == 'absorb pain':
			self.aps += 1
		elif self.action in absorbs:
			targetplayer.absorbed.append([t, self.id])

	def istargeted(self, t):
		return self.targetstart != -1 and self.targettime(t) < targetwindow

	def targettime(self, t):
		return t - self.targetstart
