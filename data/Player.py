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
		if self.targetlock: # its actually a spike
			players[aid].spiketiming.append(timing)
			if self.targetattackers[0][0] == aid:
				players[aid].first += 1

			if timing <= cleanspiketime:
				players[aid].ontime += 1
			else:
				players[aid].late += 1

	def targetcount(self, t, aid, players, action = ''):
		if (self.targetstart == -1 or 					# first target
			(t - self.targetstart) > targetcooldown or	# cooldown timer has elapsed
			(self.attackcounter<targetminattacks and (t - self.targetstart) > targetwindow and len(self.targetattackers) < targetminattackers and not self.targetlock) # or previous attack was rogue damage from 1 person
			) and action != 'jaunt':
			self.targetstart = t #start timer
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
		elif action != 'jaunt':
			if timing < targetwindow: #if within targeting window
				self.attackcounter += 1 #increase the #attacks on
				if action in primaryattacks:
					self.primaryattackcounter += 1
				if self.targetlock:
					players[aid].attacks += 1

				if aid not in [i[0] for i in self.targetattackers]:
					self.targetattackers.append([aid, t]) #add the actor to the attacker list
					self._update_ontarget(t, aid, players)

				for time, hid in self.absorbed:
					if (self.targetstart - time) < predictspiketime: # absorb was fired before the spike
						players[hid].predicts += 1
				self.absorbed = []

				if self.primaryattackcounter >= targetminattacks and len(self.targetattackers) >= targetminattackers and not self.targetlock:
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
