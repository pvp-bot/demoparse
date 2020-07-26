from data.powers import absorbs
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
		self.maxhp = 0.0

		self.crey = 0

		self.action = ''
		self.target = ''
		self.reverse = False
		self.emp = False

		# being spiked
		self.targetstart = -1
		self.targetcooldown = 0
		self.attackcounter = 0
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

			if timing <= cleanspike:
				players[aid].ontime += 1
			else:
				players[aid].late += 1

	def targetcount(self, t, aid, players):
		if (self.targetstart == -1 or 					# first target
			(t - self.targetstart) > targetcooldown or	# cooldown timer has elapsed
			(self.attackcounter<targetminattacks and (t - self.targetstart) > targetwindow and len(self.targetattackers) < targetminattackers and not self.targetlock) # or previous attack was rogue damage from 1 person
			):
			self.targetstart = t #start timer
			self.attackcounter = 0
			self.targetattackers = []
			self.targetlock = False

		timing = self.targettime(t)
		if timing < targetwindow: #if within targeting window
			self.attackcounter = self.attackcounter + 1 #increase the #attacks on
			if self.targetlock:
				players[aid].attacks += 1

			if aid not in [i[0] for i in self.targetattackers]:
				self.targetattackers.append([aid, t]) #add the actor to the attacker list
				self._update_ontarget(t, aid, players)

			temp_absorbs = []
			for time, hid in self.absorbed:
				if (self.targetstart - time) < predictspiketime: # absorb was fired before the spike
					players[hid].predicts += 1
				else:
					temp_absorbs.append([time, hid])
			self.absorbed = temp_absorbs

			if self.attackcounter >= targetminattacks and len(self.targetattackers) >= targetminattackers and not self.targetlock:
				self.targeted = self.targeted + 1
				self.targetinstance = 1
				self.targetlock = True
				if timing <= cleanspike:
					self.cleanspiked += 1

				for attacker, time in self.targetattackers:
					self._update_ontarget(time, attacker, players)
					players[attacker].attacks += 1

	def healcount(self, t, targetplayer):
		if targetplayer.istargeted(t):
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
