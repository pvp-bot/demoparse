# not in use yet
class Target:
	def __init__(self, target, team, start):
		self.start = start # match time of first attack
		self.spiketime = 0 #total time being targeted

		self.target = target # player being targeted
		self.team = team # team being targeted
		self.death = 0 # 1 if dead
		
		self.attacks = [] # how many attacks thrown  [t,actor,action]
		self.attackers = [] # how many attacks thrown  [t,actor,action]
		self.heals = [] # list of heals/absorbs received [t,actor,action]
		self.evades = [] # list of heals/absorbs received [t,actor,action]
		# self.healers = [] # list of support casting on target
		self.greens = 0 # list of support casting on target
		
		self.phasetime = 0 # time into spike when phase hit
		self.atksbeforephase = 0 # number of atks cast before phase/hiber animated

		self.jaunttime = 0 # time into spike when jaunt hit
		self.atksbeforejaunt = 0 # number of atks cast before jaunt animated

		self.greensavailable = 0
		self.greensused = 0

		self.debufftime = False
		self.kbtime = False
		self.spikedeath = False

		self.stats = {}

