from data.powers import *
from data.config import *
from data.Target import Target
import math


class Player:
	def __init__(self, name, pid):
		self.name = name
		self.id = pid
		self.team = ''
		self.death = ''
		self.hp = 0
		self.hplist = []

		self.lasthp = 0
		self.deathtotal = 0
		self.lastdeath = -14000
		self.lastspikedeath = False
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
		self.archetype = ''
		self.pos = []

		self.writelog = False

		# being spiked
		self.targetstart = -1
		self.attackcounter = 0
		self.primaryattackcounter = 0
		self.targetattackers = []
		self.targeted = 0
		self.targetlock = False
		self.targetinstance = 0
		self.absorbed = [] # List[[time, pid]] where time is when the absorb was placed, pid was the player who placed it

		# new spike count system
		self.recentattacks = [] # [t,aid,action]
		self.recentprimaryattacks = []
		self.lastjaunt = False
		self.istarget = False
		self.ontarget = 0
		self.resets = 0
		self.lastresdebuff = False
		self.painted = False
		self.kbtime = False
		self.csvhold = False

		self.dmgtaken = 0
		self.dmgtakensurv = 0
		self.healreceived = 0
		self.totaldmgtaken = 0
		self.totaldmgtakenonspike = 0
		self.totalhprecovered = 0
		self.totalhealsreceived = 0
		self.totalhealsreceivedontarget = 0
		self.firstblood = 0 # first death in a match

		self.avgspiketiming = 0
		self.medspiketiming = 0 # median
		self.avgspikedist = 0
		self.avgspiketimingvar = 0

		self.avghealspeed = 0
		self.medhealspeed = 0 # median
		self.avghealspeedvar = 0
		self.avghealtiming100 = 0
		self.avghealtiming400 = 0

		# def stats
		self.totalearlyjaunts = 0
		self.totalearlyphases = 0
		self.lastphase = -60
		self.phaseid = 0 # fxID for phase powers, 0 when not active
		self.atkstakenonspike = 0
		self.jauntreaction = []
		self.phasereaction = []
		self.deathtime = []

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
		self.killparticipation = 0

		# healing peeps
		self.ontargetheals = 0
		self.healspeed = []
		self.healtiming100 = []
		self.healtiming400 = []
		self.healbin = {10:0,100:0,200:0,400:0,800:0,1200:0,1500:0,1700:0,3200:0,9999:0,99999:0} # binned heal count by missing HP
		self.aps = 0 # absorb pain
		self.predicts = 0 # predicted the spike target and gave an absorb
		self.guesses = 0

		self.healalpha = 0
		self.healontime = 0
		self.healquick = 0
		self.healtimely = 0
		self.healslow = 0
		self.healearly = 0
		self.heallate = 0
		self.healfollowup = 0
		self.healtopup = 0
		self.healfatfinger = 0
		self.healfatfingerlist = []
		self.phaseheals = 0
		

		self.targetheals = []
		self.targetevades = []
		self.greens = 20 # assumes all slots greens
		self.greensused = 0
		self.greensavailable = 20 # assumes all slots greens
		
		self.support = False
		self.supportextras = {}
		self.cmcount = 0
		
		self.healstotal = 0
		self.healontarget = 0
		self.healmisseddead = 0
		self.healpowers = {'absorb pain':0,'heal other':0,'insulating circuit':0,'rejuvenating circuit':0,'share pain':0,'soothe':0,'aid other':0,'glowing touch':0,'cauterize':0,'alkaloid':0,'o2 boost':0}

		self.stats = {}
		self.atkchains = {}
		self.firstatktiming = False
		self.followuptiming = []
		self.atkbin = {0:0,0.34:0,0.68:0,1.0:0,1.5:0,2.0:0,9999:0} # binned heal count by missing HP
		self.lateatks = 0
		self.firstdist = []
		self.firsthealdist = []
		self.utilcount = 0

		self.lastrepeat = -30 # last time player used a repeat power (EF) - to prevent padding atk stats

	def reset(self):
		self.hp = ''
		self.action = ''
		self.target = ''
		self.targetteam = ''
		self.death = ''
		self.reverse = False
		self.targetinstance = 0
		self.writelog = False

	def _update_ontarget(self, t, aid, players,dist):
		timing = (t - self.targetstart)
		players[aid].spiketiming.append(timing)
		if dist > 0:
			players[aid].firstdist.append(dist)
		players[aid].ontarget += 1
		if self.death: # if spike is successful
			players[aid].killparticipation += 1 # count



	def getdist(self,x,y,t):
		try:
			p1,p2 = x[-1],y[-1]
		except:
			return 0
		for pos in x: # where attacker was x time ago
			if pos[3]>t-1 and pos[3]<p1[3]:
				p1 = pos
		# for pos in y: # where attacker was x time ago
		# 	if pos[3]>t-0.0 and pos[3]<p2[3]:
		# 		p2 = pos
		return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2)

	def endtarget(self,players,spikes):
		players[self.targetattackers[0]].first += 1
		for atk in self.recentattacks:
			players[atk[1]].attacks += 1
		for aid in self.targetattackers:
			timing = matchtime*2 # large number to catch error in output
			firstdist = 0 # 
			atkchain = ''
			for atk in self.recentattacks:
				if atk[1] == aid:
					if atk[2] in powerdelay:
						timing = min(timing,atk[0]) # for select powers (e.g. EF) timing is based on hit rather than cast since we're concerned with timing relative to spike start
						timing = min(timing,atk[0]+powerdelay[atk[2]]) # for select powers (e.g. EF) timing is based on hit rather than cast since we're concerned with timing relative to spike start
					else:
						timing = min(timing,atk[0]) # update attacker timing for avg
					atkchain += atk[2]+' - ' # change atk chain to string
					
					# followup attack timing stats
					if atkchain.count(' - ') == 1: # if first attack by player
						players[aid].firstatktiming = atk[0]
						firstdist = atk[3]
						if atk[0] > self.targetstart + targetwindow: # if first attack is late
							players[aid].lateatks += 1
							players[aid].ontarget -= 0.5 # half credit for late first attacks

						for abin in self.atkbin: # find the matching atk bin
							if atk[0]-self.targetstart < abin:
									players[aid].atkbin[abin] += 1 # count timing for that bin
									break # only count 1

					elif atkchain.count(' - ') == 2:
						players[aid].followuptiming.append(atk[0]-players[aid].firstatktiming)

			players[aid].firstatktiming = False		

			atkchain = atkchain[:-3] # trailing " - "
			if atkchain in players[aid].atkchains.keys():
				players[aid].atkchains[atkchain] += 1
			else:
				players[aid].atkchains[atkchain] = 1

			self._update_ontarget(timing, aid, players,firstdist)

		# new spike
		spikes.append(Target(self.name,self.team,self.targetstart))

		healsreceived = 0
		

		# spike data
		spikes[-1].attacks = self.recentattacks[:]
		spikes[-1].attackers = self.targetattackers[:]
		spikes[-1].evades = self.targetevades[:]
		spikes[-1].spiketime = self.targetstart - self.recentattacks[-1][0]
		
		if self.lastresdebuff:
			spikes[-1].debufftime = self.lastresdebuff
		elif self.painted and self.painted > self.targetstart - paintedtimer:
			spikes[-1].debufftime = self.recentattacks[0][0]
		if self.kbtime > self.targetstart - targetwindow and self.kbtime < self.recentattacks[-1][0]:
			spikes[-1].kbtime = self.kbtime
		if self.lasthp == 0:
			spikes[-1].death = 1
		if self.death == 1:
			self.targethp.append([self.lastdeath/1000,0])
			spikes[-1].spikedeath = self.lastdeath/1000 - self.targetstart
			self.lastspikedeath = self.lastdeath
			self.deathtime.append(spikes[-1].spikedeath)

		spikes[-1].hp = self.targethp[:]
		
		# calc spike heals at end of spike
		for h in self.targetheals:
			if h[2] != 'green' and h[2] != 'spirit ward': # to not count greens as heals
				healsreceived += 1
				if self.isrecentheal(self.targetstart,h[0]):
					self.totalhealsreceivedontarget += 1

					if h[1] not in self.healedby: # if first heal by X on target
						if len(self.healedby) == 0 or h[0] == self.targetheals[0][0]:
							players[h[1]].healalpha += 1 # if first heal (or tied first)
						self.healedby.append(h[1]) # add to spike healer list

						players[h[1]].healspeed.append(h[0]-self.targetstart) # heal speed relative to spike start

						# heal timing vs damage taken at different missing HPs
						dmg100,dmg400 = False,False
						
						if self.targethp[0][1] > self.maxhp - 40 and len(self.targethp)>1 and self.targethp[1][0] > self.targetstart + 1: # if target starts spike within 100 of max HP and not already taking damage, plus no damage between 0 and 1s
							for hp in self.targethp:
								if not dmg100 and hp[1] < self.targethp[0][1] - 100 and h[2] not in healhitexclude: # if non negl damage (~80hp) has been taken
									dmg100 = hp[0] # time first damage occurs, for heal categorizing
									players[h[1]].healtiming100.append(abs(h[4]-hp[0])) # absolute time between first damage and heal hit
								if not dmg400 and hp[1] < self.targethp[0][1] - 400 and h[2] not in healhitexclude: # if non negl damage (~80hp) has been taken
									dmg400 = hp[0] # time first damage occurs, for heal categorizing
									players[h[1]].healtiming400.append(abs(h[4]-hp[0])) # absolute time between first damage and heal hit

						
						missinghp = False
						for i in range(1,len(self.targethp)): # check recent hp
							if self.targethp[i][0] > h[4] - 1/30 and not missinghp: # if hp time is after heal hit time (with 1 tick leeway)
								missinghp = self.maxhp - self.targethp[i-1][1] # then get the last most recent hp
						if missinghp:
							for hbin in self.healbin: # find the matching heal bin
								if missinghp <= hbin:
									players[h[1]].healbin[hbin] += 1
									break

				
						atkcount = 0
						for atk in self.recentattacks:
							if atk[0]<h[0]: # num of attacks cast before heal thrown
								atkcount += 1

						if self.death == 1 and h[4] > self.lastdeath/1000 + 1/30: # if death and heal hits after death time (plus 1 tick leeway)
							players[h[1]].heallate += 1

							if (h[0] - self.targetstart) < 1.5: # if late, but cast fast
								players[h[1]].healbin[99999] += 1 # late (fast)
							else:
								players[h[1]].healbin[9999] += 1 # late (normal)

							if h[0] > self.targetstart + 2.5: # if heal is SLOW on top of being LATE
								players[h[1]].healontarget -= 0.5 # half 

						elif self.targethp[0][1] >= self.maxhp - 10 and h[4] < dmg100 - 1/30 and h[2] not in healhitexclude: # if target starts at max hp and the first heal hits before damage (2 tick leeway)
							players[h[1]].healearly += 1
						elif h[0] < self.targetstart + targethealwindow or h[4] < dmg100 + targethealwindowdmg: # if heal cast within 2s of spike start or hits within 1s of 
							players[h[1]].healquick += 1
						elif atkcount <= targethealatks or h[0] < self.targetstart + targethealwindow*2 or h[4] < dmg100 + targethealwindowdmg*2: # cast before 4 attacks, hits before 2s after dmg, or within 4s of start
							players[h[1]].healontime += 1
						else:
							players[h[1]].healslow += 1
							players[h[1]].healontarget -= 0.5 # half credit for slow first heals

						players[h[1]].healontarget += 1 # times on a heal target
					
					else:
						players[h[1]].healfollowup += 1

					players[h[1]].ontargetheals += 1 # heals thrown on target

				else:
					players[h[1]].healtopup += 1

		self.targetheals = [x for x in self.targetheals if self.isrecentheal(self.targetstart,x[0])] # remove recent attacks outside window
		spikes[-1].heals = self.targetheals[:]

		# spike summary
		# spikes[-1].stats['atks before evade'] = ''
		if len(self.targetevades) > 0:
			if (self.targetevades[0][2] == 'phase shift' or self.targetevades[0][2] == 'hibernate'):
				self.phasereaction.append(self.targetevades[0][0]-spikes[-1].start)
			elif (self.targetevades[0][2] == 'jaunt' and self.targetevades[0][0] > spikes[-1].start): #or self.targetevades[0][2] == 'translocation'
				self.jauntreaction.append(self.targetevades[0][0]-spikes[-1].start)
			# spikes[-1].stats['atks before evade'] = atkb4evade
		
		spikes[-1].stats['attackers'] = len(self.targetattackers)
		spikes[-1].stats['attacks'] = len(self.recentattacks)

		spikes[-1].stats['heals received'] = healsreceived
		spikes[-1].stats['greens available'] = self.greensavailable # at the start of the spike
		spikes[-1].stats['greens used'] = self.greensavailable - self.greens

		spikestartcalc = self.recentattacks[0][0] # first attack for calculating duration
		if self.recentattacks[0][2] == 'enervating field' and len(self.recentattacks) > 1:
			spikestartcalc = min(self.recentattacks[1][0],self.recentattacks[0][0]+1.5) # if first attack is EF then use the earlier of EF hit and attack #2
		if self.death != 1:
			self.dmgtakensurv += -self.dmgtaken
			spikes[-1].stats['spike duration'] = abs(self.recentattacks[-1][0] - spikestartcalc)
		else:
			spikes[-1].stats['spike duration'] = self.lastspikedeath/1000 - spikestartcalc

		# spikes[-1].stats['total hp recovered'] = self.healreceived
		spikes[-1].stats['total hp lost'] = -self.dmgtaken
		spikes[-1].stats['hp after spike'] = self.lasthp

		for p in players.values(): 
			# count num spikes missed if dead
			if p.lastdeath > 0:
				lastdeath = p.lastdeath/1000
				if p.team != self.team:
					respawn = math.ceil((lastdeath)/15)*15+15 # includes 15 sec uneffecting
					if lastdeath < self.targetstart and self.recentattacks[-1][0] < respawn:
						p.misseddead += 1
				# count num heals missed if dead
				if p.team == self.team and p.id != self.id:
					respawn = math.ceil((lastdeath)/15)*15+15 # 1 sec safety, includes 15 sec uneffecting
					if lastdeath > 0 and lastdeath < self.targetstart and self.recentattacks[-1][0] < respawn:
						p.healmisseddead += 1


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

	# def targetstarttime(patks,atks):
		# todo

	def inittarget(self,t,players):
		if self.lasthp != 0:
			self.istarget = True
			self.targeted += 1
			self.targetinstance = 1 # for spreadsheet
			self.writelog = True

			self.greensavailable = self.greens

			# todo
			# self.targetstart = targetstarttime(self.recentprimaryattacks,self.recentattacks)

			if len(self.recentprimaryattacks) > 0 and self.recentprimaryattacks[0][2] != 'enervating field':
				self.targetstart = self.recentprimaryattacks[0][0]
			elif len(self.recentprimaryattacks) > 1:
				self.targetstart = self.recentprimaryattacks[1][0]
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

			# add recent hp data to spike data
			hpstart = self.hplist[0][1] # start of spike has most recent hp
			for hp in self.hplist:
				if hp[0] < self.targetstart: # check if more recent hp data, but before spike start
					hpstart = hp[1]
			self.hplist = [hplist for hplist in self.hplist if (hplist[0] > self.targetstart)] # remove old hp data
			self.hplist.insert(0,[self.targetstart,hpstart]) # append pre-spike hp to start of list
			self.targethp = self.hplist[:]

			# determine preevades
			if len(self.targetevades) > 0:
				lastevade = self.targetevades[-1]
				self.targetevades = []
				if (t-lastevade[0] < targetwindow*2):
					self.targetevades.append(lastevade)

	def jauntoffone(self,t,players): # count as target if jaunt off single primary attack
		if not self.istarget and len(self.recentprimaryattacks) == 1 and abs(t-self.recentprimaryattacks[0][0]) <= targetwindow/2 and self.recentprimaryattacks[0] in jauntoffoneattacks: # with 1 sec of atk
			self.inittarget(t,players)

	def entanglecheck(self,atk,t,aid):
		if atk[2] == 'strangler' and atk[1] == aid and atk[0] > t-0.5:
			return False # strangler cast by attacker in the last .5 sec
		else:
			return True

	def isrecent(self,time,attacktime):
		t = time-attacktime # difference between the atk time and current time 
		if self.istarget:
			window = time - self.recentattacks[0][0] + targetcooldown
		else:
			window = targetwindow
		if t < window:
			return True
		else:
			return False

	def isphased(self,time):
		if self.lastphase + phasemax > time and self.lastphase + phasedelay < time:
			return True
		else:
			return False

	def isrecentheal(self,targetstart,healtime):
		if healtime > targetstart + 0.5:
			return True
		else:
			return False

	def targetcount(self,t,aid,players,action,spikes,rogues):
		powerrepeat = False # powers that will activate FX multiple times on a spike


		if action in repeatpowers: # really just enervating field
			for atk in self.recentattacks:
				if atk[2] == action:
					powerrepeat = True

		if not powerrepeat:

			if action not in repeatpowers or t > players[aid].lastrepeat + repeat_reset: # only count if not a repeat power OR if the repeat power hasn't been used resently
				players[aid].attackstotal += 1 

			# entangle check (anim share with strangler)
			if action == 'entangle':
				self.recentattacks = [atk for atk in self.recentattacks if self.entanglecheck(atk,t,aid)]

			# adjust attack timing for irregular attacks
			if action in powerdelay:
				t = t - powerdelay[action]

			dist = self.getdist(self.pos,players[aid].pos,t)
			hit_time = ''
			if action in hittiming:
				hit_time = t + hittiming[action][0] + dist/hittiming[action][1]

			if self.istarget: # if already target
				self.recentattacks.append([t,aid,action,round(dist,0),hit_time]) # add the atk
				if action in primaryattacks:
					self.recentprimaryattacks.append([t,aid,action,round(dist,0),hit_time])
				for atk in self.recentattacks:
					if atk[1] not in self.targetattackers: # add the atkr if needed
							self.targetattackers.append(atk[1])
				

			if not self.istarget:

				self.recentattacks.append([t,aid,action,round(dist,0),hit_time]) # add the atk
				if action in primaryattacks:
					self.recentprimaryattacks.append([t,aid,action,round(dist,0),hit_time])
				
				for atk in self.recentattacks:
					if not self.isrecent(t,atk[0]):
						rogues.append([atk[0],atk[1],atk[2],self.id])
				
				self.recentattacks = [x for x in self.recentattacks if self.isrecent(t,x[0])] # remove recent attacks outside window
				self.recentprimaryattacks = [x for x in self.recentprimaryattacks if self.isrecent(t,x[0])]

				self.targetattackers = []
				for atk in self.recentattacks:
					if atk[1] not in self.targetattackers: # add the atkr if needed
						self.targetattackers.append(atk[1])
				self.jauntoffone(t,players)

				weightedattackadj = 0
				for atk in self.recentattacks:
					if atk[2] in weightedattacks:
						weightedattackadj += weightedattacks[atk[2]]

				if  (
					len(self.targetattackers) >= targetminattackers and not self.istarget and # at least 2 people on target and not already target
					(((len(self.recentprimaryattacks) + weightedattackadj + len(self.recentattacks))/2 >= targetminattacks) # if min 2 primary attacks (weighted)
					# or (len(self.recentattacks) >= targetminattacks*2) # or if people throw at least 4x trash damage on someone i.e. 4 BBs on emp at same time
					or (len(self.recentprimaryattacks) == targetminattacks/2 and t-self.lastjaunt < targetwindow/2) # if jaunt slightly before primary atk activated				# or (len(self.recentprimaryattacks) >= targetminattacks-1 and len(self.recentattacks) >= targetminattacks+2) # if 1
					)):
					self.inittarget(t,players)


	def healcount(self, t, targetplayer,action):
		
		if not targetplayer.isphased(t):
			dist = self.getdist(targetplayer.pos,self.pos,t)
			targetplayer.totalhealsreceived += 1

			hit_time = ''
			if action in hittiming:
				hit_time = t + hittiming[action][0] + dist/hittiming[action][1]

			targetplayer.targetheals.append([t,self.id,action,round(dist,0),hit_time])

			# if cast on non-target and their hp is full at cast time and no recent attacks on player, add to self FF list to calc at HP change; exclude insulating circuit
			if (
				not targetplayer.istarget and len(targetplayer.hplist) and 
				targetplayer.hplist[-1][1] >= targetplayer.maxhp - 6 > 0 and 
				len(targetplayer.recentattacks) == 0 and action != 'insulating circuit'
				): 
				targetplayer.healfatfingerlist.append([hit_time,self.id])
				self.healfatfinger += 1


			if action in absorbs:
				if not targetplayer.istarget:
					self.guesses += 1
					targetplayer.absorbed.append([t, self.id])
			else:
				self.healstotal += 1
		else:
			self.phaseheals += 1
